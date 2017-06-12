#!/usr/bin/env python

from flask import Flask, render_template, request,\
 redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import session
import random
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import string


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db = DBSession()


# TODO: Add Facebook and local logins
# TODO: Add alerts for logins/logout
@app.route('/login/')
def showLogin():
    ''' showLogin() - Create anti-forgery state token'''
    session['state'] = ''.join(random.choice(string.ascii_uppercase +
                               string.digits) for x in xrange(32))
    return render_template('login.html', STATE=session['state'])


@app.route('/gconnect', methods=['POST'])
def gconnect():
    ''' Use state token to connect to Google OAuth'''
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Get credenitals object from auth code
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Check access token info for errors
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the token matches the user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the token is authorized for the app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if the user is already online
    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # If data does not contain username give them one based on their email
    if (data['name'] == ''):
        session['username'] = data['email'][:data['email'].find('@')]
    else:
        session['username'] = data['name']

    session['picture'] = data['picture']
    session['email'] = data['email']

    return "Login Successful"


@app.route('/gdisconnect/')
def gdisconnect():
    ''' gdisconnect() - Revoke a current user's token
        and reset their session
    '''
    access_token = session.get('access_token')
    # If user is not connected, inform them
    if access_token is None:
        response = make_response(json.dumps('User not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Otherwise revoke token and delete the session
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/', code=302)
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Catalog Information
@app.route('/Category/<string:category_name>/JSON')
def categoryJSON(category_name):
    ''' categoryJSON(category_name) - Create JSON API endpoint for a category

        @arg category_name - category name supplied by URL
    '''
    category = db.query(Category).filter_by(name=category_name).one()
    items = db.query(Item).filter_by(
        category_id=category.id).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/Category/<string:category_name>/Item/<string:item_name>/JSON')
def itemJSON(category_name, item_name):
    ''' itemJSON(category_name) - Create JSON API endpoint for an item

        @arg category_name - category name supplied by URL
        @arg item_name - item name supplied by URL
    '''
    item = db.query(Item).filter_by(name=item_name).one()
    return jsonify(item=item.serialize)


@app.route('/categories/JSON')
def categoriesJSON():
    ''' categoriesJSON(category_name) - Create JSON API
                                        endpoint for the catalog
    '''
    categories = db.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# TODO: Add search
@app.route('/')
@app.route('/index/')
@app.route('/catalog/')
def index():
    ''' index() - Route for index/catalog '''
    user = getUser()
    categories = db.query(Category).limit(5).all()
    items = db.query(Item).limit(6).all()
    return render_template('index.html', user=user, categories=categories,
                           items=items, db=db, Category=Category)


@app.route('/Categories/')
@app.route('/categories/')
def showCategories():
    ''' showCategories() - Route for categories '''
    user = getUser()
    categories = db.query(Category).all()
    return render_template('categories.html', user=user, categories=categories,
                           Item=Item, Category=Category, db=db)


@app.route('/Category/new/', methods=['GET', 'POST'])
def newCategory():
    ''' newCategory() - Route for creating a new category '''
    user = getUser()
    if user is None:  # Make sure the user is logged on
        return redirect('/login')
    # If submitting form get data to create category
    if request.method == 'POST':
        if request.form['category'] == "None":  # For categories
            newCategory = Category(name=request.form['name'],
                                   description=request.form['description'],
                                   creator=session['username'])
        else:  # For subcategories
            newCategory = Category(name=request.form['name'],
                                   description=request.form['description'],
                                   creator=session['username'],
                                   parent_id=db.query(
                                    Category.id).filter_by(
                                    name=request.form['category']).all()[0][0])
        db.add(newCategory)
        db.commit()
        return redirect(url_for('showCategories'))
    else:
        categories = db.query(Category).order_by(Category.name).all()
        return render_template('newCategory.html', categories=categories)


@app.route('/Category/<string:category_name>/edit/', methods=['GET', 'POST'])
def editCategory(category_name):
    ''' editCategory() - Edit an existing category

        @arg category_name - category to edit supplied by URL
    '''
    category_name = URLtoString(category_name)
    user = getUser()
    if user is None:  # Make sure the user is logged in
        return redirect('/login')
    category = db.query(Category).filter_by(name=category_name).one()
    # Make sure the logged in user created the category
    if category.creator != session['username']:
        return redirect('/Category/' + category_name)
    if request.method == 'POST':  # If posting form update data
        if request.form['name']:
            category.name = request.form['name']
        if request.form['description']:
            category.description = request.form['description']
        return redirect(url_for('showCategory', category_name=category.name))
    else:
        return render_template('editCategory.html', category=category)


@app.route('/Category/<string:category_name>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_name):
    ''' deleteCategory - delete a category

        @arg category_name - category to delete supplied by URL
    '''
    user = getUser()
    category_name = URLtoString(category_name)
    if user is None:  # Make sure user is logged on
        return redirect('/login')
    category = db.query(
        Category).filter_by(name=category_name).one()
    # Make sure logged in user is the creator of the category
    if category.creator != session['username']:
        return redirect('/Category/' + category_name)
    if request.method == 'POST':  # If post delete category
        db.delete(category)
        db.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteCategory.html', category=category)


@app.route('/Category/<string:category_name>/')
def showCategory(category_name):
    ''' showCategory() - show a specified category

        @arg category_name - category to view supplied by URL
    '''
    user = getUser()
    category = db.query(Category).filter_by(name=category_name).one()
    categories = db.query(Category).filter_by(parent_id=category.id).all()
    items = db.query(Item).filter_by(
        category_id=category.id).all()
    return render_template('category.html', user=user, items=items,
                           category=category, categories=categories,
                           Item=Item, db=db)


@app.route('/Category/<string:category_name>/Item/new',
           methods=['GET', 'POST'])
def newItem(category_name):
    ''' newItem() - Route for creating a new item

        @arg category_name - category item is under, supplied by URL
    '''
    user = getUser()
    if user is None:  # Make sure user is logged in
        return redirect('/login')
    if request.method == 'POST':  # If post create new item from form data
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       creator=session['username'],
                       category_id=db.query(
                        Category.id).filter_by(
                        name=category_name).all()[0][0])
        db.add(newItem)
        db.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newItem.html')


@app.route('/Category/<string:category_name>/Item/<string:item_name>/edit/',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    ''' editItem() - Edit an existing item

        @arg category_name - category of item is supplied by URL
        @arg item_name - item to edit supplied by URL
    '''
    category_name = URLtoString(category_name)
    item_name = URLtoString(item_name)
    user = getUser()
    if user is None:
        return redirect('/login')
    item = db.query(Item).filter_by(name=item_name).one()
    if item.creator != session['username']:
        return redirect('/Category/' + category_name + '/Item/' + item_name)
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        return redirect(url_for('showItem', category_name=category_name,
                                item_name=item_name))
    else:
        categories = db.query(Category).order_by(Category.name).all()
        return render_template('editItem.html', item=item,
                               categories=categories)


@app.route('/Category/<string:category_name>/Item/<string:item_name>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    ''' deleteItem() - Delete an existing item

        @arg category_name - category of item is supplied by URL
        @arg item_name - item to delete supplied by URL
    '''
    user = getUser()
    item_name = URLtoString(item_name)
    if user is None:  # Check if user is logged on
        return redirect('/login')
    item = db.query(
        Item).filter_by(name=item_name).one()
    if item.creator != session['username']:
        return redirect('/Category/' + category_name)
    if request.method == 'POST':  # If post delete item
        db.delete(item)
        db.commit()
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('deleteItem.html', item=item,
                               category_name=category_name)


@app.route('/Category/<string:category_name>/Item/<string:item_name>/')
def showItem(category_name, item_name):
    ''' showItem() - Display an item

        @arg category_name - category of item is supplied by URL
        @arg item_name - item to display supplied by URL
    '''
    user = getUser()
    category = db.query(Category).filter_by(name=category_name).one()
    item = db.query(Item).filter_by(
        name=item_name).one()
    return render_template('item.html', user=user, item=item,
                           category=category, Item=Item, db=db,
                           session=session)


def getUser():
    ''' getUser() - Get session access token
          to see if user is logged in
    '''
    user = None
    user = session.get('access_token')
    return user


def URLtoString(string):
    ''' URLtoString() - Change category or item from string
      without spaces to string with spaces for database querying

    '''
    string = string.replace('_', ' ')
    string = string.replace('%20', ' ')
    return string


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
