#this is the server code that handles routing and services for auction page

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)
import os

from TLM2008_Project.db import get_db
import datetime

#define blueprint to register with app upon startup
auctionBp = Blueprint('auction',__name__,url_prefix='/auction')
print("Initializing auction.py...")

#function extension to route auction request for render of auction front page
@auctionBp.route('/')
def mainPage():
    allItemInfo = []
    dbItemInfo = retriveAllItemInfo()
    for stuff in dbItemInfo:
        stuff = dict(stuff)
        stuff['url'] = "/auction/auctionItem/{}/".format(stuff['item_id'])
        stuff['front_image_url'] = stuff['item_image_url'].split(",")[0]
        allItemInfo.append(stuff)

    return render_template('auction/auctionMain.html',allItemInfo=allItemInfo)
    # return render_template('auction/auctionMain.html')

#function extension to route auction item request and render images of the item series for auctionItem.html
@auctionBp.route('/auctionItem/<item>/') #<item> is a variable that stores the last resource request from client and is passed into function as an argument
def itemPage(item):
    try:
        itemInfoRow = retrieveItemInfo(item)
        itemInfoDict = dict(itemInfoRow)
        print(itemInfoDict)
    except:
        print("Error retrieving item info from database")
    itemInfoDict["item_time_left"] = checkTimeLeft(itemInfoDict["item_end_date"])
    if itemInfoDict["item_time_left"] == "Expired":
        itemExpired = True
    else:
        itemExpired = False
    
    assetUrlList = itemInfoDict['item_image_url'].split(",") #split the string of image urls into a list of urls
    session.update({"item_id":itemInfoDict["item_id"]})
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

    print(assetUrlList)
    return render_template('auction/auctionItem.html',image_urls=assetUrlList,itemInfo = itemInfoDict,itemExpired=itemExpired,favouriteStatus=favouriteStatus,randomItemList = randomItemList)#url list is iterated inside the html file using python scripts, view auctionItem.html to see more

@auctionBp.route('/auctionItem/bid/<item>/',methods=('GET', 'POST'))
def bidPage(item):
    print("Bid page is accessed by user: "+request.form['bidder'])
    if(request.form['bidder'] =="Guest"):
        print("Redirecting to login page...")
        return redirect(url_for('auth.login_register'))
    if request.method == 'POST':
        username = request.form['bidder']
        bidValue = request.form['bidValue']
        item_id = request.form['item_id']
        print("Bid value of: "+bidValue + " is received from user: "+username)
        transactionDate = datetime.datetime.now()
        auctionId = item+username+str(transactionDate)
        db = get_db()
        try:
            #if details not used, create entry into database, else return error to client
            db.execute(
                "INSERT INTO auction_bids (auction_id, user_id, bid_amount, transaction_date,item_id) VALUES (?, ?, ?, ?,?)",
                (auctionId,username, bidValue, transactionDate,item_id),
            )
            db.commit()
            updateCurrentBids(item_id,bidValue)
            flash("Bid successfully placed!")
            return redirect(url_for('auction.itemPage',item=item))
        except db.DataError:
            error = f"There's an error with the database."
        flash(error)
        
    return render_template('auction/bid.html')

@auctionBp.route("/auctionItem/favItem/", methods = ['POST'])
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

def retrieveItemInfo(item):
    db = get_db()
    itemInfo = db.execute(
        "SELECT * FROM listed_item WHERE item_id = ?",(item,)
    ).fetchone()
    return itemInfo

def retriveAllItemInfo():
    db = get_db()
    itemInfo = db.execute(
        "SELECT * FROM listed_item where item_catergory = 'auction'"
    ).fetchall()
    return itemInfo

def sumCurrentBids(item):
    db = get_db()
    sumOfBids = db.execute(
        "SELECT SUM(bid_amount) FROM auction_bids WHERE item_id = ?",(item,)
    ).fetchone()
    #print("retrieved values: " + str(sumOfBids[0]))
    return sumOfBids[0]

def updateCurrentBids(itemId,amount):
    db = get_db()
    currentPrice = db.execute(
        "SELECT item_current_price from listed_item WHERE item_id = ?",(itemId,)
    ).fetchone()
    updatePrice = int(currentPrice[0]) + int(amount)
    db.execute(
        "UPDATE listed_item SET item_current_price = ? WHERE item_id = ?",(updatePrice,itemId)
    )
    db.commit()

def checkTimeLeft(time):
    timeLeft = datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S') - datetime.datetime.now()
    if(timeLeft < datetime.timedelta(0)):
        return "Expired"
    else:
        days = timeLeft.days
        hours = timeLeft.seconds//3600
        timeLeft_str = str(days)+" days "+str(hours)+" hours"
        return timeLeft_str
    
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