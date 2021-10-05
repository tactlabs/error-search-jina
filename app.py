from flask import Flask, render_template, request
from error_search import indexing, prep_docs, search_results

app  = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template('search.html')


@app.route("/", methods=["POST"])
def search():
    query = request.values.get('query_word')
    data = search_results(flow, query)
    return render_template('search.html', data = data)

    
if __name__ == "__main__":
    docs = prep_docs(num_size = -1)
    flow = indexing(docs)
    app.run(debug = True,host="0.0.0.0")