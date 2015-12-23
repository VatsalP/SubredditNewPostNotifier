#**Subreddit new post email notifier**

A simple python script that notifies a number of emailids about a new link in the subreddit specified in the script


You will need to install praw and OAuth2Util.
Just run this commands:


pip3 install praw

pip3 install praw-oauth2util


##**Setup to be done before first run:**

There are four files required for the script to run(name them exactly the same and put them in same folder as the main script):

oauth.ini, emailids, title.txt, urls

1. Read about oauth.ini at https://github.com/SmBe19/praw-OAuth2Util/


2. emailids: 
	*Put the email ids in here with space between every emailid.


3. title.txt:
	Just create this file no need to do anything with it.
	
4. urls:
	This is the file that check for posts linking the same stuff. You will have to manually put the links in here.

	The format is like this or check the sample urls:
	
	"url1 url2 url3"
	
	Its upto you to link how many links you want.
