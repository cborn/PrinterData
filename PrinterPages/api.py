import flask
from flask import render_template, request, redirect
import psycopg2
from enum import Enum

app = flask.Flask(__name__)


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


if __name__ == '__main__':
    app.run()
