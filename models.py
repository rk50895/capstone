import os
from sqlalchemy import (
    Column, String, Integer, DateTime, create_engine
)
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
actor_movie
Holds relation between Actor and Movie and vv.
'''
actor_movie = db.Table(
    'actor_movie',
    db.Column(
        'actor_id',
        db.Integer,
        db.ForeignKey('actors.id'),
        primary_key=True
    ),
    db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('movies.id'),
        primary_key=True
    )
)

'''
Actor
Have name, age and gender
'''


class Actor(db.Model):
    __tablename__ = 'actors'
    # Type Integer, Autoincrementing, for unique primary key id
    id = db.Column(db.Integer, primary_key=True)
    # Type String for storing unique name
    name = db.Column(db.String(), nullable=False, unique=True)
    # Type Integer for storing age
    age = db.Column(db.Integer)
    # Type String for storing gender
    gender = db.Column(db.String())
    # Type relationship to store all actors related to this movie
    movies = db.relationship(
        'Movie',
        secondary=actor_movie
    )

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    '''
    short()
        short form representation of the Movie model
    '''

    def short(self):
        # Retrieve all id's of related movies for current actor
        movie_id_selection = [
            key_pair[1] for key_pair in db.session.query(actor_movie).
            order_by(actor_movie.c.movie_id).
            filter(actor_movie.c.actor_id == self.id).
            all()
        ]
        if not movie_id_selection:
            movie_id_selection = ['No movies assigned (yet)']

        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': movie_id_selection
        }

    '''
    long()
        long form representation of the Movie model
    '''

    def long(self):
        # Retrieve all id's of related movies for current actor
        movie_id_selection = [
            key_pair[1] for key_pair in db.session.query(actor_movie).
            order_by(actor_movie.c.movie_id).
            filter(actor_movie.c.actor_id == self.id).
            all()
        ]

        # For each id of all related movies for current actor
        # retrieve further detail(s) from Movie table
        if movie_id_selection:
            movies = [
                Movie.query.get(movie_id).title
                for movie_id in movie_id_selection
            ]
        else:
            movies = ['No movies assigned (yet)']

        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': movies
        }

    '''
    insert()
        inserts a new actor into the database
        the actor must have a unique name
        EXAMPLE
            actor = Actor(name=req_name, age=req_age, gender=req_gender)
            actor.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an actor from the database
        the actor must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == req_id).one_or_none()
            actor.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a changed actor in the database
        the actor must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == req_id).one_or_none()
            actor.name = 'Changed actor name'
            actor.update()
    '''

    def update(self):
        db.session.commit()


'''
Movie
Have title and release date
'''


class Movie(db.Model):
    __tablename__ = 'movies'
    # Type Integer, Autoincrementing, for unique primary key id
    id = db.Column(db.Integer, primary_key=True)
    # Type String for storing unique title
    title = db.Column(db.String(), nullable=False, unique=True)
    # Type DateTime for storing release_date
    release_date = db.Column(db.DateTime())
    # Type relationship to store all actors related to this movie
    actors = db.relationship(
        'Actor',
        secondary=actor_movie
    )

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    '''
    short()
        short form representation of the Movie model
    '''

    def short(self):
        # Retrieve all id's of related actors for current movie
        actor_id_selection = [
            key_pair[0] for key_pair in db.session.query(actor_movie).
            order_by(actor_movie.c.actor_id).
            filter(actor_movie.c.movie_id == self.id).
            all()
        ]
        if not actor_id_selection:
            actor_id_selection = ['No actors assigned (yet)']

        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': actor_id_selection
        }

    '''
    long()
        long form representation of the Movie model
    '''

    def long(self):
        # Retrieve all id's of related actors for current movie
        actor_id_selection = [
            key_pair[0] for key_pair in db.session.query(actor_movie).
            order_by(actor_movie.c.actor_id).
            filter(actor_movie.c.movie_id == self.id).
            all()
        ]

        # For each id of all related actors for current movie
        # retrieve further detail(s) from Actor table
        if actor_id_selection:
            actors = [
                Actor.query.get(actor_id).name
                for actor_id in actor_id_selection
            ]
        else:
            actors = ['No actors assigned (yet)']

        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': actors
        }

    '''
    insert()
        inserts a new movie into the database
        the movie must have a unique title
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a movie from the database
        the movie must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == req_id).one_or_none()
            movie.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a changed movie in the database
        the movie must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == req_id).one_or_none()
            movie.title = 'Changed movie title'
            movie.update()
    '''

    def update(self):
        db.session.commit()
