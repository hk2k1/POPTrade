from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

itemBp = Blueprint('item',__name__,url_prefix='/item')
print("Initializing auction.py...")

# @itemBp.route('/')
# def itemPage():
#     return render_template("""Jurassic_World_series""")

@itemBp.route("/Jurassic_World_series")
def Jurassic_World_series():
    return render_template("/item/Jurassic_World_series.html")
