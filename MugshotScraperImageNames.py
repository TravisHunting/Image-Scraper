#!/usr/bin/env python3
import requests
# import pandas as pd
import re
import os.path
from bs4 import BeautifulSoup

global script_dir
script_dir = os.path.dirname(__file__)

global urlprefix
urlprefix = "https://mugshots.com"
#mugshots.com "next page" button provides only the extension to the base URL
global next_page
global current_page
global counter 
global limit
global pagecounter
pagecounter = 0
global pics_downloaded
pics_downloaded = 0

def load():	
	global next_page
	global counter
	global limit
	global current_page

	with open('checkpoint.txt',"r") as f:
	    lines = f.readlines()
	    current_page = lines[1].rstrip()
	    next_page = lines[3].rstrip()
	    counter = int(lines[5].rstrip())
	    limit = int(lines[7].rstrip())	

	print("Number of images to download: ",limit)
	print("Save images starting at number: ",counter)
	print("Previous URL: ",current_page)
	print("Starting URL: ",next_page)        

def checkpoint():
	global next_page
	global counter
	global limit
	global current_page

	with open('checkpoint.txt',"w") as f:
		f.write("Last Page Scraped:\n")
		f.write(f"{current_page}\n")
		f.write("Next Page to Scrape:\n")
		f.write(f"{next_page}\n")
		f.write("Photo Number\n")
		f.write(f"{counter}\n")
		f.write("How many photos to download\n")
		f.write(f"{limit}\n")


def scrape(url):
	global next_page
	global current_page
	global counter
	global limit 
	global pagecounter
	global pics_downloaded
	global urlprefix

	pagecounter += 1
	print("Beginning scrape on page: ",pagecounter)

	result = requests.get(url)

	if result.status_code == 200:
		print("URL Success...")
		soup = BeautifulSoup(result.content, "html.parser")

	#images = soup.find_all('img', {'src':re.compile('.jpg')})
	images = soup.find_all('img', {'src':re.compile('mugshot')})
	#for image in images:
	    #print(image['alt'])
	mydivs = soup.findAll("a", {"class": "next page"})
	#Finds the data to append to "mugshots.com" to reach the next page
	next_page = urlprefix + mydivs[0].get('href')
	current_page = url


	

	for image in images:
	    with open(script_dir + "/MugshotsLabeled/"+str(image['alt']).replace('/','').rstrip()+".jpg","wb") as f:
	    #with open(basename(image['src']),"wb") as f:
	        f.write(requests.get(image['src']).content)
	        counter += 1
	        #print("Counter = ",counter)
	        pics_downloaded += 1

	        if pics_downloaded >= limit:
	        	print("Images Downloaded: ",pics_downloaded)
	        	print("Creating Checkpoint...")
	        	checkpoint()
	        	return

	print("Current URL: ",url)
	print("Next Page: ",next_page)
	print("Images Downloaded : ",counter)

	print("Creating Checkpoint...")
	checkpoint()

	return scrape(next_page)



load()
scrape(next_page)

