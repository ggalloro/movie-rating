from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SECRET_KEY"] = "secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True)
    ratings = db.relationship("Rating", backref="movie", lazy="dynamic")

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

with app.app_context():
    db.create_all()

class SubmitMovie(FlaskForm):
    title = StringField("Movie Title")
    submit = SubmitField("Add Movie")

class VoteMovie(FlaskForm):
    value = IntegerField("Rating")
    submit = SubmitField("Rate Movie")


@app.route("/")
def index():
    movies = Movie.query.all()
    return render_template("index.html", movies = movies)

@app.route("/movies/<int:movie_id>", methods=["GET","POST"])
def movie_id(movie_id):
    vote_form = VoteMovie()
    movie = Movie.query.get(movie_id)
    if vote_form.validate_on_submit():
        rating = Rating(stars = vote_form.value.data, movie_id=movie_id)
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("movie_detail.html", movie = movie, vote_form = vote_form)


@app.route("/addmovie", methods=["GET","POST"])
def addmovie():
    movie_form = SubmitMovie()
    if movie_form.validate_on_submit():
        movie = Movie(title = movie_form.title.data)
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("addmovie.html" , movie_form = movie_form )

if __name__ == '__main__':
    app.run(debug=True)
