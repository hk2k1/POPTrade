from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.utils import secure_filename

import os

import datetime as dt

from TLM2008_Project.db import get_db

listingBp = Blueprint('listingBp',__name__,url_prefix='/listing')
print("Initializing listing.py...")

@listingBp.route("/createListing/",methods=["GET"])
def createListing():
    itemCatalog = retriveItemCatalog()
    user_id = session.get('user_id')
    return render_template("/listing/createListing.html",user_id=user_id,itemCatalog = itemCatalog)

@listingBp.route("/createListing/", methods=["POST"])
def createListingPost():
    itemEndDate = -1
    itemCurrentPrice = -1
    itemName = request.form['item-name']
    userId = session.get("user_id")
    itemDescription = request.form['item-description']
    itemPrice = request.form['price']
    itemCatergory = request.form['sell-type']
    # itemImageUrl = request.form['itemImageUrl']
    itemSeries = request.form['series']
    itemQuantity = request.form['quantity']
    item_image_url = uploadFile(request.files.getlist('image'))
    #item_image_url = uploadFile(request.files)
    if itemCatergory == "auction":
        timeNow = dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d %H:%M:%S')
        itemEndDate = dt.datetime.strptime(timeNow,'%Y-%m-%d %H:%M:%S') + dt.timedelta(days=14)
        itemCurrentPrice = itemPrice
    
    db = get_db()
    query = db.execute(
        'select max(item_id) from listed_item'
    )
    itemId = query.fetchone()[0] + 1
    db.execute(
        'insert into listed_item (item_id, item_name, user_id, item_description, item_starting_price,item_current_price,item_end_date, item_catergory, item_image_url, series,quantity) values (?,?,?,?,?,?,?,?,?,?,?)',
        (itemId, itemName, userId, itemDescription, itemPrice,itemCurrentPrice,itemEndDate, itemCatergory, item_image_url, itemSeries,itemQuantity)
    )
    db.commit()
    if itemCatergory == "auction":
        return redirect(url_for('auction.itemPage',item=itemId))
    elif itemCatergory == "market":
        return redirect(url_for('marketplace.itemPage',item=itemId))


@listingBp.route("/editListing/<item_id>",methods = ["GET"])
def editListing(item_id):
    itemInfo = dict(retrieveItemInfo(item_id))
    itemCatalog = retriveItemCatalog()
    postUrl = "/listing/editListing/"+item_id
    itemInfo['front_image'] = itemInfo['item_image_url'].split(',')[0]
    return render_template("/listing/editListing.html",itemInfo = itemInfo,itemCatalog=itemCatalog,postUrl = postUrl)

@listingBp.route("/editListing/<item_id>",methods = ["POST"])
def editListingPost(item_id):
    itemName = request.form['item-name']
    userId = session.get("user_id")
    itemDescription = request.form['item-description']
    itemPrice = request.form['price']
    # itemImageUrl = request.form['itemImageUrl']
    itemSeries = request.form['series']
    itemQuantity = request.form['quantity']
    item_image_url = uploadFile(request.files.getlist('image'))
    #item_image_url = uploadFile(request.files)
    db = get_db()
    db.execute(
        'update listed_item set item_name = ?, item_description = ?, item_starting_price = ?, item_image_url = ?, series = ?, quantity = ? where item_id = ?',
        (itemName, itemDescription, itemPrice, item_image_url, itemSeries,itemQuantity, item_id)
    )
    db.commit()
    return redirect(url_for('auth.userListing',userId = userId))

@listingBp.route("/deleteListing/<item_id>",methods = ["POST"])
def deleteListing(item_id):
    userId = session.get("user_id")
    print("ayo im deleting")
    db = get_db()
    db.execute(
        'delete from listed_item where item_id = ?',
        (item_id,)
    )
    db.execute(
        'delete from auction_bids where item_id = ?',(item_id,)
    )
    db.execute(
        'delete from user_likes where item_id = ?',(item_id,)
    )
    db.commit()
    return redirect(url_for('auth.userListing',userId = userId))

def uploadFile(fileNames):#filename is a list of file name from form request, returns a string of file path
    fileList = []
    for file in fileNames:
        if file.filename == '':
            flash('No selected file')
            return "no file selected"
        if file:
            filename = secure_filename(file.filename)
            distinct_filename = "{}_{}{}__{}".format(session.get('user_id'),dt.datetime.now().month,dt.datetime.now().year, filename)

            if (os.path.join('TLM2008_Project/static/img/listing_image/'+filename)) not in os.listdir('TLM2008_Project/static/img/listing_image'):
                file.save(os.path.join('TLM2008_Project/static/img/listing_image/'+distinct_filename))
                fileList.append(os.path.join('img/listing_image/'+distinct_filename))
            else:
                flash('File already exists')
                return "file already exists"
    fileListString = ','.join(fileList)
    return fileListString
            
def authenticateUser(parsedUserId):
    user_id = session.get('user_id')
    if user_id == int(parsedUserId):
        return True
    else:
        return False
    
def retrieveItemInfo(item):
    db = get_db()
    itemInfo = db.execute(
        "SELECT * FROM listed_item WHERE item_id = ?",(item,)
    ).fetchone()
    return  itemInfo

def retriveItemCatalog():
    db = get_db()
    itemCatalog = []
    query = db.execute(
        'select * from item_catalog'
    ).fetchall()
    for row in query:
        itemCatalog.append(row[0])
    return itemCatalog