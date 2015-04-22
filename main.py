import re
import math
from datetime import datetime

# Obtained from stack overflow: http://stackoverflow.com/questions/12164977/write-data-to-a-file-in-python
def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()
	
def get_clicks_per_minute(time_stamps):
	maximum = max(time_stamps)
	minimum = min(time_stamps)
	clicks = float(len(time_stamps))
	seconds = maximum-minimum
	minutes = seconds/60.0
	return clicks/minutes
	
def generate_minutes_map(time_map):
	for key in time_map:
		
	return


inFile = open('rmn_weblog_sample.log','r')
# Each line of the log file confirms to a slightly flexible hierarchy.
# The first entry is always an IP address, the second entry is a time stamp.
# After this, we see a mixture of tokens - usually white space delimited.
# There are large tokens which appear to have substructure - such as those
# which are sandwiched between "" - these are often subdivided with ; characters.
# 
# After the IP address and time stamp, there is usually a "GET" request of
# some kind, followed by two integers.

# Track the number of lines in the file so that we can verify the regex got everything.
line_counter = 0

# identify unique components of each line of log file. There are seven main tokens (some 
# which can be tokenized further. We use the following regular expression to match 
# each of the seven main tokens. Use raw string format to avoid plague of "\" characters.
regexp = r"((( ?\d+\. ?\d+\. ?\d+\. ?\d+,? ?|unknown),? ?)|-)+ (\S)+ (\S)+ \[(\S+\s\S+)\] (\"[^\"]*\") (\d+|-) (\d+|-) (\"[^\"]*\") (\"[^\"]*\")\n?"

# Matching the zone works, but my implementation of datetime doesn't like the 
# time zone, so I skip it
time_regexp = r"(\d+)/(\S+)/(\d+):(\d+):(\d+):(\d+) ([\+-]\d+)"
#time_regexp = r"(\d+)/(\S+)/(\d+):(\d+):(\d+):(\d+)"

get_regexp = r"GET"

get_request = "" # Any instance of get requests
date_string = "" # includes gmt offset
browser_os = "" # contains the browser / os string
view_string = "" # contains the string with the /view*/{store domain} content"
matched = 0
not_matched = 0

outFile = open('Leftovers.txt','w')

#Item 1: Get Clicks Per Minute
click_time = []
time_map = {}

for line in inFile:
	# regular expression can be used to arbitrarily match each part of every line in log file.
	line_counter+=1
	tokens = re.compile(regexp).split(line)
	# I don't care how many tokens there are, simply that my regex tokenizes the string
	# I did this by trial and error once I had a regex that matched every line in the file
	# I split it into tokens, and printed to the console. I found that it happened to 
	# produce 13 tokens, so I may now track this via hardcoding.
	if len(tokens) != 13:
		print line
		# this helped me modify my expression by catching unmatched stragglers.
		not_matched += 1
	else:
		matched+=1
	# The tokens corresponding to the data were obtained by looking at one
	date_string = tokens[6]
	get_request = tokens[7]
	view_string = tokens[10]
	browser_os = tokens[11]
	date_tokens = re.compile(time_regexp).split(date_string)
	# Tokens from date, just in case (delete to improve performance)
	time_day = date_tokens[1]
	time_month = date_tokens[2]
	time_year = date_tokens[3]
	time_hours = date_tokens[4]
	time_minutes = date_tokens[5]
	time_seconds = date_tokens[6]
	time_zone = date_tokens[7]
	# Split off Time Zone
	time_string = time_day+"/"+time_month+"/"+time_year+":"+time_hours+":"+time_minutes+":"+time_seconds
	date_obj = datetime.strptime(time_string,"%d/%b/%Y:%H:%M:%S")
	epoch_time = unix_time(date_obj)
	
	if "GET" not in get_request: continue
	epoch_int = int(epoch_time)
	
	click_time.append(epoch_time)
	if epoch_int in time_map:
		time_map[epoch_int] += 1
	else:
		time_map[epoch_time] = 1
	
# This ensures that I have accounted for every line of data.
print "There were ", matched, " lines and ", not_matched," lines.\n"
print "\total: ", matched+not_matched, "\n"
print "There were ", line_counter, " lines in the logfile.\n"
print "There were: ", len(click_time), " GET Requests\n"
print "There were: ", get_clicks_per_minute(click_time), " clicks per minute\n"
print "There were: ", len(time_map), " entries in the time_map\n"
inFile.close()
outFile.close()