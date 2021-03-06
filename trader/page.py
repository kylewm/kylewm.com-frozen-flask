import io, os, itertools, re
import markdown
import toml
from flask import url_for

PAGE_EXTENSION = ".md"

class Page():
    md = markdown.Markdown(['codehilite'])
    page_regex = re.compile(r'---(?P<head>.*?)---(?P<body>.*)', re.DOTALL | re.MULTILINE)
    file_regex = re.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<slug>.*)')
    resource_regex = re.compile(r'resource:(?P<name>[a-zA-Z0-9\-_.%]*)')
    
    @classmethod
    def load(cls, filename, resourcepath):
        with io.open(filename, encoding='utf8') as fd:
            filetext = fd.read()
            match = cls.page_regex.match(filetext)
            if match:
                head = match.group('head')
                body = match.group('body')
                resourcepath = os.path.abspath(resourcepath)
                return cls(filename, resourcepath, head, body)
        
    @classmethod
    def all(cls):
        pages = []
        for root, dirs, files in os.walk("content"):
            for name in files:
                basename, ext = os.path.splitext(name)
                if ext == PAGE_EXTENSION:
                    page = Page.load(os.path.join(root, name), 
                                     os.path.join(root, basename))
                    if page:
                        pages.append(page)            
        return pages

    @classmethod
    def find(cls, pred):
        return next((page for page in cls.all() if pred(page)), None)

    def __init__(self, filename, resourcepath, head, body):
        self.filename = filename
        self.resourcepath = resourcepath
        self.head = head
        self.body = body
        self._meta = None

    def meta(self):
        if not self._meta:
            self._meta = toml.loads(self.head)
        return self._meta

    def html(self):
        date = self.date()

        def repl(matcher):
            return url_for('article_resource', year=date.year,
                           month=date.month, day=date.day,
                           slug=self.slug(), resource=matcher.group('name'))
        
        processed = self.resource_regex.sub(repl, self.body)
            
            
        return self.md.convert(processed)

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
