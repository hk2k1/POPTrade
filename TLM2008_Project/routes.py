from flask import Flask, render_template, Blueprint

from TLM2008_Project.db import get_db
#from . import db
#from . import auth

#main = Flask(__name__)
main = Blueprint('main',__name__)
#main.config['SQLALCHEMY_DATABASE_URI']='sqlite:///poptrade.db'
#db = SQLAlchemy(main)


# class user(db.Model):
#     uid = db.Column(db.Integer,primary_key=True)
#     content = db.Column()
#what does the @main.route() do? well, the @ symbol is a function extender for the function "main". So when main.route() is passed with "/", the function index() is called as an extension

@main.route("/")
def index():
    #TODO: load random item from database
    itemList = retrieveRandomItem(3)
    print(itemList)
    for row in itemList:
        row['item_front_image'] = row['item_image_url'].split(',')[0]
        if row['item_catergory'] == "auction":
            row['item_url'] = "/auction/auctionItem/" + str(row['item_id'])
        elif row['item_catergory'] == "market":
            row['item_url'] = "/marketplace/marketplaceItem/" + str(row['item_id'])
    itemList2 = retrieveRandomItem(4)
    for row in itemList2:
        row['item_front_image'] = row['item_image_url'].split(',')[0]
        if row['item_catergory'] == "auction":
            row['item_url'] = "/auction/auctionItem/" + str(row['item_id'])
        elif row['item_catergory'] == "market":
            row['item_url'] = "/marketplace/marketplaceItem/" + str(row['item_id'])
    return render_template("index.html",itemList=itemList,itemList2 = itemList2)

# @main.route("/auction")
# def auction():
#     return render_template("/auction/auctionMain.html") #handled by auction.py now

@main.route("/register")
def register():
    return render_template("/auth/register.html")



@main.route("/login")
def loginpage():
    return render_template("/auth/login.html")

@main.route("/aboutus")
def aboutus():
    return render_template("/aboutus.html")
#db.init_app(main)

#main.register_blueprint(auth.bp)

if __name__ == "__main__":
    main.run(debug=True)


def retrieveRandomItem(number):
    db = get_db()
    itemList = []
    cur = db.execute('SELECT * FROM listed_item ORDER BY RANDOM() LIMIT ?',(number,)).fetchall()
    for item in cur:
        itemList.append(dict(item))
    return itemList
    