#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import web, os, sys,  time,  re, datetime
import urllib, markdown, random

navigation = []
navigation.append(['home','/'])

urls = (
	'/show/(.*)', 'show',
	'/(.*)', 'docs',
)

path_to_docs = '/static/docs/'
	
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
	
def list_folders():
	folders = []
	for root, dirs, files in os.walk(get_script_path() + path_to_docs):
		for dir in dirs:
			folders.append(dir)
	return folders	
	
def list_docs(dir=""):
	docs = []	
	os.chdir(get_script_path())
	files =  os.listdir(get_script_path() +os.path.join(path_to_docs,dir))
	for file in files:
		if file.endswith(".txt"):
			docs.append(dir+ file)

	return docs

class docs:
	def __init__(self):
		self.render = web.template.render(get_script_path()+"/templates")
		
	def GET(self,dir=""):
		docs = list_docs(dir)
		
		#home page content
		content = 'index.txt'
		file = open(get_script_path()+'/static/'+content, 'r')		
		content = file.read()

		return self.render.show("My Bookmarks",docs,content,time.strftime("%c"),list_folders())

class show:
	def __init__(self):
		self.render = web.template.render(get_script_path()+"/templates")
		
	def GET(self,content):
		
		dir = content.split('/')[0:-1]
		try:
			dir = dir[0]+"/"
		except:
			dir=""

		docs = list_docs(dir)
		md = markdown.Markdown(output_format='html4')
		file = open(get_script_path()+'/static/docs/'+content, 'r')
		text = file.read()
		text = md.convert(text)
		t = os.path.getmtime(get_script_path()+'/static/docs/'+content)
		file.close()
		
		return self.render.show(content.split('.')[0],docs,text,"last modified: "+ str(datetime.datetime.fromtimestamp(t)),list_folders())

if __name__ == "__main__":
	os.chdir(get_script_path())
	web.config.debug = False
	app = web.application(urls, globals())
	app.run()