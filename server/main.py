import os

from flask import Flask, jsonify, request, abort
import sys
sys.path.append("/Users/tangqidong/Desktop/naive-wiki")
sys.path.append("/Users/tangqidong/Desktop/naive-wiki/data")
sys.path.append("/Users/tangqidong/Desktop/naive-wiki/rank")
from rank.query_test import query_test
from server.crawl_abstract import get_abstract
from utils.constants import permuterm, term2doc_dict


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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/search', methods=["GET"])
    def search():
        query = None
        top_k = None
        try:
            query = request.args.get("query", type=str)
            top_k = int(request.args.get("top_k", type=int, default=10))
        except:
            abort(400)
        search_res = list(query_test(query, top_k))
        print("query", query)
        print("top_k", top_k)
        print("search_res", search_res)
        return jsonify(search_res)

    @app.route('/abstract', methods=["GET"])
    def get_doc_abstract():
        doc_name = None
        try:
            doc_name = request.args.get("doc_name", type=str)
        except:
            abort(400)
        url = "https://en.wikipedia.org/wiki/" + doc_name
        return get_abstract(url=url)

    return app


if __name__ == '__main__':
    print("docs loaded:", len(permuterm), len(permuterm.keys()))
    app = create_app()
    app.run()
