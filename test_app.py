import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db

'''
    AUTH0 Bearer tokens for all 3 roles
'''
rk50985_producer = '''
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhpWlhuV3gwanhSSHdMT3ZTVUp6ayJ9.ey
Jpc3MiOiJodHRwczovL2Zuc2QuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMDg0YTc3ZmUxZ
jM4MDA3MWYxZjAyMiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MTE2NTY1NTEsImV4cCI6MTYxMTc0
Mjk1MSwiYXpwIjoiUkdZT0VCNFBYc1BEWmxnQ243em1nYWFaMXVrRkpIcHgiLCJzY29wZSI6IiIsInB
lcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbG
V0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3O
m1vdmllcyJdfQ.3tb5_sy7oi21k5jlJhUtzgOQiqjydq-p9W56XgAQB7cpA6ajm2BOg0e0ad3U3l5od
hkYsVIfv-jnYcSqiAGJHfg8bikkfdGmLIybhcQ9cKDXA0iBksy73k-U9uZmXx9tLNDW43N_-8oqAUAf
3_hRRhxOohHXW0C9qs61mBJBDZIroLpSQsqys8P81_dGdvVSl1LdlvCNtR8ZsjqtKjACshNLm_2vvz8
MUemJhQcV5460Gd6DNPPRGPFkYoF71J8xIQoE3KnGduqnN4FoFCvTbWyNVDTGH-r42EwXuV4FO5lZJL
TTdyEY_ZHXna2sZiy0PGtWg3XqVtWRvGOyPtc7jQ
'''.replace('\n', '')

rk50985_assistant = '''
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhpWlhuV3gwanhSSHdMT3ZTVUp6ayJ9.ey
Jpc3MiOiJodHRwczovL2Zuc2QuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMDZlNjAyNmY3Y
2I4MDA2OWY4YTFlMyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MTE2NzA3NDksImV4cCI6MTYxMTc1
NzE0OSwiYXpwIjoiUkdZT0VCNFBYc1BEWmxnQ243em1nYWFaMXVrRkpIcHgiLCJzY29wZSI6IiIsInB
lcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.wwMlpL6yMQRYPD2vb1KUaY
QZ0WqkuW287zYU2GNBX-x3V_HK4vWtjnlc2tGtXoNBW33IrDoM84ZvHA5Gwn_zoJU13PjavuSduPAGE
0WUdC1eMsJ7__q1XjvyZ3aI3visDB1CERjXb02pR-bXgePLLayO1GCF29tDAJiV0la771F44xblVO4l
ov9gjtTwCr18nWm1GnDWWpDRzJjUB366yJPRjAGXHw1R_8PS0JILqzlzi_JKF1RR-_A9Zxa59SNFFzC
jjKohN16vSZrTUmBDcST580yMIwdOEGQJnl6CDD6gmgSjFVFb0MqnmMNS2_NehP5tIW41wuMCGoexA5
s5ng
'''


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            "name": "Actor11",
            "age": 61,
            "gender": "male",
        }

        self.new_movie = {
            "title": "film6",
            "release_date": "06-06-2006"
        }

        self.change_actor = {
            "name": "New Name",
        }

        self.change_movie = {
            "title": "New Title",
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    All tests on endpoint @app.route('/actors')
    '''

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actor1(self):
        res = self.client().get(
            '/actors/1',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_get_actors_no_endpoint(self):
        res = self.client().get(
            '/actors/1000',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'resource not found')

    '''
    All tests on endpoint @app.route('/movies')
    '''

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_movie1(self):
        res = self.client().get(
            '/movies/1',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_get_movies_no_endpoint(self):
        res = self.client().get(
            '/movies/1000',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'resource not found')

    '''
    All tests on endpoint @app.route('/actors', methods=['POST'])
    '''

    def test_create_actor(self):

        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_twice(self):

        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'unprocessable')

    def test_create_actor_no_json(self):

        res = self.client().post(
            '/actors',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'bad request')

    def test_create_actor_empty_json(self):

        new_actor = {}

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'bad request')

    def test_create_actor_no_endpoint(self):

        res = self.client().post(
            '/actors/1000',
            json=self.new_actor,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'method not allowed')

    def test_create_actor_no_auth_header(self):

        res = self.client().post(
            '/actors',
            json=self.new_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'],
                         'Authorization header is expected.')

    def test_create_actor_not_authorized(self):

        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': 'Bearer ' + rk50985_assistant}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    '''
    All tests on endpoint @app.route('/movies', methods=['POST'])
    '''

    def test_create_movie(self):

        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_twice(self):

        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'unprocessable')

    def test_create_movie_no_json(self):

        res = self.client().post(
            '/movies',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'bad request')

    def test_create_movie_empty_json(self):

        new_movie = {}

        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'bad request')

    def test_create_movie_no_endpoint(self):

        res = self.client().post(
            '/movies/1000',
            json=self.new_movie,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'method not allowed')

    '''
    All tests on endpoint
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    '''

    def test_del_specific_actors(self):

        res = self.client().delete(
            '/actors/4',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_deleted'])

    def test_del_specific_actors_wrong_id(self):

        res = self.client().delete(
            '/actors/1000',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'resource not found')

    def test_del_specific_actors_wrong_url(self):

        res = self.client().delete(
            '/actors',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'method not allowed')

    '''
    All tests on endpoint
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    '''

    def test_del_specific_movies(self):

        res = self.client().delete(
            '/movies/4',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_deleted'])

    def test_del_specific_movies_wrong_id(self):

        res = self.client().delete(
            '/movies/1000',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'resource not found')

    def test_del_specific_movies_wrong_url(self):

        res = self.client().delete(
            '/movies',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'method not allowed')

    '''
    All tests on endpoint
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    '''

    def test_upd_specific_actors(self):

        res = self.client().patch(
            '/actors/5',
            json=self.change_actor,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_upd_specific_actors_wrong_id(self):

        res = self.client().patch(
            '/actors/1000',
            json=self.change_actor,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'resource not found')

    def test_upd_specific_actors_wrong_url(self):

        res = self.client().patch(
            '/actors',
            json=self.change_actor,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'method not allowed')

    def test_upd_specific_actors_no_json(self):

        res = self.client().patch(
            '/actors/5',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'bad request')

    def test_upd_specific_actors_empty_json(self):

        change_actor = {}

        res = self.client().patch(
            '/actors/5',
            json=change_actor,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'bad request')

    '''
    All tests on endpoint
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    '''

    def test_upd_specific_movies(self):

        res = self.client().patch(
            '/movies/5',
            json=self.change_movie,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_upd_specific_movies_wrong_id(self):

        res = self.client().patch(
            '/movies/1000',
            json=self.change_movie,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'resource not found')

    def test_upd_specific_movies_wrong_url(self):

        res = self.client().patch(
            '/movies',
            json=self.change_movie,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'method not allowed')

    def test_upd_specific_movies_no_json(self):

        res = self.client().patch(
            '/movies/5',
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'bad request')

    def test_upd_specific_movies_empty_json(self):

        change_movie = {}

        res = self.client().patch(
            '/movies/5',
            json=change_movie,
            headers={'Authorization': 'Bearer ' + rk50985_producer}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
