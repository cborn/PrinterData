import flask
from flask import render_template, request, redirect
import psycopg2
from enum import Enum

app = flask.Flask(__name__)


class Column(Enum):
    TITLE = 0
    AUTHOR = 1
    DOWNLOADS = 2
    LANGUAGE = 3
    SUBJECT = 4
    LINK = 5


@app.route('/')
## Here is where we are going to need to call the script to gather the printer info.
def homepage():
    return render_template("homepage.html")
def _get_printers():
    # get the printers here, return them as a list of lists where the items are as follows:
    # model, printer_name, paperType, maxLevel, level (low/high/etc), tonerLevel, errorMessages
    printers = [["HP4500", "WCC007", "Standard", "300", "Low", "High", "N/A"]]
    return printers

@app.route('/printers')
def printer_page():
    # Call the script to get the first models' data.
    printers = _get_printers()
    return render_template('printerdata.html', printers=printers)

# Renders the advanced search page.
@app.route('/advanced')
def advanced_search():
    return render_template('advancedsearch.html')



# Intermediary URL to parse form data and redirect to advanced search page with params
@app.route('/readme')
def read_me():
    return render_template('readme.html')


@app.route('/advancedmagic', methods=['POST'])
def advanced_redirect():
    # Flask has the ability to handle requests using built in libraries.

    author = request.form['author'] # Flask has the functionality to parse the form based on it's name.
    genre = request.form['genre']
    title = request.form['title']
    url_to_append = "?"
    if author != "":
        url_to_append += "author=" + author + "&"
    if genre != "":
        url_to_append += "subject=" + genre + "&"
    if title != "":
        url_to_append += "title=" + title
    print("Url to Append: ", url_to_append)

    # Note that since Javascript wasn't working and AJAX had too much overhead,
    # we decided to finally look up and use the built in redirect system for Flask.
    return redirect('/advancedsearch/' + url_to_append)

# Intermediary URL that parses form data and redirects to popularity page with params
@app.route("/popularity", methods=['POST'])
def popularity_redirect():
    query = request.form["query"]
    return redirect('/popularity/' + query)


# Calls local function to get data based on queries, then renders page with results.
@app.route('/advancedsearch/')
def advanced_search_results():
    queries = flask.request.args
    books = []
    search_string = ""
    if queries:
        columns = queries.items()
        books = _local_advanced_search_results(columns)
        search_string = ""
        for k, v in queries.items():
            search_string += "{}: \"{}\", ".format(k, v)
        search_string = search_string[:-2]
    return render_template('searchresults.html',
                           books=books, titleIndex=Column.TITLE.value, authorIndex=Column.AUTHOR.value,
                           subjectIndex=Column.SUBJECT.value, linkIndex=Column.LINK.value, query=search_string)

# Queries the database using the queries from URL. Queries are processed in public function and passed to here.
def _local_advanced_search_results(dict_as_list):
    sql = "SELECT * FROM gutenberg WHERE ("
    for k, v in dict_as_list:
        sql += "(lower({}) LIKE '%{}%') AND".format(k.lower(), v.lower())
    sql = sql[:-4]
    sql += ") ORDER BY downloads DESC;"
    connection = connect_to_database()
    cursor = query_database(connection, sql)
    results = []
    for row in cursor:
        results.append(row)
    disconnect_database(connection)
    return results

# Query database for results using local function, render page with results.
@app.route('/popularity/<query>')
def get_books_by_popularity(query):
    books = _local_get_books_by_popularity(query)
    return render_template('searchresults.html',
                           books=books, titleIndex=Column.TITLE.value, authorIndex=Column.AUTHOR.value,
                           subjectIndex=Column.SUBJECT.value, linkIndex=Column.LINK.value, query="\"{}\"".format(query))

# Based on the query, we query each column of the table and collect all of the results in a list.
def _local_get_books_by_popularity(query):
    connection = connect_to_database()
    sql = "SELECT * FROM gutenberg WHERE ((lower(author) LIKE '%{0}%')" \
          "OR (lower(title) LIKE '%{0}%')" \
          "OR (lower(subject) LIKE '%{0}%')" \
          "OR (lower(language) LIKE '%{0}%'))" \
          "ORDER BY downloads DESC;".format(query.lower())
    cursor = query_database(connection, sql)
    results = []
    for row in cursor:
        results.append(row)
    disconnect_database(connection)
    return results



if __name__ == '__main__':
    app.run()
