import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def get_All_sook(id):
    stoocks = db.execute("SELECT DISTINCT suck FROM purch WHERE user_id is (?)", id)
    stock = []
    for suck in stoocks:

        s = lookup(suck["suck"])
        shares = db.execute("SELECT sum(share_num) FROM purch WHERE user_id IS (?) AND suck is (?)",
                            id, suck["suck"])[0]["sum(share_num)"]
        if shares <= 0:
            continue
        price = shares * s["price"]
        tmp = {}
        tmp["suck"] = suck["suck"]
        tmp["shares"] = shares
        tmp["cost"] = usd(s["price"])
        tmp["price"] = usd(price)
        stock.append(tmp)
    return stock


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    id = session["user_id"]
    me = db.execute("SELECT * FROM users where id = (?)", id)[0]
    total = 0
    stock = get_All_sook(id)
    for suck in stock:
        num_str = suck["price"][1::]
        total += float(num_str.replace(",", ""))

    return render_template("index.html", stock=stock, me=usd(me["cash"]), total=usd(total + me["cash"]))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        c = request.form.get("symbol")
        k = request.form.get("shares")
        s = lookup(c)
        if not s or not k or not k.isdigit() or int(k) <= 0:
            return apology("wrong input")
        price = int(k) * s["price"]
        id = session["user_id"]
        me = db.execute("SELECT * FROM users where id = (?)", id)[0]
        if (me["cash"] < price):
            return apology("not enough money")

        db.execute("INSERT INTO purch (user_id, status, suck, share_num) VALUES(?, ?, ?, ?)", id, "buy", c, int(k))
        db.execute("UPDATE users SET cash = (?) WHERE id = (?)", me["cash"] - price, id)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    id = session["user_id"]
    stock = db.execute("SELECT * FROM purch WHERE user_id is (?)", id)
    for suck in stock:
        price = lookup(suck["suck"])["price"]
        suck["share_num"] = abs(suck["share_num"])
        suck["total"] = price * suck["share_num"]
    return render_template("history.html", stock=stock)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        c = request.form.get("symbol")
        s = lookup(c)
        if s:
            return render_template("quoted.html", sucks=s, price=usd(s["price"]))
        else:
            return apology("Didn't found")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # if i post request
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        passconf = request.form.get("confirmation")
        if not name or not password or not passconf:
            return apology("empty field")
        Name = db.execute("SELECT * FROM users where username is (?)", name)
        # check if valid name
        if Name:
            return apology("invald name")
        if password != passconf:
            return apology("password doesn't match")
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, generate_password_hash(password))
        # get account
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    # if get request
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # gettint user id
    id = session["user_id"]
    if request.method == "POST":
        c = request.form.get("symbol")
        k = request.form.get("shares")
        s = lookup(c)
        if not s or not k or not k.isdigit() or int(k) <= 0:
            return apology("wrong input")
        # get my account
        me = db.execute("SELECT * FROM users where id = (?)", id)[0]

        price = int(k) * s["price"]
        stock = get_All_sook(id)
        isit = True
        for suck in stock:
            if suck["suck"] == c and int(k) <= suck["shares"]:
                isit = False
                break
        if isit:
            return apology("not enough suck")
        # add new sell purch
        db.execute("INSERT INTO purch (user_id, status, suck, share_num) VALUES(?, ?, ?, ?)", id, "sell", c, int(k) * -1)
        db.execute("UPDATE users SET cash = (?) WHERE id = (?)", me["cash"] + price, id)
        return redirect("/")
    else:
        stock = db.execute("SELECT DISTINCT suck FROM purch WHERE user_id is (?)", id)
        return render_template("sell.html", stock=stock)
