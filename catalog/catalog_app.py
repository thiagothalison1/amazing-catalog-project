import database
import json
from helpers import utils
from google.oauth2 import id_token
from google.auth.transport import requests as google_auth_requests
from flask import (Flask, render_template, request, redirect, jsonify, url_for,
                   flash, make_response)
from flask import session as user_session

GOOGLE_CLIENT_ID = json.loads(
  open('google_client_secret.json', 'r').read())['web']['client_id']

app = Flask(__name__)


@app.context_processor
def inject_login_state():
    return dict(user_session=user_session)


@app.route('/')
@app.route('/category/')
def index():
    categories = database.query.get_categories()
    latest_items = database.query.get_latest_items()
    return render_template('category.html', categories=categories,
                           latest_items=latest_items)


@app.route('/category/new', methods=['GET', 'POST'])
def create_category():
    if not user_session.get('username'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['submit_button'] == 'Create':
            database.query.add_category(request.form['new_category_name'],
                                        request.form['new_category_desc'])
        return redirect(url_for('index'))
    else:
        return render_template('add_category.html')


@app.route('/category/<int:category_id>', methods=['GET'])
def showItems(category_id):
    categories = database.query.get_categories()
    selected_category = filter(lambda category: category.id == category_id,
                               categories)
    items = database.query.get_category_items(category_id)
    return render_template('items.html',
                           selected_category=selected_category[0],
                           categories=categories,
                           items=items)


@app.route('/category/<int:category_id>/item/<int:item_id>', methods=['GET'])
def showItem(category_id, item_id):
    categories = database.query.get_categories()
    selected_category = filter(lambda category: category.id == category_id,
                               categories)
    items = database.query.get_category_items(category_id)
    selected_item = filter(lambda item: item.id == item_id, items)
    user = database.query.get_user(user_session.get('username'))
    if user is not None:
        is_owner = selected_item[0].validate_user(user.id)
    else:
        is_owner = False
    return render_template('item.html', selected_category=selected_category[0],
                           categories=categories,
                           selected_item=selected_item[0],
                           items=items,
                           is_owner=is_owner)


@app.route('/category/<int:category_id>/item/new', methods=['GET', 'POST'])
def create_item(category_id):
    if not user_session.get('username'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['submit_button'] == 'Create':
            user = database.query.get_user(user_session.get('username'))
            database.query.add_item(request.form['new_item_name'],
                                    request.form['new_item_desc'],
                                    category_id, user.id)
        return redirect(url_for('showItems', category_id=category_id))
    else:
        category = database.query.get_category(category_id)
        return render_template('add_item.html', category=category)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def edit_item(category_id, item_id):
    if not user_session.get('username'):
        return redirect(url_for('login'))
    item = database.query.get_item(item_id)
    user = database.query.get_user(user_session.get('username'))
    if item.validate_user(user.id) is False:
        response = make_response(json.dumps('Unauthorized user!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if request.method == 'POST':
        if request.form['submit_button'] == 'Edit':
            database.query.edit_item(request.form['new_item_name'],
                                     request.form['new_item_desc'],
                                     item_id)
        return redirect(url_for('showItem', category_id=category_id,
                                item_id=item_id))
    else:
        category = database.query.get_category(category_id)
        return render_template('edit_item.html', category=category, item=item)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def delete_item(category_id, item_id):
    if not user_session.get('username'):
        return redirect(url_for('login'))
    item = database.query.get_item(item_id)
    user = database.query.get_user(user_session.get('username'))
    if item.validate_user(user.id) is False:
        response = make_response(json.dumps('Unauthorized user!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if request.method == 'POST':
        if request.form['submit_button'] == 'Delete':
            database.query.delete_item(item_id)
            return redirect(url_for('showItems', category_id=category_id))
        return redirect(url_for('showItem', category_id=category_id,
                                item_id=item_id))
    else:
        category = database.query.get_category(category_id)
        item = database.query.get_item(item_id)
        return render_template('delete_item.html', category=category,
                               item=item)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if user_session.get('username'):
        return redirect(url_for('index'))
    if request.method == 'GET':
        state = utils.gen_random_text(32)
        user_session['state'] = state
        return render_template('login.html', STATE=state, login_page=True)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Signup':
            user = database.query.get_user(request.form['username'])

            if user:
                return render_template('sign_up.html', existing_user=True)

            user_info = {
                "name": request.form['full_name'],
                "username": request.form['username'],
                "password": request.form['password']
            }

            user = database.query.create_user(user_info=user_info,
                                              is_sign_up=True)

            user_session['name'] = user.name
            user_session['username'] = user.username
            user_session['user_id'] = user.id

            return redirect(url_for('index'))
        return redirect(url_for('index'))
    else:
        return render_template('sign_up.html')


@app.route('/signin', methods=['POST'])
def signin():
    if request.args.get('state') != user_session.get('state'):
        response = make_response(json.dumps('Permission Denied!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        credentials = request.get_json()
        user = database.query.get_user(credentials.get('username'))
        if user and user.verify_password(credentials.get('password')):
            user_session['name'] = user.name
            user_session['username'] = user.username
            user_session['user_id'] = user.id
            response = make_response(json.dumps('User Logged in.'), 200)
        else:
            response = make_response(json.dumps('Permission Denied!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    return redirect(url_for('index'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != user_session['state']:
        response = make_response(json.dumps('Permission Denied!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        try:
            user_token = request.data
            g_auth_request = google_auth_requests.Request()
            idinfo = id_token.verify_oauth2_token(user_token,
                                                  g_auth_request,
                                                  GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                raise ValueError('Invalid User Token.')

            user_g_id = idinfo['sub']

            if (user_session.get('user_g_id') is not None and
                    user_session['user_g_id'] == user_g_id):
                message = json.dumps('Current user is already connected.')
                response = make_response(message, 200)
                response.headers['Content-Type'] = 'application/json'
                return response

            user_session['user_g_id'] = user_g_id
            user_session['name'] = idinfo['name']
            user_session['picture'] = idinfo['picture']
            user_session['username'] = idinfo['email']

            user = database.query.get_user(user_session['username'])
            if not user:
                user = database.query.create_user(user_info=user_session,
                                                  is_sign_up=False)
            user_session['user_id'] = user.id

            response = make_response(json.dumps('User Logged in.'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response

        except ValueError:
            response = make_response(json.dumps('Wrong issuer.'), 500)
            response.headers['Content-Type'] = 'application/json'
            return response


@app.route('/logout', methods=['POST'])
def logout():
    username = user_session.get('username')
    if username is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print(user_session)
        if user_session.get('state'):
            del user_session['state']
        if user_session.get('user_g_id'):
            del user_session['user_g_id']
        if user_session.get('name'):
            del user_session['name']
        if user_session.get('picture'):
            del user_session['picture']
        if user_session.get('username'):
            del user_session['username']
        if user_session.get('user_id'):
            del user_session['user_id']

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = utils.gen_random_text(32)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
