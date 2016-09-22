import datetime
import re
import math 

from django.utils.html import strip_tags

def count_words(html_string):
	# html_string = 
	# """
	# 	<h1> This is a Gogolee.</h1>
	# """
	word_string = strip_tags(html_string)
	matching_words = re.findall(r'\w+', word_string)
	count = len(matching_words)
	return count

def get_read_time(html_string):
	count = count_words(html_string)
	read_time_min = math.ceil(count/200.0)	# Assuming 200 words per min...
	# read_time_sec = read_time_min * 60 #In one mins
	# read_time = str(datetime.timedelta(seconds = read_time_sec))
	#read_time = str(datetime.timedelta(minutes = read_time_min))
	return int(read_time_min)