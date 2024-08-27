from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-movie-store.db"

# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)


class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)  # Allow NULL
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)  # Allow NULL
    review: Mapped[str] = mapped_column(String(250), nullable=True)  # Allow NULL
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book: {self.title}>'


with app.app_context():
    db.create_all()


class MyForm(FlaskForm):
    rating = StringField('Your Rating Out of 10 e.g. 7.8', validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


# CREATE TABLE

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POSt"])
def edit():
    form = MyForm()
    movie_id = request.args.get("id")
    title = request.args.get("title")
    if form.validate_on_submit():
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        # or book_to_update = db.get_or_404(Book, book_id)
        movie_to_update.review = form.review.data
        movie_to_update.rating = form.rating.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", form=form, title=title)


@app.route('/delete')
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    # or book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


class New_form(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route('/add', methods=["GET", "POSt"])
def add():
    form = New_form()
    if form.validate_on_submit():
        response = requests.get("https://api.themoviedb.org/3/search/movie",
                                params={"api_key": 'efec31ba5122b4e5574dae96d155856d',
                                        "query": form.title.data})
        data = response.json()["results"]
        return render_template('select.html', options=data)

    return render_template('add.html', form=form)


@app.route('/movie')
def get_movie_detail():
    movie_id = request.args.get("movie_id")
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}",
                            params={"api_key": 'efec31ba5122b4e5574dae96d155856d'})
    movie_detail = response.json()

    new_movie = Movie(
        title=movie_detail['original_title'],
        year=movie_detail['release_date'].split("-")[0],
        description=movie_detail['overview'],
        rating=movie_detail['vote_average'],  # Provide a default value for rating
        ranking=0,
        review="",
        img_url=f"https://image.tmdb.org/t/p/w500{movie_detail['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
