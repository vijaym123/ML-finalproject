import json

def readMovieID(filename):
	f = open(filename,"r")
	result = dict()
	string = f.read().split('\r')
	for i in string:
		result[i.split(",")[0]] = i.split(",")[1]
	return result

def readJoeyDataSet(filename):
	f = open(filename,'r')
	string = f.read().split('\r')
	movietype = string[0].split(',')[1:]
	movieDict = dict()
	for line in string[1:]:
		movieName = line.split(',')[0]
		movieTags = line.split(',')[1:]
		for i in range(len(movietype)):
			try :
				movieDict[movieName][movietype[i]]=movieTags[i]
			except KeyError:
				movieDict[movieName]={}
				movieDict[movieName][movietype[i]]=movieTags[i]
	return movieDict

def combine(filename,movieIDs,joeyDataset):
	f = open(filename,'r')
	string = f.read().split("\r")
	count = 0
	typeOrder = "SciFi,Horror,Fantasy,Action,Romance,Documentary,Mockumentary,Campy,Outer Space,Dystopia,Funny,Slapstick,Dark,Dramatic,Mystery,Suspense,Epic,War,Past,Present,Future,Gore,Sex,Car Chase,Family,Death,Provocative,Feel Good,Animated,Raunchy,Visually Impressive,Foreign Language,Female Protagonist,Adapted from Prev Work,Musical,Real people,Independent,Politics,Sports,Dance,Animals".split(',')
	for line in string:
		count += 1
		#print count
		jsonObj = json.loads(line)
		name = jsonObj["name"]
		typeOrder.append(name)
		#print name
		jsonObj = jsonObj["critics"]
		for movie in joeyDataset.keys():
			try :
				joeyDataset[movie][name] = jsonObj[movieIDs[movie][7:]]['User']
			except KeyError:
				joeyDataset[movie][name] = ''
	f.close()
	f = open("output.csv","w")
	string = ","
	for t in typeOrder:
		string+= t + ","
	string = string + "\n"
	f.write(string)
	for movie in joeyDataset.keys():
		string = movie
		for column in typeOrder:
			string = string + str(joeyDataset[movie][column]) + ","
		string += "\n"
		f.write(string)
	f.close()

if __name__ == "__main__":
	movieIDs = readMovieID("joes-movie.csv")
	joeyDataset = readJoeyDataSet("joes.csv")
	print movieIDs
	combine("critic.json",movieIDs,joeyDataset)
