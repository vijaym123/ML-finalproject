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

def getCritics(name):
	count = 0
	notDone = True
	movies = {}
	page = url.urlopen("http://www.metacritic.com/critic/" + name + "?filter=movies&page=" + str(count))
	while page:
		print count
		soupBody = BeautifulSoup(page)
		subPage=soupBody.find("ol", { "class" : "reviews critic_profile_reviews"})
		element = subPage.findChild()
		while element:
			movieID = str(element.findAll('a')[0]['href'][7:])
			if movies.has_key(movieID):
				return movies
			movies[movieID] = {}
			print movieID
			movies[movieID]["name"] = element.findAll('a')[0].text
			try :
				movies[movieID]["MetaScore"] =  int(element.findAll("span")[0].text) 
			except ValueError: 
				movies[movieID]["MetaScore"] = element.findAll("span")[0].text
			movies[movieID]["User"] = int(element.findAll("span")[2].text)
			element = element.findNextSibling()
		count+=1
		page = url.urlopen("http://www.metacritic.com/critic/" + name + "?filter=movies&page=" + str(count))
	return movies

if __name__ == "__main__":
	movieID = "tt0120689"
	print getMovieInformation(movieID)
	#print getCritics("stephen-holden")
	professionals = ["roger-ebert","mick-lasalle","joe-morgenstern","peter-travers","kyle-smith","ao-scott","lou-lumenick","lawrence-toppman",
	         "andrew-ohehir","manohla-dargis/the-new-york-times","joe-neumaier","kenneth-turan","james-berardinelli","owen-gleiberman"
	         "michael-phillips","peter-rainer/christian-science-monitor","ann-hornaday","elizabeth-weitzman/new-york-daily-news","claudia-puig",
	         "rene-rodriguez","stephen-holden","jonathan-rosenbaum","todd-mccarthy","stephen-hunter","ty-burr","michael-wilmington","david-sterritt",
	         "wesley-morris/boston-globe","elizabeth-weitzman/new-york-daily-news","steven-rea"]
	professionals = list(set(professionals))
	f = open("critic.json","w")
	for person in professionals:
		f.write(json.dumps(getCritics(person))+"\n")
	f.close()