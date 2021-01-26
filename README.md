# Full Stack Casting Agency Project

## Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
This is the capstone project of Udacity fullstack nanodegree program, which demonstrate the skillset of
using Flask, SQLAlchemy, Auth0, gunicorn and heroku to develop and deploy a RESTful API.
([API rk50895-capstone on heroku](https://rk50895-capstone.herokuapp.com/))

## Roles and Permissions
The Casting Agency RESTful API has 3 roles:

1. **Casting Assistant**
    Available userid/password: rk50985_assistant@gmail.com/qwerty01!
    - Can view actor(s) (Permission: 'view:actors')
    - Can view movie(s) (Permission: 'view:movies')

2. **Casting Director**
    Available userid/password: rk50985_director@gmail.com/qwerty01!
    - All permissions a Casting Assistant has and…
    - Can add an actor (Permission: 'add:actors')
    - Can modify an actor (Permission: 'edit:actors')
    - Can delete an actor (Permission: 'delete:actors')
    - Can modify a movie (Permission: 'edit:movies')

3. **Executive Producer**
    Available userid/password: rk50985_producer@gmail.com/qwerty01!
    - All permissions a Casting Director has and…
    - Can add a movie (Permission: 'add:movies')
    - Can delete a movie (Permission: 'delete:movies')

## Getting Started

### Installing Dependencies

#### Python 3

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the project folder and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Heroku](https://dashboard.heroku.com/apps) Deployment Platform.

- [Auth0](https://auth0.com/) Auth0 is an easy to implement, adaptable authentication and authorization platform.

- [Postman](https://www.postman.com/) Testing the Application Endpoints.

## Running the server

From within the project folder first ensure you are working using your created virtual environment.

To run the server locally, execute:

```bash
source setup.sh
flask run
```
content of setup.sh
```
export DATABASE_URL=postgres://hsbncqstmvkgxy:75ccff390bf0a5aeeec5daf32bd2b7a0f1a1607525e8156c3ea551c116410dda@ec2-52-212-157-46.eu-west-1.compute.amazonaws.com:5432/d2fg4qvq80nrbt
export FLASK_APP=app
export FLASK_ENV=development
export AUTH0_DOMAIN=fnsd.eu.auth0.com
export ALGORITHMS=RS256
export API_AUDIENCE=casting
export AUTH0_CLIENT_ID=RGYOEB4PXsPDZlgCn7zmgaaZ1ukFJHpx
export AUTH0_CALLBACK_URL=https://rk50895-capstone.herokuapp.com/
```
Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically. Setting the FLASK_APP variable to directs flask to use the app.py to find the application.

## Endpoints

#### `GET '/movies'`
(Requires permission: 'view:movies')
- Fetches a dictionary of movies
- Returns: Returns Json data about retrieved movies
```
curl http://127.0.0.1:5000/movies
{
  "movies": [
    {
      "actors": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10
      ],
      "id": 1,
      "release_date": "Mon, 01 Jan 2001 00:00:00 GMT",
      "title": "film1"
    },
    {
      "actors": [
        2,
        4,
        6,
        8,
        10
      ],
      "id": 2,
      "release_date": "Sat, 02 Feb 2002 00:00:00 GMT",
      "title": "film2"
    },
    {
      "actors": [
        1,
        3,
        5,
        7,
        9
      ],
      "id": 3,
      "release_date": "Mon, 03 Mar 2003 00:00:00 GMT",
      "title": "film3"
    },
    {
      "actors": [
        1,
        7
      ],
      "id": 4,
      "release_date": "Sun, 04 Apr 2004 00:00:00 GMT",
      "title": "film4"
    },
    {
      "actors": [
        "No actors assigned (yet)"
      ],
      "id": 5,
      "release_date": "Thu, 05 May 2005 00:00:00 GMT",
      "title": "film5"
    }
  ],
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```

#### `GET '/movies/<int:movie_id>'`
(Requires permission: 'view:movies')
- Fetches a movie
- Required URL Arguments: movie_id filled with movie number of choice
- Returns: Returns Json data about retrieved movie
```
curl http://127.0.0.1:5000/movies/1
{
  "movie": {
    "actors": [
      "Actor01",
      "Actor02",
      "Actor03",
      "Actor04",
      "Actor05",
      "Actor06",
      "Actor07",
      "Actor08",
      "Actor10"
    ],
    "id": 1,
    "release_date": "Mon, 01 Jan 2001 00:00:00 GMT",
    "title": "film1"
  },
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```

#### `DELETE '/movies/<int:movie_id>'`
(Requires permission: 'delete:movies')
- Deletes a movie
- Required URL Arguments: movie_id filled with movie number of choice
- Returns: Returns Json data about deleted movie
```
curl --location --request DELETE http://127.0.0.1:5000/movies/4
{
  "id_deleted": 4,
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```

#### `POST '/movies'`
(Requires permission: 'add:movies')
- Posts a new movie 
- Required Data Arguments:  Json data
- Returns: Returns Json data about inserted movie
```
curl --location --request POST http://127.0.0.1:5000/movies -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"title": "film2", "release_date": "02-02-2002", "actors": [2,4,6,8,10]}'
{
  "movie": {
    "actors": [
      "Actor02",
      "Actor04",
      "Actor06",
      "Actor08",
      "Actor10"
    ],
    "id": 2,
    "release_date": "Sat, 02 Feb 2002 00:00:00 GMT",
    "title": "film2"
  },
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```

#### `PATCH '/movies/<int:movie_id>'`
(Requires permission: 'edit:movies')
- Updates a movie
- Required URL Arguments: movie_id filled with movie number of choice
- Returns: Json data about the updated movie
```
curl --location --request PATCH http://127.0.0.1:5000/movies/5 -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"actors": [1,3,5,7,9]}'
{
  "movie": {
    "actors": [
      "Actor01",
      "Actor03",
      "Actor05",
      "Actor07"
    ],
    "id": 5,
    "release_date": "Thu, 05 May 2005 00:00:00 GMT",
    "title": "film5"
  },
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```

#### `GET '/actors'`
(Requires permission: 'view:actors')
- Fetches a dictionary of actors
- Returns: Json data about retrieved actors
```
curl http://127.0.0.1:5000/actors
{
  "actors": [
    {
      "age": 51,
      "gender": "male",
      "id": 1,
      "movies": [
        1,
        3,
        4
      ],
      "name": "Actor01"
    },
    {
      "age": 52,
      "gender": "female",
      "id": 2,
      "movies": [
        1,
        2
      ],
      "name": "Actor02"
    },
    {
      "age": 53,
      "gender": "male",
      "id": 3,
      "movies": [
        1,
        3
      ],
      "name": "Actor03"
    },
    {
      "age": 54,
      "gender": "female",
      "id": 4,
      "movies": [
        1,
        2
      ],
      "name": "Actor04"
    },
    {
      "age": 55,
      "gender": "male",
      "id": 5,
      "movies": [
        1,
        3
      ],
      "name": "Actor05"
    },
    {
      "age": 56,
      "gender": "female",
      "id": 6,
      "movies": [
        1,
        2
      ],
      "name": "Actor06"
    },
    {
      "age": 57,
      "gender": "male",
      "id": 7,
      "movies": [
        1,
        3,
        4
      ],
      "name": "Actor07"
    },
    {
      "age": 58,
      "gender": "female",
      "id": 8,
      "movies": [
        1,
        2
      ],
      "name": "Actor08"
    },
    {
      "age": 59,
      "gender": "male",
      "id": 9,
      "movies": [
        1,
        3
      ],
      "name": "Actor09"
    },
    {
      "age": 60,
      "gender": "female",
      "id": 10,
      "movies": [
        1,
        2
      ],
      "name": "Actor10"
    }
  ],
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```

#### `GET '/actors/<int:actor_id>'`
(Requires permission: 'view:actors')
- Fetches an actor
- Required URL Arguments: actor_id filled with actor number of choice
- Returns: Json data about retrieved actor
```
curl http://127.0.0.1:5000/actors/1
{
  "actor": {
    "age": 51,
    "gender": "male",
    "id": 1,
    "movies": [
      "film1",
      "film3"
    ],
    "name": "Actor01"
  },
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```

#### `DELETE '/actors/<int:actor_id>'`
(Requires permission: 'delete:actors')
- Deletes the `actor_id` of actor
- Required URL Arguments: actor_id filled with actor number of choice
- Returns: Json data about deleted actor
```
curl --location --request DELETE http://127.0.0.1:5000/actors/9
{
  "id_deleted": 9,
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```

#### `POST '/actors'`
(Requires permission: 'add:actors')
- Posts a new actor
- Required URL Arguments: None
- Required Data Arguments:  Json data
```
curl --location --request POST http://127.0.0.1:5000/actors -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor08", "age": "58", "gender": "female"}'
{
  "actor": {
    "age": 58,
    "gender": "female",
    "id": 8,
    "movies": [
      "No movies assigned (yet)"
    ],
    "name": "Actor08"
  },
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```

#### `PATCH '/actors/<int:actor_id>'`
(Requires permission: 'edit:actors')
- Updates an actor
- Required URL Arguments: actor_id filled with actor number of choice
- Returns: Json data about updated actor
```
curl --location --request PATCH http://127.0.0.1:5000/actors/9 -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor Nine"}'
{
  "actor": {
    "age": 59,
    "gender": "male",
    "id": 9,
    "movies": [
      "film1",
      "film3"
    ],
    "name": "Actor Nine"
  },
  "status_code": 200,
  "status_message": "OK",
  "success": true
}
```
## Creating Auth0 tokens

Run the command:
```
https://fnsd.eu.auth0.com/authorize?audience=casting&response_type=token&client_id=RGYOEB4PXsPDZlgCn7zmgaaZ1ukFJHpx&redirect_uri=https://rk50895-capstone.herokuapp.com/
```

Log in with one of these predefined users and copy the token from the response.

Userid/Passwords:
1. **Casting Assistant**
  rk50985_assistant@gmail.com/qwerty01!
2. **Casting Director**
  rk50985_director@gmail.com/qwerty01!
3. **Executive Producer**
  rk50985_producer@gmail.com/qwerty01!

## Managing the database on Heroku
We would like to use the manage.py as suggested in the courses documentation:
```
heroku run python3 manage.py db init --directory app/migrations
heroku run python3 manage.py db migrate --app rk50895-capstone
heroku run python3 manage.py db upgrade --app rk50895-capstone
```
But sadly , but that's not working, because migrate folder disappears after every command or change.

Instead of that I found and used the following work-around:
```
- locally perform "flask db init" and "flask db migrate"
- then commit and promote migrations folder to Heroku via "git push heroku master"
- Then on Heroku: "heroku run python3 manage.py db upgrade --app rk50895-capstone"
```

To propegate some data into the database, I have created the file testdata.sh.
Prepare by creating a auth0 token and saving it in a variable *TOKEN*.
```
export TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhpWlhuV3gwanhSSHdMT3ZTVUp6ayJ9.eyJpc3MiOiJodHRwczovL2Zuc2QuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMDg0YTc3ZmUxZjM4MDA3MWYxZjAyMiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MTE2NTY1NTEsImV4cCI6MTYxMTc0Mjk1MSwiYXpwIjoiUkdZT0VCNFBYc1BEWmxnQ243em1nYWFaMXVrRkpIcHgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.3tb5_sy7oi21k5jlJhUtzgOQiqjydq-p9W56XgAQB7cpA6ajm2BOg0e0ad3U3l5odhkYsVIfv-jnYcSqiAGJHfg8bikkfdGmLIybhcQ9cKDXA0iBksy73k-U9uZmXx9tLNDW43N_-8oqAUAf3_hRRhxOohHXW0C9qs61mBJBDZIroLpSQsqys8P81_dGdvVSl1LdlvCNtR8ZsjqtKjACshNLm_2vvz8MUemJhQcV5460Gd6DNPPRGPFkYoF71J8xIQoE3KnGduqnN4FoFCvTbWyNVDTGH-r42EwXuV4FO5lZJLTTdyEY_ZHXna2sZiy0PGtWg3XqVtWRvGOyPtc7jQ
source testdata.sh
```
Content of testdata.sh:
```
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor01", "age": "51", "gender": "male"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor02", "age": "52", "gender": "female"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor03", "age": "53", "gender": "male"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor04", "age": "54", "gender": "female"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor05", "age": "55", "gender": "male"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor06", "age": "56", "gender": "female"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor07", "age": "57", "gender": "male"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor08", "age": "58", "gender": "female"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor09", "age": "59", "gender": "male"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"name": "Actor10", "age": "60", "gender": "female"}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/movies -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"title": "film01", "release_date": "01-01-2001", "actors": [1,2,3,4,5,6,7,8,9,10]}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/movies -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"title": "film02", "release_date": "02-02-2002", "actors": [2,4,6,8,10]}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/movies -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"title": "film03", "release_date": "03-03-2003", "actors": [1,3,5,7,9]}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/movies -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"title": "film04", "release_date": "04-04-2004", "actors": [1,7]}'
curl --location --request POST https://rk50895-capstone.herokuapp.com/movies -H "Authorization: Bearer ${TOKEN}" -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"title": "film05", "release_date": "05-05-2005", "actors": []}'
```
Verify with:
```
curl https://rk50895-capstone.herokuapp.com/actors -H "Authorization: Bearer ${TOKEN}"
curl https://rk50895-capstone.herokuapp.com/movies -H "Authorization: Bearer ${TOKEN}"
```

## Testing locally
To run the tests on a test database from the project folder, run
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone_test.psql
python3 test_app.py
```

## Testing heroku api
To run the tests on the [heroku api](https://rk50895-capstone.herokuapp.com/), a postman collection has been created for testing the endpoints.
Import [the file](rk50895-capstone.postman_collection.json) into Postman to run the tests.
*Bearer token* and *Capstone-url* will have to be filled in the collection defenition accordingly. 
