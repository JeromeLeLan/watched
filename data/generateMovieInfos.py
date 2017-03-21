#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, json, urllib2, math, collections, operator

apiFile = "../private/themoviedb.apikey"

def getTheMovieDBApiKey():
	with open(apiFile, "rU") as f:
		for line in f:
			apiKey = line
	return apiKey

apiKey = getTheMovieDBApiKey()

watchedFile = "watched.txt"
#watchedFile = "watchedSample.txt" # debug
exportFile = "../js/watched.json"

movieInfos = []
countryList = dict()
decadeList = dict()
genreList = dict()
actorList = dict()
directorList = dict()
cameraList = dict()
jsonResult = dict()

def addItemToDict(vDict, key, value, valueType):
	if not key in vDict:
		vDict[key] = dict()
		vDict[key]["count"] = 0
		vDict[key][valueType] = value
	vDict[key]["count"] = vDict[key]["count"] + 1

def getMovieInfo(imdbId):
	print imdbId,
	url = "https://api.themoviedb.org/3/movie/tt" + imdbId + \
		"?api_key=" + apiKey + "&language=en-US"
	movieInfo = json.load(urllib2.urlopen(url))
	time.sleep(0.25)
	print "-> " + movieInfo["original_title"].encode('utf-8'),
	return movieInfo

def getCreditsInfo(imdbId):
	url = "https://api.themoviedb.org/3/movie/tt" + imdbId + \
		"/credits?api_key=" + apiKey
	credits = json.load(urllib2.urlopen(url))
	time.sleep(0.25)
	director = ""
	for cast in credits["cast"]:
		addItemToDict(actorList, cast["id"], cast["name"], "name")
	for crew in credits["crew"]:
		if crew["job"] == "Director":
			director += crew["name"] + ", "
			addItemToDict(directorList, crew["id"], crew["name"], "name")
		if crew["job"] == "Director of Photography":
			addItemToDict(cameraList, crew["id"], crew["name"], "name")
	return director[0:len(director)-2]

def getDecade(movieInfo):
	decade = str(int(math.floor(int(movieInfo["release_date"][0:4]) / 10) * 10)) + 's'
	print "- " + decade
	decadeList[decade] = decadeList.get(decade, 0) + 1

def getCountry(movieInfo):
	for country in movieInfo["production_countries"]:
		countryISO = country["iso_3166_1"].replace("SU", "RU")
		countryName = country["name"].replace("Soviet Union", "Russia")
		addItemToDict(countryList, countryISO, countryName, "name")

def getGenre(movieInfo):
	for genre in movieInfo["genres"]:
		genreName = genre["name"]
		genreList[genreName] = genreList.get(genreName, 0) + 1

def generateMovieInfos():
	with open(watchedFile, "rU") as f:
		for movie in f:
			watchDate, imdbId, rating = movie.strip().split(" ")
			if movie:
				movieInfo = getMovieInfo(imdbId)
				movieInfo["watchDate"] = watchDate
				movieInfo["personalRating"] = rating
				getDecade(movieInfo)
				getCountry(movieInfo)
				getGenre(movieInfo)
				director = getCreditsInfo(imdbId)
				movieInfo["director"] = director
				movieInfos.append(movieInfo)
				sys.stdout.flush()

	jsonResult["countries"] = countryList

	decadeListSorted = collections.OrderedDict(sorted(decadeList.items()))
	jsonResult["decades"] = decadeListSorted

	genreListSorted = sorted(genreList.items(), key=operator.itemgetter(1), reverse=True)
	jsonResult["genres"] = collections.OrderedDict(genreListSorted)

	actorListSorted = sorted(actorList.items(), key=operator.itemgetter(1), reverse=True)
	jsonResult["actors"] = actorListSorted[0:10]

	directorListSorted = sorted(directorList.items(), key=operator.itemgetter(1), reverse=True)
	jsonResult["directors"] = directorListSorted

	cameraListSorted = sorted(cameraList.items(), key=operator.itemgetter(1), reverse=True)
	jsonResult["cinematographers"] = cameraListSorted[0:10]

	jsonResult["movies"] = movieInfos
	file = open(exportFile, "w")
	file.write(json.dumps(jsonResult, indent=4, separators=(',', ': ')))
	file.close()

def main():
	generateMovieInfos()

if __name__ == '__main__':
	main()
