from ics import Calendar
from urllib.request import urlopen
from markupsafe import escape

url = "http://ade.univ-tours.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=ca4182f302426b0cdf58fd19a72c4dbe31b66c493702208e664667048bc043732a2c262ab3ba48506729f6560ae33af6fc01170004907f5cc88c870a3a988597,1"


source = Calendar(urlopen(url).read().decode())
clean = Calendar()

teachers = set()

for event in source.events:
    desc = event.description.split('\n')
    teachers.add(desc[3])

for teacher in teachers:
    print("<li>" + teacher + " - Lien: http://edt.alexscode.com:5000/edt/" + teacher.replace(" ", "%20") + "</li> ")