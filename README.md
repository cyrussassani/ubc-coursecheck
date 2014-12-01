<h1>UBC Course Checker</h>

<p>UBC Course Checker works to determine the number of remaining seats available in a course. The script can then either register in the course automatically or simply notify (open the course link).</p>
<p>To minimize the need to install extra modules like mechanize or requests for people who may not be tech-savy, only libraries that are already part of Python's Standard Library are included.</p>

<h2>Usage</h>
<p>The script requires python 2.7 to run so make sure you have that installed.</p>
<p>Save the code into a file called ubcCourseChecker.py</p>
<p>You can run the file using either  <code>python ubcCourseChecker.py</code> or simply right clicking and using the launcher.</p>
<p>Some notes:</p>
<ul>
  <li>Make sure you enter the section URL, it should look like this: <code>https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=XXXX&course=XXX&section=XXX</code></li>
  <li>Only enter <b>y</b> or <b>n</b>, not yes or no. There's no catching protocol.</li>
  <li>Mac users: If you want to keep your laptop awake until it registers you (or you terminate the process), use: <code>$ caffeinate -i -s python ubcCourseChecker.py</code>. The screen will turn off but python will keep running.</li>
</ul> 
