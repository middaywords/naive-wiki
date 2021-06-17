#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI - a simple web search engine.
The goal is to index an infinite list of URLs (web pages),
and then be able to quickly search relevant URLs against a query.

See https://github.com/AnthonySigogne/web-search-engine for more information.
"""

__author__ = "Anthony Sigogne"
__copyright__ = "Copyright 2017, Byprog"
__email__ = "anthony@byprog.com"
__license__ = "MIT"
__version__ = "1.0"

import os
import requests
from urllib import parse
from flask import Flask, request, jsonify, render_template
import sys 
import time
#sys.path.append("/Users/tangqidong/Desktop/naive_wiki")
from rank.query_test import query_test 

# init flask app and env variables
app = Flask(__name__)
# host = os.getenv("HOST")
# port = os.getenv("PORT")
host = '127.0.0.1'
port = '8899'

@app.route("/", methods=['GET'])
def search():
    """
    URL : /
    Query engine to find a list of relevant URLs.
    Method : POST or GET (no query)
    Form data :
        - query : the search query
        - hits : the number of hits returned by query
        - start : the start of hits
    Return a template view with the list of relevant URLs.
    """
    # GET data
    query = request.args.get("query", None)
    print("here")
    print("query is:", query)
    start = request.args.get("start", 0, type=int)
    hits = request.args.get("hits", 5, type=int)
    print("start",start)
    print("hits",hits)
    if start < 0 or hits < 0 :
        return "Error, start or hits cannot be negative numbers"

    if query :
        print("into query")
        # query search engine
        try :
            # r = requests.post('www.google.com'%(host, port), data = {
            #     'query':query,
            #     'hits':hits,
            #     'start':start
            # })
            # url = 'http://httpbin.org/post'
            # d = {'key1': 'value1', 'key2': 'value2'}
            # r = requests.post(url, data=d)
            # print(r.text) 

            #search_res = query_test(query='tencent')
            start_time = time.time()
            search_title = ['Tencent QQ#QQ_Coin', 'Tencent QQ#QQ Coin', 'Tencent_QQ#QQ_Coin',
            'Tencent Video All Star Awards', ':Category:Tencent original programming',
            ':Category:Tencent web series' ,'Tencent#Tencent Games','Tencent#Video_streaming', 
            'Tencent QQ#Q coin', 'Tencent QQ#Q_coin','11','12','13','14','15','16','17','18','19','20']
            part_search_title = search_title[start:start+hits]
            search_abstract = ['Tencent QQ#QQ_Coin', 'Tencent QQ#QQ Coin', 'Tencent_QQ#QQ_Coin',
            'Tencent Video All Star Awards', ':Category:Tencent original programming',
            ':Category:Tencent web series' ,'Tencent#Tencent Games','Tencent#Video_streaming', 
            'Tencent QQ#Q coin', 'Tencent QQ#Q_coin','11','12','13','14','15','16','17','18','19','20']
            part_search_abstract = search_abstract[start:start+hits]
            search_res = zip(part_search_title, part_search_abstract)
            end_time = time.time()
            print(search_res)
        except :
            return "Error, check your installation"
        
        # get data and compute range of results pages
        # data = r.json()
        i = int(start/hits)
        #maxi = 1+int(data["total"]/hits)
        maxi =4
        range_pages = range(i-5,i+5 if i+5 < maxi else maxi) if i >= 6 else range(0,maxi if maxi < 10 else 10)

        # show the list of matching results
        return render_template('spatial/index.html', query=query,
            response_time= round(end_time - start_time, 2),
            total=4,
            hits=hits,
            start=start,
            range_pages=range_pages,
            results=["https://www.begtut.com/python/ref-requests-post.html"]+[i for i in range(7)],
            page=i,
            search_res = search_res,
            maxpage=max(range_pages))

        # return render_template('spatial/index.html', query=query,
        #     response_time=r.elapsed.total_seconds(),
        #     total=data["total"],
        #     hits=hits,
        #     start=start,
        #     range_pages=range_pages,
        #     results=data["results"],
        #     page=i,
        #     maxpage=maxi-1)


    # return homepage (no query)
    return render_template('spatial/index.html')

@app.route("/reference", methods=['POST'])
def reference():
    """
    URL : /reference
    Request the referencing of a website.
    Method : POST
    Form data :
        - url : url to website
        - email : contact email
    Return homepage.
    """
    # POST data
    data = dict((key, request.form.get(key)) for key in request.form.keys())
    if not data.get("url", False) or not data.get("email", False) :
        return "Vous n'avez pas renseigné l'URL ou votre email."

    # query search engine
    try :
        r = requests.post('http://%s:%s/reference'%(host, port), data = {
            'url':data["url"],
            'email':data["email"]
        })
    except :
        return "Une erreur s'est produite, veuillez réessayer ultérieurement"

    return "Votre demande a bien été prise en compte et sera traitée dans les meilleurs délais."

# -- JINJA CUSTOM FILTERS -- #

@app.template_filter('truncate_title')
def truncate_title(title):
    """
    Truncate title to fit in result format.
    """
    return title if len(title) <= 70 else title[:70]+"..."

@app.template_filter('truncate_description')
def truncate_description(description):
    """
    Truncate description to fit in result format.
    """
    if len(description) <= 160 :
        return description

    cut_desc = ""
    character_counter = 0
    for i, letter in enumerate(description) :
        character_counter += 1
        if character_counter > 160 :
            if letter == ' ' :
                return cut_desc+"..."
            else :
                return cut_desc.rsplit(' ',1)[0]+"..."
        cut_desc += description[i]
    return cut_desc

@app.template_filter('truncate_url')
def truncate_url(url):
    """
    Truncate url to fit in result format.
    """
    #url = parse.unquote(url)
    url = 'https://www.begtut.com/python/ref-requests-post.html'
    if len(url) <= 60 :
        return url
    url = url[:-1] if url.endswith("/") else url
    url = url.split("//",1)[1].split("/")
    url = "%s/.../%s"%(url[0],url[-1])
    return url[:60]+"..." if len(url) > 60 else url
