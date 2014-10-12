# import the necessary modules
import requests # easy REST for python 
from pattern import web # perfect module for scraping the web 
import pandas as pd  # the pandas data handling module 

# this script at its current form works only for imdb. 
# when you understand the logic you can use for any website you want. 

# The first function creates a list with the urls for the movies from a page
# where the movies that received the most votes are 
# a much more elegant and easy solution would be to tease the &start= parameters in the url and imcrement by 51 but 
# this is tutorial for web scraping so we will go the long way

def get_links_from_page(number_of_pages): 
	# get initial url 
	url = web.URL('http://www.imdb.com/search/title?sort=num_votes,desc&start=1&title_type=feature&year=1990,2012')
	# create an empty array to populate with the urls 
	pages = []
	# the loop to get the links 
	for page_index in range(number_of_pages): 
		if page_index == 0: # the first page has only next button so the DOM is different
			dom = web.DOM(url.download(cached = False))
			# to see which part of the DOM to use right click in Chrome 
			# and use 'Inspect Element'
			entry = dom('span.pagination')[1].by_tag('a')
			href = 'http://www.imdb.com/' + entry[0].attributes.get('href')
			pages.append(href)
			print(pages)
			url = web.URL(href)
		else:  # after the first page you have both previous and next butoon so you select next 
			dom = web.DOM(url.download(cached = False))
			entry = dom('span.pagination')[1].by_tag('a')
			href = 'http://www.imdb.com/' + entry[1].attributes.get('href')
			pages.append(href)
			print(pages)
			url = web.URL(href)
	# return a list that handles empty urls
	return list(set(pages))



# you then create a function that gets the data you need from every url you scraped above
def get_data_from_pages(links): 
	# open an empty array 
	data = []
	#create the loop to get the links that you created from the previous function
	for urltext in links: 
		#parse the url 
		url = web.URL(urltext)
		# print them for "matrix" like effect (slower, comment this line if you do not want it)
		print "Getting data from: ", url 
		try:  # the main scraping loop, it all about DOM manipulation 
			# learn more about DOM at http://code.tutsplus.com/tutorials/javascript-and-the-dom-series-lesson-1--net-3134 
			dom = web.DOM(url.download(cached=False))
			for movie in dom.by_tag('td.title'):
				title = movie.by_tag('a')[0].content
				print title
				genres = movie.by_tag('span.genre')[0].by_tag('a')
				genres = [g.content for g in genres]
				print genres
				director = movie.by_tag('span.credit')[0].by_tag('a')[0].content
				print director
				first_actor = movie.by_tag('span.credit')[0].by_tag('a')[1].content
				print first_actor
				second_actor = movie.by_tag('span.credit')[0].by_tag('a')[2].content
				print second_actor
				runtime = movie.by_tag('span.runtime')[0].content
				print runtime
				rating = movie.by_tag('span.value')[0].content
				print rating
				data.append((title, genres, director, first_actor, second_actor, runtime, rating))	
		except KeyboardInterrupt:
			break # to be able to interrupt the Ctrl+c without losing the data
		except: 
			pass # to not stop in case of missing data 
	return data

# use the following commands to create a dataframe from your scraped data
	#titles, genres, directors, first_actors, second_actors, runtimes, ratings =zip(*data) # this is very beatiful python command to unpack your data into separate lists
	#data = pd.DataFrame({'title': titles, 'genres': genres, 'director':directors, 'first_actor':first_actors, 'second_actor':second_actors, 'runtime': runtimes, 'rating': ratings})
	#print data

	# now the real work as a data scientist starts!!! 
	#Load your weapons for DATA MUNGING.......
#		---------					----------
#     ̿ ̿̿ ̿’̿’̵͇̿̿з=(◣_◢)=ε/̵͇̿̿/’̿’̿ ̿ ̿̿﻿ ̿̿ ̿̿



	

