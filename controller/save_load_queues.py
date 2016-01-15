"""
Steven Jenny
smj2mm@virginia.edu
1-15-2016

This file is used to test a save and load function. These functions are intended to be used in the
scenery robot designed in DRAMA 4598 to save queues of recorded encoder ticks and load them for
playback. The file takes an argument of a text file which will be written to and then loaded from.
Some of the code was included from online python tutorials.
"""
from sys import argv

script, my_filename = argv

print "We're going to rewrite (erase) %r." % my_filename
print "If you don't want that, hit CTRL-C (^C)."
print "If you do want that, hit RETURN."

raw_input("?")

target = open(my_filename, 'w')
target.truncate()

this_queue = [[1,2], [2,3], [3,4]]

def save_new_queue(filename, queue_to_save, queuename="UNTITLED"):
	"""
	This function will open a file and append to it a new queue with a title and data.
	@params: filename: the save file (text file where info will be stored)
		list_to_save: the data of the new queue being saved
		listname: the name of the queue being saved as a list
	"""
	target = open(filename, 'a+')
	target.write(queuename)
	for i in range(0, len(queue_to_save)):
		target.write("\n")
		target.write(str(queue_to_save[i]))
	target.write("\n"), target.write("\n")
	target.close()	

def load_queue_file(filename):
	"""
	This function first reads in an entire list, line by line. It then creates a list of lists where
	each list contains all the points in a list
	@params: filename: the file to be loaded
	"""
	loaded_lines = [["start"]]
	with open(filename) as f:
		lines = f.readlines()
	
	j=0
	for i in range(0,len(lines)):
		loaded_lines[j].append(lines[i])
	    	if lines[i] == '\n':
	    		loaded_lines.append([])
	    		j+=1
    	return loaded_lines		
	
save_new_queue(my_filename, this_queue, "queue1")
save_new_queue(my_filename, this_queue, "queue2")
save_new_queue(my_filename, this_queue, "queue3")
load_queue_file(my_filename)
print "file written!\n"