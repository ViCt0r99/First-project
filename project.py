from _datetime import datetime

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from forms import BookAddingForm
import json
import requests
from sqlalchemy import exc
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
url = 'https://www.googleapis.com/books/v1/volumes?q='

class BooksList(db.Model):
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    published_date = db.Column(db.String)
    ISBN = db.Column(db.String, primary_key=True)
    page_count = db.Column(db.String)
    url_thumbnail = db.Column(db.String)
    language = db.Column(db.String(200))
    added_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<ISBN %r>' % self.ISBN


@app.route('/', methods=['POST', 'GET'])
def welcome():
    books = BooksList.query.order_by(BooksList.added_time).all()
    return render_template('welcome.html', books=books)


@app.route('/adding', methods=['GET', 'POST'])
def adding():
    form = BookAddingForm()
    if form.validate_on_submit():
            print("Działa!")
            new_book = BooksList(
                title=request.form['Title'],
                author=request.form['Author'],
                published_date=request.form['PublishedDate'],
                ISBN=request.form['ISBN'],
                page_count=request.form['PageCount'],
                url_thumbnail=request.form['Url_thumbnail'],
                language=request.form['Language']
            )
            try:
                db.session.add(new_book)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your book'

    return render_template(
        'book_adding2.html',
        form=form
        )


@app.route('/edit/<string:ISBN>', methods=['GET', 'POST'])
def edit_book(ISBN):
    book = BooksList.query.get_or_404(ISBN)
    form = BookAddingForm()
    if request.method == 'POST' and form.validate():
        book.title = request.form['Title']
        book.author = request.form['Author']
        book.published_date = request.form['PublishedDate']
        book.ISBN = request.form['ISBN']
        book.page_count = request.form['PageCount']
        book.language = request.form['Language']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue editing your book'
    else:
        return render_template(
            'edit_book.html',
            form=form,
            book=book
        )

@app.route('/import')
def import_API():
    return render_template('import_page.html')


@app.route('/import_by_title', methods=['GET', 'POST'])
def import_by_title():
    if request.method == 'POST':
        title_search = request.form['title']
        response = requests.get(url + 'intitle:' + title_search)
        obj = json.loads(response.text)
        w = obj['items']
        for item in w:
            author_tab = []
            i = 0
            author1 = item['volumeInfo'].get('authors', 'None')
            url_import = item['volumeInfo'].get('imageLinks', 'None')
            if url_import != 'None':
                url_import = item['volumeInfo']['imageLinks'].get('thumbnail', 'None')
            if author1 != 'None':
                for author in item['volumeInfo']['authors']:
                    author_tab.append(author)
                while i < len(author_tab):
                    if i == 0:
                        author1 = author_tab[i]
                    else:
                        author1 = author1 + ', ' + author_tab[i]
                    i += 1
            ISBN = item['volumeInfo'].get('industryIdentifiers', 'None')
            if ISBN != 'None':
                for number in item['volumeInfo']['industryIdentifiers']:
                    if number['type'] == 'ISBN_13' or number['type'] == 'OTHER':
                        ISBN = number['identifier']
                    else:
                        continue
            new_book = BooksList(
                title=item['volumeInfo'].get('title', 'None'),
                author=author1,
                published_date=item['volumeInfo'].get('publishedDate', 0),
                ISBN=ISBN,
                page_count=item['volumeInfo'].get('pageCount', 0),
                url_thumbnail=url_import,
                language=item['volumeInfo']['language']
            )
            try:
                db.session.add(new_book)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                print(e)
                return 'There was an issue adding your book'
        return redirect('/')
    else:
        return render_template('import_page_by_title.html')


@app.route('/import_by_author', methods=['GET', 'POST'])
def import_by_author():
    if request.method == 'POST':
        author_search = request.form['author']
        response = requests.get(url + 'inauthor:' + author_search)
        obj = json.loads(response.text)
        w = obj['items']
        for item in w:
            author_tab = []
            i = 0
            author1 = item['volumeInfo'].get('authors', 'None')
            url_import = item['volumeInfo'].get('imageLinks', 'None')
            if url_import != 'None':
                url_import = item['volumeInfo']['imageLinks'].get('thumbnail', 'None')
            if author1 != 'None':
                for author in item['volumeInfo']['authors']:
                    author_tab.append(author)
                while i < len(author_tab):
                    if i == 0:
                        author1 = author_tab[i]
                    else:
                        author1 = author1 + ', ' + author_tab[i]
                    i += 1
            ISBN = item['volumeInfo'].get('industryIdentifiers', 'None')
            if ISBN != 'None':
                for number in item['volumeInfo']['industryIdentifiers']:
                    if number['type'] == 'ISBN_13' or number['type'] == 'OTHER':
                        ISBN = number['identifier']
                    else:
                        continue
            new_book = BooksList(
                title=item['volumeInfo'].get('title', 'None'),
                author=author1,
                published_date=item['volumeInfo'].get('publishedDate', 0),
                ISBN=ISBN,
                page_count=item['volumeInfo'].get('pageCount', 0),
                url_thumbnail=url_import,
                language=item['volumeInfo']['language']
            )
            try:
                db.session.add(new_book)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                print(e)
                return 'There was an issue adding your book'
        return redirect('/')
    else:
        return render_template('import_page_by_author.html')


@app.route('/delete/<string:ISBN>')
def delete(ISBN):
    book_to_delete = BooksList.query.get_or_404(ISBN)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/filter')
def fliter():
    return render_template('filter.html')


@app.route('/filtered_base_author', methods=['POST', 'GET'])
def filter_author():
    if request.method == 'POST':
        author_filter = request.form['author_filter']
        filtered_base = BooksList.query.filter(BooksList.author.ilike(author_filter))
        return render_template('filtered_base.html', books=filtered_base)
    else:
        return render_template('filter_base_author.html')


if __name__ == "__main__":
    app.run(debug=True)