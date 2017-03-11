#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, urllib2, math, collections

watchedList = "watched.txt"

def generateMovieInfos():
	result = []
	countryStats = dict()
	yearStats = dict()
	genreStats = dict()
	with open(watchedList, "rU") as f:
		for movie in f:
			watchDate, imdbId, rating = movie.strip().split(" ")
			if movie:
				print "GET movie ID " + imdbId
				response = json.load(urllib2.urlopen("http://www.omdbapi.com/?i=tt"+imdbId+"&tomatoes=true"))
				print "  -> Title: " + response["Title"].encode('utf-8')
				response["watchDate"] = watchDate
				response["personalRating"] = rating
				result.append(response)
				for country in response["Country"].split(","):
					country = country.strip()
					country = country.replace("USA", "United States")
					country = country.replace("West Germany", "Germany")
					country = country.replace("Czechoslovakia", "Czechia")
					country = country.replace("Soviet Union", "RU")
					country = country.replace("UK", "United Kingdom")
					countryStats[country] = countryStats.get(country, 0) + 1
				decade = str(int(math.floor(int(response["Year"]) / 10) * 10)) + 's'
				yearStats[decade] = yearStats.get(decade, 0) + 1
				for genre in response["Genre"].split(","):
					genre = genre.strip()
					genreStats[genre] = genreStats.get(genre, 0) + 1
	file = open("../generated/watched.json", "w")
	file.write(json.dumps(result, indent=4, separators=(',', ': ')))
	file.close()
	file = open("../generated/countryStats.json", "w")
	file.write(json.dumps(countryStats, indent=4, separators=(',', ': ')))
	file.close()
	yearStatsSorted = collections.OrderedDict(sorted(yearStats.items()))
	file = open("../generated/yearStats.json", "w")
	file.write(json.dumps(yearStatsSorted, indent=4, separators=(',', ': ')))
	file.close()
	file = open("../generated/genreStats.json", "w")
	file.write(json.dumps(genreStats, indent=4, separators=(',', ': ')))
	file.close()

def main():
	generateMovieInfos()

if __name__ == '__main__':
	main()
