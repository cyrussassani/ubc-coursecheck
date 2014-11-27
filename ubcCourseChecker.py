import urllib
import urllib2
import re

totalSeats = re.compile("<td width=200px>Total Seats Remaining:</td>" + "<td align=left><strong>(.*?)</strong></td>")
generalSeats = re.compile("<td width=200px>General Seats Remaining:</td>" + "<td align=left><strong>(.*?)</strong></td>")
restrictedSeats = re.compile("<td width=200px>Restricted Seats Remaining\*:</td>" + "<td align=left><strong>(.*?)</strong></td>")

def checkSeats(varCourse):

  url = varCourse
  ubcResp = urllib.urlopen(url);
  ubcPage = ubcResp.read();

  t = re.search(totalSeats, ubcPage)
  g = re.search(generalSeats, ubcPage)
  r = re.search(restrictedSeats, ubcPage)

  if t:
    print "Total Seats Remaining:", t.group(1)
  else:
    print "Can't locate seats"

  if g:
    print "General Seats Remaining:", g.group(1)
  else:
    print "Can't locate seats"
    
  if r:
    print "Restricted Seats Remaining:", r.group(1)
  else:
    print "Can't locate seats"


course = raw_input("Enter course URL:")
checkSeats(course)
