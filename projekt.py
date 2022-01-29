from _datetime import datetime

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from forms import BookAddingForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SECRET_KEY'] = '123'
db = SQLAlchemy(app)


class BooksList(db.Model):
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    published_date = db.Column(db.DateTime, default=datetime.date)
    ISBN = db.Column(db.Integer, primary_key=True)
    page_count = db.Column(db.Integer, primary_key=True)
    # url_thumbnail
    language = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<ISBN %r>' % self.ISBN


@app.route('/', methods=['POST', 'GET'])
def welcome():
    books = BooksList.query.order_by(BooksList.ISBN).all()
    return render_template('welcome.html', books=books)


@app.route('/adding', methods=['POST', 'GET'])
def adding():
    form = BookAddingForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print("Działa!")
            new_book = BooksList(
                title=BookAddingForm.Title,
                author=BookAddingForm.Author,
                published_date=BookAddingForm.PublishedDate,
                ISBN=BookAddingForm.ISBN,
                page_count=BookAddingForm.Page_count,
                language=BookAddingForm.Language
            )
            try:
                db.session.add(new_book)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
        else:
            print("Nie jest valid!")
            return render_template(
                'book_adding.html',
                form=form
            )
    elif request.method == 'GET':
        print("Nie działa")
        return render_template(
        'book_adding.html',
        form=form
        )


if __name__ == "__main__":
    app.run(debug=True)