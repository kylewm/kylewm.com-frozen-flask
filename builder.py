import io, os, itertools, re
import markdown
import toml
from flask import Flask, render_template, url_for, abort

PAGE_EXTENSION = ".md"
PYGMENTS_STYLE = "tango"

class Page():
    _pages = None
    md = markdown.Markdown(['codehilite'])
    page_regex = re.compile(r'---(?P<head>.*?)---(?P<body>.*)', re.DOTALL | re.MULTILINE)
    file_regex = re.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<slug>.*)')
    
    @classmethod
    def load(cls, filename):
        with io.open(filename, encoding='utf8') as fd:
            filetext = fd.read()
            match = cls.page_regex.match(filetext)
            if match:
                head = match.group('head')
                body = match.group('body')
                return cls(filename, head, body)
        
    @classmethod
    def all(cls):
        if not cls._pages: 
            cls._pages = []
            for root, dirs, files in os.walk("content"):
                for name in files:
                    basename, ext = os.path.splitext(name)
                    if ext == PAGE_EXTENSION:
                        page = Page.load(os.path.join(root, name))
                        if page:
                            cls._pages.append(page)
        return cls._pages

    @classmethod
    def find(cls, pred):
        return next((page for page in cls.all() if pred(page)), None)

    def __init__(self, filename, head, body):
        self.filename = filename
        self.head = head
        self.body = body
        self._meta = None

    def meta(self):
        if not self._meta:
            self._meta = toml.loads(self.head)
        return self._meta

    def html(self):
        return self.md.convert(self.body)

    def _filename_base(self):
        path, name = os.path.split(self.filename)
        base, ext = os.path.splitext(name)
        return base

    def date(self):
        date = self.meta().get('date')
        if date:
            return date
        m = self.file_regex.match(self._filename_base())
        if m:
            year = m.group('year')
            month = m.group('month')
            day = m.group('day')
            return datetime.date(int(year), int(month), int(day))
        raise ValueError("Could not parse date from filename {}".format(self.filename))

    def slug(self):
        slug = self.meta().get('slug')
        if slug: 
            return slug
        m = self.file_regex.match(self._filename_base())
        if m:
            return m.group('slug')
        raise ValueError("Could not parse filename {}".format(self.filename))

    def url(self):
        date = self.date()
        return url_for('article', year=date.year, month=date.month,
                       day=date.day, slug=self.slug())
    
    def __getitem__(self, name):
        return self.meta()[name]

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

@app.route("/css/style.css")
def style_css():
    import pygments.formatters
    pygments_css = (pygments.formatters.HtmlFormatter(style=PYGMENTS_STYLE)
                    .get_style_defs('.codehilite'))

    css = render_template('style.css', pygments=pygments_css)
    return app.response_class(css, mimetype='text/css')

@app.route("/css/pygments.css")
def pygments():
    import pygments.formatters
    formatter = pygments.formatters.HtmlFormatter(style=PYGMENTS_STYLE)
    pygments_css = formatter.get_style_defs('.codehilite')
    return app.response_class(pygments_css, mimetype='text/css')

@app.template_filter('strftime')
def _jinja2_filter_strftime(date, fmt=None):
    return date.strftime(fmt or '%Y %b %d') 

if __name__ == "__main__":
    app.run(port=8000, debug=True)
