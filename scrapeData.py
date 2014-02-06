import urllib2 as url
from BeautifulSoup import BeautifulSoup
import sys
import json

def getKeywords(movieID):
	page = url.urlopen("http://www.imdb.com/title/"+movieID+"/keywords") 
	soupBody = BeautifulSoup(page)
	keywords = [str(link.getText()) for link in soupBody.findAll('a') if link.get('href').startswith("/keyword/")]
	return keywords

def getMovieInformation(movieID):
	page = url.urlopen("http://www.omdbapi.com/?i="+movieID)
	jsonObj = json.loads(page.read())
	jsonObj['keywords'] = getKeywords(movieID)
	return jsonObj

if __name__ == "__main__":
	movieID = "tt0120689"
	print getMovieInformation(movieID)