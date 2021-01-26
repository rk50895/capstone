import os
import json
from flask import (
    Flask, request, abort, jsonify
)
from sqlalchemy import exc
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import (
    AuthError, requires_auth
)
from models import (
    db, setup_db, Actor, Movie, actor_movie, db_drop_and_create_all
)


def create_app(test_config=None):
    '''
        Create and configure app
    '''
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    # db_drop_and_create_all()
    migrate = Migrate(app, db)

    '''
        CORS Headers
    '''
    @app.after_request
    def after_request(response):

        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )

        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PATCH, POST, DELETE, OPTIONS'
        )

        return response

    '''
        Start of declaration of all ROUTES
    '''

    '''
        GET /
            it should be a public endpoint
            it is a dummy endpoint
        returns welcome message
    '''
    @app.route('/')
    def index():

        return "Welcome to my Capstone project!"

    '''
        GET /actors
            it should be a public endpoint
            it should contain only the actor.short() data representation
        returns status code 200 and json {"success": True, "actors": actors}
            where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def get_actors(jwt):

        # Retrieve all actors from database
        try:
            actor_selection = [
                actor.short() for actor in Actor.query.order_by(Actor.id).all()
            ]
        except Exception as e:
            # print(e)
            abort(422)

        # No actors in database
        if len(actor_selection) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "actors": actor_selection
        })

    '''
        GET /actors/<id>
            it should be a public endpoint
            where <id> is the existing actor id
            it should respond with a 404 error if <id> is not found
            it should contain only the actor.long() data representation
        returns status code 200 and json {"success": True, "actor": actor}
            where actor is the selected actor
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('view:actors')
    def get_actor(jwt, actor_id):

        # Retrieve requested actor from database
        try:
            target_actor = Actor.query.get(actor_id)
        except Exception as e:
            # print(e)
            abort(422)

        # No actor for this id in database
        if target_actor is None:
            abort(404)

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "actor": target_actor.long()
        })

    '''
        POST /actors
            it should create a new row in the actors table
            it should require the 'add:actors' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True, "actor": actor}
            where actor contains only the newly created actor
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actors')
    def post_actors(jwt):

        # Retrieve JSON payload
        body = request.get_json()

        # No JSON payload provided
        if not body:
            abort(400)

        name = body.get("name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)
        movies = body.get("movies", None)

        if name is None:
            abort(422)

        new_actor = Actor(name=name, age=age, gender=gender)

        if movies:
            new_actor.movies = Movie.query.filter(Movie.id.in_(movies)).all()

        try:
            new_actor.insert()

            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": "OK",
                "actor": new_actor.long()
            })
        except Exception as e:
            # print(e)
            abort(422)

    '''
        PATCH /actors/<id>
            where <id> is the existing actor id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'edit:actors' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True, "actor": actor}
            where actor containing only the updated actor
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def patch_actors(jwt, actor_id):

        # Retrieve JSON payload
        body = request.get_json()

        # No JSON payload provided
        if not body:
            abort(400)

        name = body.get("name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)
        movies = body.get("movies", None)

        # Retrieve requested actor from database
        target_actor = Actor.query.get(actor_id)

        if target_actor is None:
            abort(404)

        if name:
            target_actor.name = name

        if age:
            target_actor.age = age

        if gender:
            target_actor.gender = gender

        if movies:
            target_actor.movies = Movie.query.filter(
                Movie.id.in_(movies)).all()

        try:
            target_actor.update()

            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": 'OK',
                "actor": target_actor.long()
            })
        except Exception as e:
            # print(e)
            abort(422)

    '''
        DELETE /actors/<id>
            where <id> is the existing actor id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actors' permission
        returns status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actors(jwt, actor_id):

        # Retrieve requested actor from database
        target_actor = Actor.query.get(actor_id)

        if target_actor is None:
            abort(404)

        try:
            target_actor.delete()

            return jsonify({"success": True,
                            "status_code": 200,
                            "status_message": 'OK',
                            "id_deleted": actor_id})
        except Exception as e:
            # print(e)
            abort(422)

    '''
        GET /movies
            it should be a public endpoint
            it should contain only the movie.short() data representation
        returns status code 200 and json {"success": True, "movies": movies}
            where movies is the list of movies
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=["GET"])
    @requires_auth('view:movies')
    def get_movies(jwt):

        # Retrieve all movies from database
        try:
            movie_selection = [
                movie.short() for movie in Movie.query.order_by(Movie.id).all()
            ]
        except Exception as e:
            # print(e)
            abort(422)

        # No movies in database
        if len(movie_selection) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "movies": movie_selection
        })

    '''
        GET /movies/<id>
            it should be a public endpoint
            where <id> is the existing movie id
            it should respond with a 404 error if <id> is not found
            it should contain only the movie.long() data representation
        returns status code 200 and json {"success": True, "movie": movie}
            where movie is the selected movie
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('view:movies')
    def get_movie(jwt, movie_id):

        # Retrieve requested movie from database
        try:
            target_movie = Movie.query.get(movie_id)
        except Exception as e:
            # print(e)
            abort(422)

        # No movie for this id in database
        if target_movie is None:
            abort(404)

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "movie": target_movie.long()
        })

    '''
        POST /movies
            it should create a new row in the movies table
            it should require the 'add:movies' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movie": movie}
            where movie contains only the newly created movie
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='add:movies')
    def post_movies(jwt):

        # Retrieve JSON payload
        body = request.get_json()

        # No JSON payload provided
        if not body:
            abort(400)

        title = body.get("title", None)
        release_date = body.get("release_date", None)
        actors = body.get('actors', None)

        if title is None:
            abort(400)

        new_movie = Movie(title=title, release_date=release_date)

        if actors:
            new_movie.actors = Actor.query.filter(Actor.id.in_(actors)).all()

        try:
            new_movie.insert()

            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": 'OK',
                "movie": new_movie.long()
            })
        except Exception as e:
            # print(e)
            abort(422)

    '''
        PATCH /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:movies' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movies": movie}
            where movie an array containing only the updated movie
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission='edit:movies')
    def patch_movies(jwt, movie_id):

        # Retrieve JSON payload
        body = request.get_json()

        # No JSON payload provided
        if not body:
            abort(400)

        title = body.get("title", None)
        release_date = body.get("release_date", None)
        actors = body.get("actors", None)

        # Retrieve requested movie from database
        target_movie = Movie.query.get(movie_id)

        if target_movie is None:
            abort(404)

        if title:
            target_movie.title = title

        if release_date:
            target_movie.release_date = release_date

        if actors:
            target_movie.actors = Actor.query.filter(
                Actor.id.in_(actors)).all()

        try:
            target_movie.update()

            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": 'OK',
                "movie": target_movie.long()
            })
        except Exception as e:
            # print(e)
            abort(422)

    '''
        DELETE /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movies' permission
        returns status code 200 and json {"success": True, "delete": id}
            where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movies(jwt, movie_id):

        # Retrieve requested movie from database
        target_movie = Movie.query.get(movie_id)

        if target_movie is None:
            abort(404)

        try:
            target_movie.delete()

            return jsonify({"success": True,
                            "status_code": 200,
                            "status_message": 'OK',
                            "id_deleted": movie_id})
        except Exception as e:
            # print(e)
            abort(422)

    '''
        Error handling for resource not found
    '''
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "status_message": "bad request"
        }), 400

    '''
        Error handling for resource not found
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "status_message": "resource not found"
        }), 404

    '''
        Error handling for method not allowed'
    '''
    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "status_message": "method not allowed"
        }), 405

    '''
        Error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "status_message": "unprocessable"
        }), 422

    '''
        Error handling for AuthError that were raised
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
