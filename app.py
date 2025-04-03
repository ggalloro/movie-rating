from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringForm, SubmitForm, IntegerForm

app = Flask(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True)
    ratings = db.relationship("Rating", backref="movie", lazy="dynamic")

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey(movie.id))

with app.app_context():
    db.create_all()

class SubmitMovie(FlaskForm):
    title = StringField("Movie Title")
    submit = SubmitField("Add Movie")

class VoteMovie(FlaskForm):
    value = IntegerForm("Rating")
    submit = SubmitField("Rate Movie")


@app.route("/")
def index():
    return render_template("index.html")

#@app.route("/movies/<int:id>", methods=["GET","POST"])
#def movie_id():
#    vote_form = 


@app.route("/addmovie", methods=["GET","POST"])
def addmovie():
    movie_form = SubmitMovie()
    if movie_form.validate_on_submit():
        movie = Movie(title = movie_form.title.data)
    return render_template("addmovie.html", movie_form = movie_form)


