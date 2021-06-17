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
import threading

from rank.query_test import query_test
from server.crawl_abstract import get_abstracts, get_urls
from utils.constants import permuterm, term2doc_dict

print("docs loaded:", len(permuterm), len(permuterm.keys()))
previous_search_res = None
abstract_Flag = True
previous_search_res_abs = []
search_res = None
search_titles = None
previous_query = None
current_start = 0
current_hits = 5
previous_search_time = 0



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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
        global previous_search_res, previous_search_res_abs, search_res, previous_query, search_titles
        global current_start, current_hits, previous_search_time, update_page_Flag, abstract_Flag
        # GET data
        query = request.args.get("query", None)
        top_k = int(request.args.get("top_k", type=int, default=20))
        doc_name = request.args.get("doc_name", type=str, default=None)
        print("query is:", query)
        start = request.args.get("start", 0, type=int)
        hits = request.args.get("hits", 5, type=int)
        print("start", start)
        print("hits", hits)
        if start < 0 or hits < 0:
            return "Error, start or hits cannot be negative numbers"
        if previous_query != query:
            update_page_Flag = True
        if previous_query != query or start != current_start:
            abstract_Flag = True

        if query:
            try:
                if previous_search_res is not None and previous_query == query:
                    search_time = previous_search_time
                    search_res = list(previous_search_res)[start:start + hits]
                else:
                    start_time = time.time()

                    search_titles = list(query_test(query, top_k))
                    if len(search_titles) < top_k:
                        top_k = len(search_titles)
                    search_titles = search_titles[:top_k]
                    urls = get_urls(doc_names=search_titles)
                    end_time = time.time()
                    search_abstracts = [''] * top_k
                    previous_search_res = list(zip(search_titles, search_abstracts, urls))
                    previous_search_res_abs = previous_search_res.copy()
                    search_res = previous_search_res[start:start + hits]

                    search_time = round(end_time - start_time, 2)
                    previous_search_time = search_time
                    print("search first over")
                    t1 = threading.Thread(target=update_page)
                    t1.start()
                    update_page_Flag = False

            except:
                return "Error, check your installastion"

            # get data and compute range of results pages
            i = int(start / hits)
            maxi = 4
            range_pages = range(i - 5, i + 5 if i + 5 < maxi else maxi) if i >= 6 else range(0,
                                                                                             maxi if maxi < 10 else 10)

            # show the list of matching results
            previous_query = query
            current_start, current_hits = start, hits
            return render_template('spatial/index.html', query=query,
                                   response_time=search_time,
                                   total=top_k,
                                   hits=hits,
                                   start=start,
                                   range_pages=range_pages,
                                   page=i,
                                   search_res=search_res,
                                   maxpage=max(range_pages))

        # return homepage (no query)
        return render_template('spatial/index.html')

    def update_page():
        if not update_page_Flag:
            return
        global search_titles, previous_search_res_abs
        search_abstracts = get_abstracts(doc_names=search_titles[0:5])
        urls = get_urls(doc_names=search_titles)
        # previous_search_res_abs = list(zip(search_titles[0:5], search_abstracts, urls)) + previous_search_res[5:]
        previous_search_res_abs[0:5] = list(zip(search_titles[0:5], search_abstracts, urls))
        print("First layer of Abstracts have been obtained")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        search_abstracts_2layer = get_abstracts(doc_names=search_titles[5:10])
        urls_2layer = get_urls(doc_names=search_titles)
        previous_search_res_abs[5:10] = list(zip(search_titles[5:10], search_abstracts_2layer, urls_2layer))
        print("Second layer of Abstracts have been obtained")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        search_abstracts_3layer = get_abstracts(doc_names=search_titles[10:15])
        urls_2layer = get_urls(doc_names=search_titles)
        previous_search_res_abs[10:15] = list(zip(search_titles[10:15], search_abstracts_2layer, urls_2layer))
        print("Third layer of Abstracts have been obtained")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        search_abstracts_4layer = get_abstracts(doc_names=search_titles[15:20])
        urls_2layer = get_urls(doc_names=search_titles)
        previous_search_res_abs[15:20] = list(zip(search_titles[15:20], search_abstracts_2layer, urls_2layer))
        print("Fourth layer of Abstracts have been obtained")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # search_abstracts = get_abstracts(doc_names=search_titles)
        # urls = get_urls(doc_names=search_titles)
        # previous_search_res_abs = list(zip(search_titles, search_abstracts, urls))
        # print("Abstracts have been obtained")
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    @app.route("/", methods=['POST'])
    def abstract():
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
        global abstract_Flag, previous_search_res_abs, previous_search_res, previous_search_time, previous_query
        global current_start, current_hits
        # GET data
        print("into abstract function")
        query = request.args.get("query", None)
        top_k = int(request.args.get("top_k", type=int, default=20))
        doc_name = request.args.get("doc_name", type=str, default=None)
        start = current_start
        hits = current_hits
        print("start", start)
        print("hits", hits)
        if start < 0 or hits < 0:
            return "Error, start or hits cannot be negative numbers"

        try:
            print("abstract_Flag", abstract_Flag)
            search_time = previous_search_time
            if abstract_Flag:
                search_res = list(previous_search_res_abs)[start:start + hits]

            else:
                search_res = list(previous_search_res)[start:start + hits]
            abstract_Flag = not abstract_Flag


        except:
            return "Error, check your installation"

        # get data and compute range of results pages
        i = int(start / hits)
        maxi = 4
        range_pages = range(i - 5, i + 5 if i + 5 < maxi else maxi) if i >= 6 else range(0, maxi if maxi < 10 else 10)

        # show the list of matching results
        return render_template('spatial/index.html', query=previous_query,
                               response_time=previous_search_time,
                               total=top_k,
                               hits=hits,
                               start=start,
                               range_pages=range_pages,
                               page=i,
                               search_res=search_res,
                               maxpage=max(range_pages))

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
        if not data.get("url", False) or not data.get("email", False):
            return "Vous n'avez pas renseigné l'URL ou votre email."

        # query search engine
        try:
            r = requests.post('http://%s:%s/reference' % (host, port), data={
                'url': data["url"],
                'email': data["email"]
            })
        except:
            return "Une erreur s'est produite, veuillez réessayer ultérieurement"

        return "Votre demande a bien été prise en compte et sera traitée dans les meilleurs délais."

    # -- JINJA CUSTOM FILTERS -- #

    @app.template_filter('truncate_title')
    def truncate_title(title):
        """
        Truncate title to fit in result format.
        """
        return title if len(title) <= 70 else title[:70] + "..."

    @app.template_filter('truncate_description')
    def truncate_description(description):
        """
        Truncate description to fit in result format.
        """
        if len(description) <= 160:
            return description

        cut_desc = ""
        character_counter = 0
        for i, letter in enumerate(description):
            character_counter += 1
            if character_counter > 160:
                if letter == ' ':
                    return cut_desc + "..."
                else:
                    return cut_desc.rsplit(' ', 1)[0] + "..."
            cut_desc += description[i]
        return cut_desc

    @app.template_filter('truncate_url')
    def truncate_url(url):
        """
        Truncate url to fit in result format.
        """
        # url = parse.unquote(url)
        url = 'https://www.begtut.com/python/ref-requests-post.html'
        if len(url) <= 60:
            return url
        url = url[:-1] if url.endswith("/") else url
        url = url.split("//", 1)[1].split("/")
        url = "%s/.../%s" % (url[0], url[-1])
        return url[:60] + "..." if len(url) > 60 else url

    return app


if __name__ == '__main__':
    print("docs loaded:", len(permuterm), len(permuterm.keys()))
    app = create_app()
    app.run()
