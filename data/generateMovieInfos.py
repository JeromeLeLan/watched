#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, json, urllib2, math, collections

apiFile = "../private/themoviedb.apikey"
watchedFile = "watched.txt"
#watchedFile = "watchedSample.txt" // debug
exportFile = "../js/watched.json"

def getTheMovieDBApiKey():
	with open(apiFile, "rU") as f:
		for line in f:
			apiKey = line
	return apiKey

def generateMovieInfos():
	apiKey = getTheMovieDBApiKey()
	movieInfos = []
	countryStats = dict()
	decadeStats = dict()
	genreStats = dict()
	jsonResult = dict()
	with open(watchedFile, "rU") as f:
		for movie in f:
			watchDate, imdbId, rating = movie.strip().split(" ")
			if movie:
				print imdbId,
				url = "https://api.themoviedb.org/3/movie/tt" + imdbId + "?api_key=" + apiKey + "&language=en-US"
				response = json.load(urllib2.urlopen(url))
				print "-> " + response["original_title"].encode('utf-8'),
				response["watchDate"] = watchDate
				response["personalRating"] = rating
				movieInfos.append(response)
				decade = str(int(math.floor(int(response["release_date"][0:4]) / 10) * 10)) + 's'
				print "- " + decade
				decadeStats[decade] = decadeStats.get(decade, 0) + 1
				for country in response["production_countries"]:
					countryISO = country["iso_3166_1"]
					countryISO = countryISO.replace("SU", "RU")
					countryStats[countryISO] = countryStats.get(countryISO, 0) + 1
				for genre in response["genres"]:
					genreName = genre["name"]
					genreStats[genreName] = genreStats.get(genreName, 0) + 1
				sys.stdout.flush()
				time.sleep(0.3)
	jsonResult["countries"] = countryStats
	decadeStatsSorted = collections.OrderedDict(sorted(decadeStats.items()))
	jsonResult["decades"] = decadeStatsSorted
	jsonResult["genres"] = genreStats
	jsonResult["movies"] = movieInfos
	file = open(exportFile, "w")
	file.write(json.dumps(jsonResult, indent=4, separators=(',', ': ')))
	file.close()

def main():
	generateMovieInfos()

if __name__ == '__main__':
	main()
