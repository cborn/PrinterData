#!/usr/bin/python

import xml.etree.ElementTree
import csv
import os
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
""" Since our data was in XML format with specific namespaces designed for Project Gutenberg,
	we had to write a script to manually go through the XML tree and parse the data. This turned out
	to be a pain in the butt, but after drawing out the paths we got there.
"""

""" This function takes a parent node and a 'key', which corresponds to the name of the node in the XML tree.
	Given that node and the key, it returns the child that corresponds to the key."""

def get_child(parent, key_to_find):
	if parent == None:
		return None
	for child in parent:
		if key_to_find in child.tag:
			return child
	return None


""" This function acts as the function to recursively go down the XML tree based on a list of keys. These
    keys were ones that we figured out manually based on looking at a few files and are apparently not
    consistent across all .rdf files. Once we get the node corresponding to the last key, we return that node.
"""

def get_descendent(parent, list_of_keys):
	for i in range(0, len(list_of_keys)):
		parent = get_child(parent, list_of_keys[i])
		
	return parent

""" For each category of data we want (title, author, downloads, subject, language), we call our above functions
    to get the node the contains that data. We then use the .text function of the XML tree object to get the data.
    Once we have all of the data, we generate the link corresponding to each book, and then return a list of the data.
"""

def collect_info(filename):
	root = xml.etree.ElementTree.parse(filename).getroot()
	title = get_descendent(root[0], ["title"])
	if title is not None:
		title = title.text
	else:
		title = ""
	author = get_descendent(root[0], ["creator", "agent", "name"])
	if author is not None:
		author = author.text
	else:
		author = ""
	downloads = get_descendent(root[0], [ "downloads"])
	if downloads is not None: 
		downloads = int(downloads.text)
	else:
		downloads = 0
	subject = get_descendent(root[0], ["subject", "Description", "value"])
	if subject is not None:
		subject = subject.text
	else:
		subject = ""
	language = get_descendent(root[0], ["language", "Description", "value"])
	if language is not None:
		language = language.text
	else:
		language = ""

	link = "https://www.gutenberg.org/ebooks/"
	book_page = filename.split("pg")[1]
	book_page = book_page.split(".rdf")[0]
	link = link + book_page
	data = [title, author, downloads, language, subject, link]
	return data


# We utilize Python's csv library to easily write our data to a csv file.
def make_csv(data):
	with open("data.csv", "a", encoding = "utf-8") as f:
		writer = csv.writer(f)
		for char in data:
			if type(char) != int:
				char.encode("utf-8")
		writer.writerow(data)

def main():
	for filename in os.listdir("./"):
		if not ".rdf" in filename or "pg0" in filename:
			continue
		data = collect_info(filename)
		make_csv(data)

if __name__ == '__main__':
	main()
