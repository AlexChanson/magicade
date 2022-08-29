from flask import Flask
import flask as fl
from markupsafe import escape
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from ics import Calendar
from urllib.request import urlopen

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': 'data/tmp/cache/data',
    'cache.lock_dir': 'data/tmp/cache/lock'
}

url = "http://ade.univ-tours.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=ca4182f302426b0cdf58fd19a72c4dbec49a74fae5535d80911af2f48666394e57d58ab4c63f8fe92968762d8416ed8d6aad19fe006b760288bd644fb363dc02,1"
cache = CacheManager(**parse_cache_config_options(cache_opts))
app = Flask(__name__)


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route("/clear_caches")
def empty_cache():
    from beaker.cache import cache_managers
    for _cache in cache_managers.values():
        _cache.clear()
    return fl.Response("cache cleared")


@app.route('/edt/<string:teacher_name>')
def show_edt(teacher_name):
    edt = parse_edt(teacher_name)

    resp = fl.Response(edt)
    resp.headers['Content-Type'] = 'text/calendar;charset=UTF-8'
    resp.headers['Content-disposition'] = 'inline; filename=ADECal_'+escape(teacher_name)+'.ics'
    return resp


@cache.cache('show_edt', expire=3600)
def parse_edt(teacher_name):
    source = fetch_all()
    clean = Calendar()

    for event in source.events:
        desc = event.description
        if teacher_name.lower() in desc.lower():
            clean.events.add(event)

    print(clean)
    return str(clean)


@cache.cache('fetch_all', expire=1800)
def fetch_all():
    return Calendar(urlopen(url).read().decode())


if __name__ == '__main__':
    app.run()
