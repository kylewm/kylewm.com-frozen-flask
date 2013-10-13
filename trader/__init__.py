import io, os, itertools, re
from page import Page
from flask import Flask, render_template, url_for, abort

PYGMENTS_STYLE = "tango"

app = Flask(__name__)

@app.route("/article/<int:year>/<int:month>/<int:day>/<slug>/")
def article(year, month, day, slug):
    def match(page):
        date = page.date()
        return date.year == year and date.month == month \
            and date.day == day and page.slug() == slug
    page = Page.find(match)
    if page:
        return render_template("article.html", page=page)
    abort(404)

@app.route("/")
def index():
    pages = sorted(Page.all(), key=Page.date, reverse=True)
    return render_template("index.html", pages=pages)

@app.route("/css/pygments.css")
def pygments_css():
    import pygments.formatters
    pygments_css = (pygments.formatters.HtmlFormatter(style=PYGMENTS_STYLE)
                    .get_style_defs('.codehilite'))
    return app.response_class(pygments_css, mimetype='text/css')

@app.template_filter('strftime')
def _jinja2_filter_strftime(date, fmt='%Y %b %d'):
    return date.strftime(fmt) 
