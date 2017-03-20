#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, json, urllib2, math, collections

watchedList = "watched.txt"

def getTheMovieDBApiKey():
	with open("../private/themoviedb.apikey", "rU") as f:
		for line in f:
			apiKey = line
	return apiKey

def generateMovieInfos():
	apiKey = getTheMovieDBApiKey()
	result = []
	countryStats = dict()
	yearStats = dict()
	genreStats = dict()
	with open(watchedList, "rU") as f:
		for movie in f:
			watchDate, imdbId, rating = movie.strip().split(" ")
			if movie:
				print "GET movie ID " + imdbId,
				url = "https://api.themoviedb.org/3/movie/tt" + imdbId + "?api_key=" + apiKey + "&language=en-US"
				response = json.load(urllib2.urlopen(url))
				print "-> " + response["original_title"].encode('utf-8'),
				response["watchDate"] = watchDate
				response["personalRating"] = rating
				result.append(response)				
				decade = str(int(math.floor(int(response["release_date"][0:4]) / 10) * 10)) + 's'
				print " - " + decade
				yearStats[decade] = yearStats.get(decade, 0) + 1
				for country in response["production_countries"]:
					countryISO = country["iso_3166_1"]
					countryISO = countryISO.replace("SU", "RU")
					countryStats[countryISO] = countryStats.get(countryISO, 0) + 1
				for genre in response["genres"]:
					genreName = genre["name"]
					genreStats[genreName] = genreStats.get(genreName, 0) + 1
				sys.stdout.flush()
				time.sleep(0.3)
	file = open("../js/watched.json", "w")
	file.write(json.dumps(result, indent=4, separators=(',', ': ')))
	file.close()
	file = open("../js/countryStats.json", "w")
	file.write(json.dumps(countryStats, indent=4, separators=(',', ': ')))
	file.close()
	yearStatsSorted = collections.OrderedDict(sorted(yearStats.items()))
	file = open("../js/yearStats.json", "w")
	file.write(json.dumps(yearStatsSorted, indent=4, separators=(',', ': ')))
	file.close()
	file = open("../js/genreStats.json", "w")
	file.write(json.dumps(genreStats, indent=4, separators=(',', ': ')))
	file.close()

def main():
	generateMovieInfos()

if __name__ == '__main__':
	main()
