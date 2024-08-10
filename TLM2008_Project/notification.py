from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,Response
)

import os

import datetime

from TLM2008_Project.db import get_db

notificationBp = Blueprint('notification',__name__,url_prefix='/notification')
print("Initializing notification.py...")

@notificationBp.route("/")
def mainPage():
    notifList = getAllNotification(session['user_id'])
    print(notifList)
    return render_template("/notification/notification.html",notifList = notifList)

@notificationBp.route("/getNotification",methods=['POST'])
def getNotification():
    user_id = request.json['user_id']
    print("user" + user_id)
    if user_id == " ":
        response = Response(
            response = " ",
            status = 200,
            mimetype='text/plain',
        )
        return response
    notifList = getAllNotification(user_id)
    if notifList.__len__() == 0:
        response = Response(
            response = "0",
            status = 200,
            mimetype='text/plain',
        )
        return response
    else:
        response = Response(
        response = str(notifList.__len__()),
        status = 200,
        mimetype='text/plain',
        )
        return response
    
@notificationBp.route("/reply",methods=['POST'])
def reply():
    notifId = request.form['id']
    print(notifId)
    clearNotification(notifId)
    return redirect(url_for('auth.message'))


def getAllNotification(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM notification WHERE user_id = ?",(user_id,))
    notifList = []
    for row in cursor.fetchall():
        notifList.append(dict(row))
    return notifList

def clearNotification(notifId):
    db = get_db()
    db.execute(
        'DELETE FROM notification WHERE notification_id = ?',
        (notifId,)
    )
    db.commit()