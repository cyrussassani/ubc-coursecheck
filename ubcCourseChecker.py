import urllib
import urllib2
import cookielib
import re
import time
import webbrowser

# Notify that a course is available
def notify():
  print("Seat available.")
  webbrowser.open_new(courseURL)

# Delay to prevent sending too many requests
def wait(varDelay):
  time.sleep(varDelay) 

# Automatically registers in the course
def autoRegister():
  # Cookie / Opener holder
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

  # Login Header
  opener.addheaders = [('User-agent', 'UBC-Login')]

  # Install opener
  urllib2.install_opener(opener)

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
  data = urllib.urlencode(formData)

  # First request object
  req = urllib2.Request(postURL, data)

  # Submit request and read data
  resp = urllib2.urlopen(req)
  respRead = resp.read()

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
  data2 = urllib.urlencode(formData2)

  # Submit request
  req2 = urllib2.Request(postURL2, data2)
  resp2 = urllib2.urlopen(req2)

  loginURL = "https://courses.students.ubc.ca/cs/secure/login"

  # Perform login and registration
  urllib2.urlopen(loginURL)
  register = urllib2.urlopen(registerURL)
  respReg = register.read()
  print("Course Registered.")
  webbrowser.open_new('https://ssc.adm.ubc.ca/sscportal/')


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
courseURL = raw_input("Enter course + section link:")
acceptRestricted = raw_input("Allowed restricted seating? (y/n)")
delay = int(raw_input("Check every _ seconds?"))
register = raw_input("Autoregister when course available? (y/n)")
if register == "y":
  cwl_user = raw_input("CWL Username:")
  cwl_pass = raw_input("CWL Password:")

# Extract department, course #, and section #
deptPattern = 'dept=(.*?)&'
coursePattern = 'course=(.*?)&'
sectionPattern = 'section=(.*)'

dept = re.search(deptPattern, courseURL)
course = re.search(coursePattern, courseURL)
sect = re.search(sectionPattern, courseURL)

registerURL = 'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&submit=Register%20Selected&wldel=' + dept.group(1) + '|' + course.group(1) + '|' + sect.group(1)

# Prevent too fast of a search rate/DOSing the website
if delay < 10:
  delay = 10

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
