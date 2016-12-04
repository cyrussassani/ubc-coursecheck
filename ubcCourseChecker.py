try:
  from http.cookiejar import CookieJar
except ImportError:
  from cookielib import CookieJar

try:
  input = raw_input
except NameError:
  pass

try:
  from urllib.request import HTTPCookieProcessor, build_opener, install_opener, Request, urlopen
  from urllib.parse import urlencode
except ImportError:
  from urllib2 import HTTPCookieProcessor, build_opener, install_opener, Request, urlopen
  from urllib import urlencode

import re
import time
import webbrowser
from random import randrange

# Notify that a course is available
def notify():
  print("Seat available.")
  webbrowser.open_new(courseURL)

# Delay to prevent sending too many requests
def wait(varDelay):
  randDelay = delay + int(randrange(11))
  time.sleep(randDelay) 

# Automatically registers in the course
def autoRegister():
  # Cookie / Opener holder
  cj = CookieJar()
  opener = build_opener(HTTPCookieProcessor(cj))

  # Login Header
  opener.addheaders = [('User-agent', 'UBC-Login')]

  # Install opener
  install_opener(opener)

  # Form POST URL
  postURL = "https://cas.id.ubc.ca/ubc-cas/login/"

  # First request form data
  formData = {
    'username': cwl_user,
    'password': cwl_pass,
    'execution': 'e1s1',
    '_eventId': 'submit',
    'lt': 'xxxxxx',
    'submit': 'Continue >'
    }

  # Encode form data
  data = urlencode(formData).encode('UTF-8')

  # First request object
  req = Request(postURL, data)

  # Submit request and read data
  resp = urlopen(req)
  respRead = resp.read().decode('utf-8')

  # Find the ticket number
  ticket = "<input type=\"hidden\" name=\"lt\" value=\"(.*?)\" />"
  t = re.search(ticket, respRead)

  # Extract jsession ID
  firstRequestInfo = str(resp.info())
  jsession = "Set-Cookie: JSESSIONID=(.*?);"
  j = re.search(jsession, firstRequestInfo)

  # Second request form data with ticket
  formData2 = {
    'username': cwl_user,
    'password': cwl_pass,
    'execution': 'e1s1',
    '_eventId': 'submit',
    'lt': t.group(1),
    'submit': 'Continue >'
    }

  # Form POST URL with JSESSION ID
  postURL2 = "https://cas.id.ubc.ca/ubc-cas/login;jsessionid=" + j.group(1)

  # Encode form data
  data2 = urlencode(formData2).encode('UTF-8')

  # Submit request
  req2 = Request(postURL2, data2)
  resp2 = urlopen(req2)

  loginURL = "https://courses.students.ubc.ca/cs/secure/login"
  summerURL = 'https://courses.students.ubc.ca/cs/main?sessyr={year}&sesscd=S'.format(year=year)
  # Perform login and registration
  urlopen(loginURL)
  if season =='S':
  	urlopen(summerURL)
  register = urlopen(registerURL)
  respReg = register.read()
  print("Course Registered.")
  webbrowser.open_new('https://ssc.adm.ubc.ca/sscportal/')


# Scan webpage for seats
def checkSeats(varCourse):

  url = varCourse
  ubcResp = urlopen(url);
  ubcPage = ubcResp.read().decode('utf-8');

  # Search for the seat number element
  t = re.search(totalSeats, ubcPage)
  g = re.search(generalSeats, ubcPage)
  r = re.search(restrictedSeats, ubcPage)

  # Find remaining seats
  if t:
    if t.group(1) == '0':
      return 0
  else:
    print ("Error: Can't locate number of seats.")

  if g:
    if g.group(1) != '0':
      return 1
  else:
    print ("Error: Can't locate number of seats.")
    
  if r:
    if r.group(1) != '0':
      return 2
  else:
    print ("Error: Can't locate number of seats.")

# Search pattern (compiled for efficiency)
totalSeats = re.compile("<td width=200px>Total Seats Remaining:</td>" + "<td align=left><strong>(.*?)</strong></td>")
generalSeats = re.compile("<td width=200px>General Seats Remaining:</td>" + "<td align=left><strong>(.*?)</strong></td>")
restrictedSeats = re.compile("<td width=200px>Restricted Seats Remaining\*:</td>" + "<td align=left><strong>(.*?)</strong></td>")

# Get course parameters
courseURL = input("Enter course + section link:")
season = input("Summer course (y/n):")
year = input("Term year (2015/2016/2017/...):")
acceptRestricted = input("Allowed restricted seating? (y/n):")
delay = int(input("Check every _ seconds?"))
register = input("Autoregister when course available? (y/n):")
if register == "y":
  cwl_user = input("CWL Username:")
  cwl_pass = input("CWL Password:")

# Extract department, course #, and section #
deptPattern = 'dept=(.*?)&'
coursePattern = 'course=(.*?)&'
sectionPattern = 'section=(.*)'

dept = re.search(deptPattern, courseURL)
course = re.search(coursePattern, courseURL)
sect = re.search(sectionPattern, courseURL)

if season == 'y':
  season = 'S'
else:
  season = 'W'

registerURL = 'https://courses.students.ubc.ca/cs/main?sessyr=' + year + '&sesscd=' + season + '&pname=subjarea&tname=subjareas&submit=Register%20Selected&wldel=' + dept.group(1) + '|' + course.group(1) + '|' + sect.group(1)
courseURL = 'https://courses.students.ubc.ca/cs/main?sessyr=' + year + '&sesscd=' + season + '&pname=subjarea&tname=subjareas&req=5&dept=' + dept.group(1) + '&course=' + course.group(1) +'&section=' + sect.group(1)

# Prevent too fast of a search rate/DOSing the website
if delay < 15:
  delay = 15

print ("Scanning seat availablility...")

# Conditional for determining whether to register/notify
while True:
  status = checkSeats(courseURL)
  if status == 0:
    wait(delay)
    continue
  if status == 1:
    if register == 'y':
      autoRegister()
    else:
      notify()
    break
  if status == 2:
    if acceptRestricted == "y":
      if register == 'y':
        autoRegister()
      else:
        notify()
      break
    else:
      wait(delay)
      continue