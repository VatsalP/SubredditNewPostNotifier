"""
	Copyright (C) 2015 Vatsal Parekh
	
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#!/usr/bin/python3
import praw
import smtplib
import OAuth2Util
import logging
from sys import exit
from time import sleep, strftime

def ReadFile(stri):
	"""
	Reads file and returns a string if the file is title.txt or a list otherwise
	"""
	f = open(stri, 'r')
	readStuff = f.read()
	f.close()
	return readStuff
	

def CheckDuplicate(url):
	"""
	Checks froma list of urls for duplicate. 
	If presents then return False else writes to the urls file and return True
	"""
	readStuff = ReadFile("urls")
	readStuff = readStuff.split(" ")
	for item in readStuff:
		if item == url:
			return True
	readStuff.pop()
	readStuff.insert(0, url)
	readStuff = " ".join(readStuff)
	f = open("urls","w")
	f.write(readStuff)
	f.close()
	return False
	

		
def UseMail(lis, msg):
	"""
	Sends mail to a list of email ids
	"""
	fromaddr = username = 'youremail@email.com'
	password = 'yourpassword'
	
	server = smtplib.SMTP('smtp.whichevermailyouareusing.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	for item in lis:
		server.sendmail(fromaddr, item, msg)
		mailsent = "MAIL SENT TO {}".format(item)
		logging.info(mailsent)
	server.quit()


def main():
	r = praw.Reddit(user_agent='Personal_messenger:v0.1')
	o = OAuth2Util.OAuth2Util(r)
	o.refresh(force=True)
	
	logging.basicConfig(filename='details.log',level=logging.DEBUG)
	timestring = strftime('%X %x %Z')
	timestring = "Start time: " + timestring
	logging.info(timestring)
			
	while True:
		try:
			titlecompare = ReadFile("title.txt")

			subreddit = r.get_subreddit('subredditname')
			subreddit_generator = subreddit.get_new(limit=1)
			for submission in subreddit_generator:
				title = submission.title
				if titlecompare == title:
					continue
				else:
					f = open('title.txt','w')
					f.write(title)
					f.close()
					
					#Checks for Duplicate and continues to next iteration if true
					contnext = CheckDuplicate(submission.url)
					if contnext: 
						continue
					
					if not submission.is_self:
						mesg = "url: {}  |  title: {}  |  url of Reddit comment thread: {}  {}".format(submission.url, title, submission.link_flair_text, submission.permalink)
					else:
						continue
					
					# Email related			
					msg = "\r\n".join([
						"From: The free game notification bot",
						"To: You ofcourse",
						"Subject: A new post at /r/Freegamefindings",
						"",
						mesg
					])
					lis = ReadFile("emailids")
					lis = lis.split(" ")
					UseMail(lis, msg)
			sleep(60)
						
		except KeyboardInterrupt:
			timestring = strftime('%X %x %Z')
			timestring = "Exit time: " + timestring
			logging.info(timestring)
			exit(0)
		except Exception as e:
			exception = "Exception: " + str(e)
			logging.error(exception)

if __name__ == "__main__":
	main()
