#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, json, urllib.request, math, collections, operator

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
	url = "https://api.themoviedb.org/3/movie/tt" + imdbId + \
		"?api_key=" + apiKey + "&language=en-US"
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	movieInfo = json.load(response)
	time.sleep(0.25)
	return movieInfo

def getCreditsInfo(imdbId):
	url = "https://api.themoviedb.org/3/movie/tt" + imdbId + \
		"/credits?api_key=" + apiKey
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)	
	credits = json.load(response)
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
	print(" - " + decade, flush=True)
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
			if '//' in movie:
				continue
			watchDate, imdbId, rating, useEnglishTitle = movie.strip().split(" ")
			if movie:
				print(imdbId, end='', flush=True)
				movieInfo = getMovieInfo(imdbId)
				movieInfoLight = dict()			
				if useEnglishTitle == "1":
					movieInfoLight["original_title"] = movieInfo["title"]
				else:
					movieInfoLight["original_title"] = movieInfo["original_title"]	
				print("-> " + movieInfoLight["original_title"], end='', flush=True)
				getDecade(movieInfo)
				getCountry(movieInfo)
				getGenre(movieInfo)
				director = getCreditsInfo(imdbId)
				movieInfoLight["imdb_id"] = movieInfo["imdb_id"]					
				movieInfoLight["release_date"] = movieInfo["release_date"][0:4]
				#movieInfoLight["vote_average"] = movieInfo["vote_average"]
				movieInfoLight["watchDate"] = watchDate
				movieInfoLight["personalRating"] = rating
				movieInfoLight["runtime"] = movieInfo["runtime"]
				movieInfoLight["poster_path"] = movieInfo["poster_path"]
				movieInfoLight["director"] = director.strip()
				movieInfos.append(movieInfoLight)

	jsonResult["countries"] = countryList

	decadeListSorted = collections.OrderedDict(sorted(decadeList.items()))
	jsonResult["decades"] = decadeListSorted

	genreListSorted = sorted(genreList.items(), key=operator.itemgetter(1), reverse=True)
	jsonResult["genres"] = collections.OrderedDict(genreListSorted)

	actorListSorted = sorted(actorList.items(), key=lambda x: x[1].get('count'), reverse=True)
	jsonResult["actors"] = actorListSorted[0:10]

	directorListSorted = sorted(directorList.items(), key=lambda x: x[1].get('count'), reverse=True)
	jsonResult["directors"] = directorListSorted

	cameraListSorted = sorted(cameraList.items(), key=lambda x: x[1].get('count'), reverse=True)
	jsonResult["cinematographers"] = cameraListSorted[0:10]

	jsonResult["movies"] = movieInfos
	file = open(exportFile, "w")
	file.write(json.dumps(jsonResult, indent=4, separators=(',', ': ')))
	file.close()

def main():
	generateMovieInfos()

if __name__ == '__main__':
	main()
