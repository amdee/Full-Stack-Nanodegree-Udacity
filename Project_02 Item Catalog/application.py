#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
from flask import make_response, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie, User
from flask import session as login_session
from functools import wraps
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
# from sqlalchemy.pool import StaticPool

app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///Movie_Genre.db',
                       connect_args={'check_same_thread': False})


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Authentication
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Movie Catalog App"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in login_session:
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return decorated_function


# Connecting to google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is '
                                            'already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['email']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;' \
              'border-radius: 150px;-webkit-border-radius: ' \
              '150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?' \
          'token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully '
                                            'disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token '
                                            'for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs to view Genre Information
@app.route('/genre/<int:genre_id>/movie/JSON')
def genreMovieJSON(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(
        genre_id=genre_id).all()
    return jsonify(Movies=[i.serialize for i in movies])


@app.route('/genre/<int:genre_id>/movie/<int:movie_id>/JSON')
def movieItemJSON(genre_id, movie_id):
    movie_item = session.query(Movie).filter_by(id=movie_id).one()
    return jsonify(movie_item=movie_item.serialize)


@app.route('/genre/JSON')
def genresJSON():
    genres = session.query(Genre).all()
    return jsonify(genres=[r.serialize for r in genres])


# Show all genres
@app.route('/')
@app.route('/genre/')
def showGenres():
    genres = session.query(Genre).order_by(asc(Genre.name))
    if 'username' not in login_session:
        return render_template('publicgenres.html', genres=genres)
    else:
        return render_template('genres.html', genres=genres)


# Create a new genre
@app.route('/genre/new/', methods=['GET', 'POST'])
@login_required
def newGenre():
    if request.method == 'POST':
        print(login_session)
        if 'user_id' not in login_session and 'email' in login_session:
            login_session['user_id'] = getUserID(login_session['email'])
        newGenre = Genre(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newGenre)
        flash('New Genre %s Successfully Created' % newGenre.name)
        session.commit()
        flash("New genre created!", 'success')
        return redirect(url_for('showGenres'))
    else:
        return render_template('newGenre.html')


# Edit a genre
@app.route('/genre/<int:genre_id>/edit/', methods=['GET', 'POST'])
@login_required
def editGenre(genre_id):
    editedGenre = session.query(
        Genre).filter_by(id=genre_id).one()
    if editedGenre.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not " \
               "authorized to edit this genre. Please create your own genre" \
               " in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
            flash('Genre Successfully Edited %s' % editedGenre.name)
            return redirect(url_for('showGenres'))
    else:
        return render_template('editGenre.html', genre=editedGenre)


# Delete a genre
@app.route('/genre/<int:genre_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteGenre(genre_id):
    genreToDelete = session.query(
        Genre).filter_by(id=genre_id).one()
    if genreToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not " \
               "authorized to delete this genre. Please create your " \
               "own genre in order to delete.');}</script><body " \
               "onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(genreToDelete)
        flash('%s Successfully Deleted' % genreToDelete.name)
        session.commit()
        return redirect(url_for('showGenres', genre_id=genre_id))
    else:
        return render_template('deleteGenre.html', genre=genreToDelete)


# Show a genre movie
@app.route('/genre/<int:genre_id>/')
@app.route('/genre/<int:genre_id>/movie/')
def showMovie(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    creator = getUserInfo(genre.user_id)
    movies = session.query(Movie).filter_by(
        genre_id=genre_id).all()
    if 'username' not in login_session or \
            creator.id != login_session['user_id']:
        return render_template('publicmovie.html', movies=movies,
                               genre=genre, creator=creator)
    else:
        return render_template('movie.html', movies=movies,
                               genre=genre, creator=creator)


# Create a new movie
@app.route('/genre/<int:genre_id>/movie/new/', methods=['GET', 'POST'])
def newMovie(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if login_session['user_id'] != genre.user_id:
        return "<script>function myFunction() {alert('You are not " \
               "authorized to add movies to this genre. Please create" \
               " your own genre in order to add movies.');}</script><body" \
               " onload='myFunction()'>"
        if request.method == 'POST':
            newmovie = Movie(name=request.form['name'],
                             description=request.form['description'],
                             price=request.form['price'],
                             ratings=request.form['course'],
                             genre_id=genre_id, user_id=genre.user_id)
            session.add(newmovie)
            session.commit()
            flash('New Movie %s Movie Successfully Created' % (newmovie.name))
            return redirect(url_for('showMovie', genre_id=genre_id))
    else:
        return render_template('newmovie.html', genre_id=genre_id)


# Edit a movie
@app.route('/genre/<int:genre_id>/movie/<int:movie_id>/edit',
           methods=['GET', 'POST'])
def editMovie(genre_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedMovie = session.query(Movie).filter_by(id=movie_id).one()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if login_session['user_id'] != genre.user_id:
        return "<script>function myFunction() {alert('You are not authorized" \
               " to edit movie items to this genre. Please create your " \
               "own genre in order to edit movies.');}</script><body " \
               "onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedMovie.name = request.form['name']
        if request.form['description']:
            editedMovie.description = request.form['description']
        if request.form['price']:
            editedMovie.price = request.form['price']
        if request.form['ratings']:
            editedMovie.course = request.form['ratings']
        session.add(editedMovie)
        session.commit()
        flash('Movie Successfully Edited')
        return redirect(url_for('showMovie', genre_id=genre_id))
    else:
        return render_template('editmovie.html', genre_id=genre_id,
                               movie_id=movie_id, movie=editedMovie)


# Delete a movie
@app.route('/genre/<int:genre_id>/movie/<int:movie_id>/delete',
           methods=['GET', 'POST'])
def deleteMovie(genre_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movieToDelete = session.query(Movie).filter_by(id=movie_id).one()
    if login_session['user_id'] != genre.user_id:
        return "<script>function myFunction() {alert('You are " \
               "not authorized to delete movie items to this genre. " \
               "Please create your own genre in order to delete " \
               "movie items.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(movieToDelete)
        session.commit()
        flash('Movie Successfully Deleted')
        return redirect(url_for('showMovie', genre_id=genre_id))
    else:
        return render_template('deleteMovie.html', movie=movieToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showGenres'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showGenres'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
