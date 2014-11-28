import urllib
import urllib2
import re
import time
import webbrowser

# Notify that a course is available
def notify():
  print("Open browser")
  webbrowser.open_new(course)

# Delay to prevent sending too many requests
def wait(varDelay):
  time.sleep(varDelay) 

# Scan webpage for seats
def checkSeats(varCourse):

  url = varCourse
  ubcResp = urllib.urlopen(url);
  ubcPage = ubcResp.read();


  # Search for the seat number element
  t = re.search(totalSeats, ubcPage)
  g = re.search(generalSeats, ubcPage)
  r = re.search(restrictedSeats, ubcPage)

  # Find remaining seats
  if t:
    if t.group(1) == '0':
      return 0
  else:
    print "Can't locate seats"

  if g:
    if g.group(1) != '0':
      return 1
  else:
    print "Can't locate seats"
    
  if r:
    if r.group(1) != '0':
      return 2
  else:
    print "Can't locate seats"

# Search pattern (compiled for efficiency)
totalSeats = re.compile("<td width=200px>Total Seats Remaining:</td>" + "<td align=left><strong>(.*?)</strong></td>")
generalSeats = re.compile("<td width=200px>General Seats Remaining:</td>" + "<td align=left><strong>(.*?)</strong></td>")
restrictedSeats = re.compile("<td width=200px>Restricted Seats Remaining\*:</td>" + "<td align=left><strong>(.*?)</strong></td>")

# Get course parameters
course = raw_input("Enter course + section link:") #"file:///Users/cyrus/Box%20Sync/Programming/Python/UBC%20Course%20Fetch/apsc598x.html"
acceptRestricted = raw_input("Allowed restricted seating? (y/n)")
delay = int(raw_input("Check every _ seconds?"))

# Prevent too low of a search rate/DOSing the website
if delay < 5:
  delay = 5

# Confitional for determining whether to notify
while True:
  status = checkSeats(course)
  print(status)
  if status == 0:
    print("No")
    wait(delay)
    continue
  if status == 1:
    notify()
    break
  if status == 2:
    if acceptRestricted == "y":
      notify()
      break
    elif acceptRestricted == "n":
      wait(delay)
      continue
