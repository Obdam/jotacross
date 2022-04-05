from flask import Flask, render_template, send_from_directory
from flask_flatpages import FlatPages
from flask_frozen import Freezer

REPO_NAME = 'jotacross'
DEBUG = True
FLATPAGES_ROOT = 'articles'
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FREEZER_DESTINATION = 'docs'
FREEZER_DESTINATION_IGNORE = ['.nojekyll']
FREEZER_BASE_URL = "http://localhost/{0}".format(REPO_NAME)


app = Flask(__name__)
app.config.from_object(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)


@app.route('/')
def home():
    # Articles are pages with a publication date
    published_articles = (p for p in flatpages if 'published' in p.meta)
    # Show the 10 most recent articles, most recent first.
    latest = sorted(published_articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('home.html', articles=latest)


@app.route('/nieuws.html')
def nieuws():
    # Articles are pages with a publication date
    published_articles = (p for p in flatpages if 'published' in p.meta)
    latest = sorted(published_articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('news.html', articles=latest)

@app.route('/articles/<name>.html')
def articles(name):
    post = flatpages.get_or_404(name)
    return render_template('blog_post.html', post=post)


@app.route('/downloads/<path:filename>', methods=['GET'])
def downloads(filename):
    return send_from_directory(directory="downloads", path=filename)


if __name__ == "__main__":
    # freezer.freeze()
    # export FLASK_APP=application.py && export FLASK_ENV=development flask run
    app.run(debug=True)
