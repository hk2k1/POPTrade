#this is the server code that handles routing and services for auth page

import functools

import os

from datetime import timedelta

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,app
)
from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.utils import secure_filename

from TLM2008_Project.db import get_db

#define blueprint to register with app upon startup
bp = Blueprint('auth', __name__, url_prefix='/auth')
print("Initializing auth.py...")

# #function extension to route auth request for register resource
# @bp.route('/register', methods=('GET', 'POST'))
# def register():
#     #if post request is received from client, process register service. Else renders register.html for client
#     if request.method == 'POST':
#         #retrieve username and password field from form
#         username = request.form['username']
#         password = request.form['password']
#         #create database object to intereact with sqlite db
#         db = get_db()
#         error = None

#         #validates field
#         if not username:
#             error = 'Username is required.'
#         elif not password:
#             error = 'Password is required.'

#         if error is None:
#             try:
#                 #if details not used, create entry into database, else return error to client
#                 db.execute(
#                     "INSERT INTO user (username, password) VALUES (?, ?)",
#                     (username, generate_password_hash(password)),
#                 )
#                 db.commit()
#             except db.IntegrityError:
#                 error = f"User {username} is already registered."
#             else:
#                 #redirects client to login page
#                 return redirect(url_for("auth.login"))

#         flash(error)

#     return render_template('auth/register.html')

# #function extension to route auth request for login resource
# @bp.route('/login', methods=('GET', 'POST'))
# def login():
#     #if post request is received from client, process login service. Else renders login.html for client
#     if request.method == 'POST':
#         #retrieve username and password field from form
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None
#         #executes query for user, if user does not exist, return error msg to client
#         user = db.execute(
#             'SELECT * FROM user WHERE username = ?', (username,)
#         ).fetchone()

#         if user is None:
#             error = 'Incorrect username.'
#         elif not check_password_hash(user['password'], password):
#             error = 'Incorrect password.'
#         #once no error, means user is authenticated and redirects user to front page with session created for user
#         if error is None:
#             session.clear()
#             session['user_id'] = user['id']
#             return redirect(url_for('main.index'))

#         flash(error)

#     return render_template('auth/login.html')

@bp.route('/login-register',methods =('GET','POST'))
def login_register():
    if request.method == 'POST':
        state = request.form['state']
        #email = request.form['email']
        

        if state == 'login':   #if email is not send with form, client is requesting for login service
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            error = None
            #executes query for user, if user does not exist, return error msg to client
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'
            #once no error, means user is authenticated and redirects user to front page with session created for user
            if error is None:
                session.clear()
                session['user_id'] = user['id']
                userUrl = "/auth/user"+str(user['id'])
                return redirect(url_for('main.index',values=userUrl))

            flash(error)

        elif state == 'register' :   #if email is send with form, client is requesting for registration service
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            #create database object to intereact with sqlite db
            db = get_db()
            error = None

            #validates field
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not email:
                error = 'Email is requried.'

            if error is None:
                try:
                    #if details not used, create entry into database, else return error to client
                    db.execute(
                        "INSERT INTO user (username, password,email) VALUES (?, ?,?)",
                        (username, generate_password_hash(password),email),
                    )
                    userId = db.execute(
                        'SELECT * FROM user WHERE username = ?', (username,)
                    ).fetchone()[0]
                    db.execute(
                        "INSERT INTO user_info (user_id,username,userRating,userTotalListing,email,contactNo) VALUES (?,?,?,?,?,?)",
                        (userId,username,0,0,email,0),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    #redirects client to login page
                    #return redirect(url_for("auth.userCreated"))
                    return redirect(request.url)

            flash(error)
    return render_template('auth/login_register.html')

@bp.route('/user/<userId>/',methods =('GET','POST'))
def userProfile(userId):
    if authenticateUser(userId): #check if user is allowed to access page
        userInfo = fetchUserInfo(userId)
        if userInfo['profileImgUrl'] == None:
            userInfo['profileImgUrl'] = "img/profile_image/profile-default.jpg"
        # userListing = fetchUserListing(userId)
        # for row in userListing:
        #     row["item_edit_url"] = "/listing/editListing/"+str(row["item_id"])
        #     row["item_delete_url"] = "/listing/deleteListing/"+str(row["item_id"])
        #     row["item_front_image"] = row['item_image_url'].split(",")[0]

            
        #print(userListing)
        userLikesId = retriveUserLikes(userId)
        userLikes = []
        for row in userLikesId:
            itemInfo = retrieveItemInfo(row['item_id'])
            row['item_name'] = itemInfo['item_name']
            row['item_description'] = itemInfo['item_description']
            row['item_image_url'] = itemInfo['item_image_url'].split(",")[0]
            row['item_catergory'] = itemInfo['item_catergory']
            print(row)
            userLikes.append(row)
        return render_template('auth/profilepage.html',userInfo = userInfo,userLikes = userLikes)
    else:
        return redirect(url_for('main.index'))
    
@bp.route('/user/listing',methods =('GET','POST'))
def userListing():
    userId = session['user_id']
    if authenticateUser(userId): #check if user is allowed to access page
        userInfo = fetchUserInfo(userId)
        if userInfo['profileImgUrl'] == None:
            userInfo['profileImgUrl'] = "img/profile_image/profile-default.jpg"
        userListing = fetchUserListing(userId)
        for row in userListing:
            row["item_edit_url"] = "/listing/editListing/"+str(row["item_id"])
            row["item_delete_url"] = "/listing/deleteListing/"+str(row["item_id"])
            row["item_front_image"] = row['item_image_url'].split(",")[0]
            if row["item_catergory"] == "auction":
                row["item_url"] = "/auction/auctionItem/"+str(row["item_id"])
            elif row["item_catergory"] == "market":
                row["item_url"] = "/marketplace/marketplaceItem/"+str(row["item_id"])
        return render_template('auth/userpage.html',userInfo = userInfo,userListing=userListing)

@bp.route('/edit',methods=('GET',))
def editProfile():
    db=get_db()
    userInfo = db.execute(
        'SELECT * FROM user_info WHERE user_id = ?', (session['user_id'],)
    ).fetchone()
    return render_template('auth/edit_profile.html',userInfo = userInfo)

@bp.route('/edit',methods=('POST',))
def editProfilePost():
    username = request.form['username']
    email = request.form['email']
    contactNo = request.form['contactNo']
    userId = session['user_id']
    profileImg = uploadFile(request.files['image'])
    db = get_db()
    error = None
    if not username:
        error = 'Username is required.'
    elif not email:
        error = 'Email is required.'
    elif not contactNo:
        error = 'Contact No is required.'
    if error is None:
        try:
            db.execute(
                "UPDATE user_info SET username = ?, email = ?, contactNo = ?, profileImgUrl = ? WHERE user_id = ?",
                (username,email,contactNo,profileImg,userId),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered."
        else:
            #redirects client to login page
            #return redirect(url_for("auth.userCreated"))
            return redirect(url_for('auth.userListing',userId = userId))

    flash(error)
    return redirect(url_for('auth.editProfile'))

@bp.route('/message',methods=('GET',))
def message():
    db = get_db()
    userInfo = db.execute(
        'SELECT * FROM user_info WHERE user_id = ?', (session['user_id'],)
    ).fetchone()
    if userInfo['profileImgUrl'] == None:
        userInfo['profileImgUrl'] = "img/profile_image/profile-default.jpg"
    return render_template('/chat/chat.html',userInfo = userInfo)

#before app loads, check if user is login and session is created. If user is login, session is created, else proceeds with no user session
@bp.before_app_request
def load_logged_in_user():
    session.permanent = True
    bp.permenent_session_lifetime = timedelta(minutes=30)
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#function extension to route auth request for logout resource
@bp.route('/logout')
def logout():
    #clear user session
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login-register'))

        return view(**kwargs)

    return wrapped_view

def fetchUserInfo(userId):
    user = get_db().execute(
            'SELECT * FROM user_info WHERE user_id = ?', (userId,)
        ).fetchone()
    user = dict(user)
    return user

def fetchUserListing(userId):
    userListing = []
    userListingQuery = get_db().execute(
            'SELECT * FROM listed_item WHERE user_id = ?', (userId,)
        ).fetchall()
    for row in userListingQuery:
        row = dict(row)
        userListing.append(row)
    return userListing

def authenticateUser(parsedUserId):
    user_id = session.get('user_id')
    if user_id == int(parsedUserId):
        return True
    else:
        return False
    
def uploadFile(file):#filename is a list of file name from form request, returns a string of file path
    if file.filename == '':
        flash('No selected file')
        return "no file selected"
    if file:
        filename = secure_filename(file.filename)
        if (os.path.join('TLM2008_Project/static/img/profile_image/'+filename)) not in os.listdir('TLM2008_Project/static/img/profile_image'):
            file.save(os.path.join('TLM2008_Project/static/img/profile_image/'+filename))
        else:
            flash('File already exists')
            return "file already exists"
    return os.path.join('img/profile_image/'+filename)

def retriveUserLikes(userId):
    userLikes = []
    userLikesQuery = get_db().execute(
            'SELECT * FROM user_likes WHERE user_id = ?', (userId,)
        ).fetchall()
    for row in userLikesQuery:
        row = dict(row)
        userLikes.append(row)
    return userLikes

def retrieveItemInfo(item):
    db = get_db()
    itemInfo = db.execute(
        "SELECT * FROM listed_item WHERE item_id = ?",(item,)
    ).fetchone()
    return  itemInfo