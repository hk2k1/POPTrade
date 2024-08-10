from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,Response,jsonify
)

import os

import datetime

from TLM2008_Project.db import get_db

marketBp = Blueprint('marketplace',__name__,url_prefix='/marketplace')
print("Initializing market.py...")

# @itemBp.route('/')
# def itemPage():
#     return render_template("""Jurassic_World_series""")

@marketBp.route("/")
def mainPage():
    allItemInfo = []
    dbItemInfo = retriveAllItemInfo()
    for stuff in dbItemInfo:
        stuff = dict(stuff)
        stuff['url'] = "/marketplace/marketplaceItem/{}/".format(stuff['item_id'])
        stuff['user_name'] = retrieveUserName(stuff['user_id'])
        stuff['item_image_url'] = stuff['item_image_url'].split(",")[0]
        allItemInfo.append(stuff)     
    #print(allItemInfo)
    return render_template("/marketplace/Marketplace.html",allItemInfo = allItemInfo)

@marketBp.route("/marketplaceItem/<item>/")
def itemPage(item):
    try:
        itemInfoRow = retrieveItemInfo(item)
        itemInfoDict = dict(itemInfoRow)
        itemInfoDict["user_name"] =  retrieveUserName(itemInfoDict["user_id"])
        print(itemInfoDict)
    except:
        print("Error retrieving item info from database")
    
    assetUrlList = itemInfoDict['item_image_url'].split(",")
    userSellingItemList= retrieveUsersSellingItem(itemInfoDict['item_name'])
    for user in userSellingItemList:
        userName = retrieveUserName(user['user_id'])
        user.update({"user_name":userName})
    try:
        userFavouriteItem = isFavoriteItem(session["user_id"],itemInfoDict["item_id"])
    except:
        userFavouriteItem = False
    if userFavouriteItem == True:
        favouriteStatus = 1
    else:
        favouriteStatus = 0

    randomItemList = retrieveRandomItem(8)
    for row in randomItemList:
        row['item_front_image'] = row['item_image_url'].split(',')[0]
        if row['item_catergory'] == "auction":
            row['item_url'] = "/auction/auctionItem/" + str(row['item_id'])
        elif row['item_catergory'] == "market":
            row['item_url'] = "/marketplace/marketplaceItem/" + str(row['item_id'])
    # print(userFavouriteItem)
    # print("Asset URL:")
    # print(assetUrlList)
    # print("Item Info:")
    # print(itemInfoDict)
    # print(randomItemList)
    session.update({"item_id":itemInfoDict["item_id"]})
    session.update({"seller_id":itemInfoDict["user_id"]})
    session.update({"item_name":itemInfoDict["item_name"]})
    print("rendered item name is: {}".format(itemInfoDict['item_name']))
    return render_template('marketplace/marketplaceItem.html',image_urls=assetUrlList,itemInfo = itemInfoDict,userSellingItemList = userSellingItemList,favouriteStatus = favouriteStatus,randomItemList= randomItemList)

@marketBp.route("/marketplaceItem/buyItem/", methods = ['POST'])
def buyItem():
    if request.method == 'POST':
        print("received item name is {}".format(str(request.json['item_name'])))
        userName = retrieveUserName(session["user_id"])
        time =datetime.datetime.now()
        notificationId = str(session["user_id"])+'BUY'+str(request.json['seller_id'])+str(session["item_id"])+str(time)
        message = "{} wants to buy your {}".format(userName,str(request.json['item_name']))
        updateNotificationTable(notificationId,request.json['seller_id'],"transaction",time,session["user_id"],message)
        return Response(status = 200, mimetype = 'application/json')
    
@marketBp.route("/marketplaceItem/favItem/", methods = ['POST'])
def favItem():
    if request.method == 'POST':
        user_id = session['user_id']
        item_id = session['item_id']
        print("user_id: {} item_id: {}".format(user_id,item_id))
        favStatus = isFavoriteItem(user_id,item_id)
        print(favStatus)
        if not favStatus:           
            updateFavTable(user_id,item_id)
            data = {"status":True}
            # return Response(data,status = 200, content_type = 'application/json')
            return jsonify(data)
        else:
            deleteFavoriteItem(user_id,item_id)
            data = {"status":False}
            # return Response(data,status = 200, content_type = 'application/json')
            return jsonify(data)

def retriveAllItemInfo():
    db = get_db()
    itemInfo = db.execute(
        "SELECT * FROM listed_item where item_catergory = 'market'"
    ).fetchall()
    return itemInfo

def retrieveItemInfo(item):
    db = get_db()
    itemInfo = db.execute(
        "SELECT * FROM listed_item WHERE item_id = ?",(item,)
    ).fetchone()
    return  itemInfo

def retrieveUserName(userId):
    db = get_db()
    userNameQuery = db.execute(
        "select username from user_info where user_id = ?",(userId,)
    ).fetchone()
    userName = userNameQuery[0]
    #userName = userNameQuery["username"]
    return userName

def retrieveUsersSellingItem(item_name):
    db = get_db()
    userSellingItemQuery = db.execute(
        "SELECT user_id,item_starting_price FROM listed_item WHERE item_name= ?",(item_name,)
    ).fetchall()
    userSellingItem = []
    for stuff in userSellingItemQuery:
        userSellingItem.append(dict(stuff))
    return userSellingItem

def updateNotificationTable(notification_id, seller_id,type,time, buyer_id,message):
    db = get_db()
    db.execute(
        "INSERT INTO notification (notification_id,user_id,notification_type,logged_timing,sender_id,message) VALUES (?, ?, ?,?,?,?)",
        (notification_id, seller_id,type,time, buyer_id,message)
    )
    db.commit()

def updateFavTable(user_id,item_id):
    db = get_db()
    db.execute(
        "INSERT INTO user_likes (user_id,item_id) VALUES (?, ?)",
        (user_id,item_id)
    )
    db.commit()

def deleteFavoriteItem(user_id,item_id):
    db = get_db()
    db.execute(
        "DELETE FROM user_likes WHERE user_id = ? AND item_id=?",(user_id,item_id,)
    )
    db.commit()

def isFavoriteItem(user_id,item_id):
    db = get_db()
    # print("{}.{}".format(user_id,item_id))
    favItemQuery = db.execute(
        "SELECT CASE WHEN EXISTS(SELECT 1 FROM user_likes WHERE user_id = ? AND item_id = ?) THEN true ELSE false END as exist;",(user_id,item_id,)
    ).fetchone()
    db.commit()
    favItem = dict(favItemQuery)
    print(favItem)
    if favItem['exist']:
        return True
    else:
        return False
    
def retrieveRandomItem(number):
    db = get_db()
    itemList = []
    cur = db.execute('SELECT * FROM listed_item ORDER BY RANDOM() LIMIT ?',(number,)).fetchall()
    for item in cur:
        itemList.append(dict(item))
    return itemList
    