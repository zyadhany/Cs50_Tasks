import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_file
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, is_valid_image
from datetime import date
from PIL import Image

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///DataBase.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
  
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    id = session["user_id"]
    me = db.execute("SELECT * FROM users WHERE id is (?)", id)[0]
    if request.method == "POST":
        about = request.form.get("about")
        image = request.files.get("image")
        print(about)
        db.execute("UPDATE users SET about = (?) WHERE id = (?)", about, id)
        if not is_valid_image(image):
            return redirect("/profile")
        image.save(f'./static/images/user_image/{id}.png')
        return redirect("/profile")
    pro_id = request.args.get("id")
    if not pro_id:
        pro_id = id
    posts = get_post(pro_id)
    him = db.execute("SELECT * FROM users WHERE id is (?)",pro_id)[0]
    if not pro_id or int(pro_id) == int(id) or not him:
        return render_template("MyProfile.html", me = me, posts=posts)
    return render_template("Profile.html", me = me, him=him, posts=posts)


@app.route("/")
@login_required
def index():
    id = session["user_id"]
    me = db.execute("SELECT * FROM users WHERE id is (?)", id)[0]
    posts = get_post('*')
    return render_template("index.html", posts=posts, me=me)

#like & dislike
@app.route("/like", methods=["POST"])
@login_required
def like():
    id = session["user_id"]
    post_id = request.form.get("id")
    db.execute("INSERT INTO post (user_id, post_id) VALUES(?, ?)", id, post_id)
    return redirect('/')

@app.route("/dislike", methods=["POST"])
@login_required
def dislike():
    id = session["user_id"]
    post_id = request.form.get("id")
    db.execute("DELETE FROM post WHERE user_id = (?) and post_id = (?)",id,post_id)
    return redirect('/')



# upload/del posts

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    id = session["user_id"]
    text = request.form.get('text')
    image = request.files["image"]
    dateaa = 1

    if not is_valid_image(image):
            return redirect("/profile")
    
    db.execute("INSERT INTO posts (user_id, text, date) VALUES(?, ?, ?)"
                , id, text, date.today().strftime("%d/%m/%Y"))
    n = db.execute("SELECT max(id) from posts")[0]['max(id)']
    image.save(f'./static/images/post_images/{n}.png')

    return redirect("/profile")

@app.route("/delete", methods=["POST"])
@login_required
def delete_Post():
    id = session["user_id"]
    post_id = request.form.get("id")
    post = db.execute("SELECT * FROM posts where id is (?)",post_id)[0]
    if post["user_id"] != id:
        return redirect("/")
    db.execute("DELETE FROM posts WHERE id = (?)",post_id)
    os.remove(f'./static/images/post_images/{post_id}.png')
    return redirect("/")


# Login & Register

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        passconf = request.form.get("confirm")
        if not name or not password or not passconf:
            return render_template("register.html",message="Empty field")
        Name = db.execute("SELECT * FROM users where username is (?)", name)
        if Name:
            return render_template("register.html",message="invalid name")
        if password != passconf:
            return render_template("register.html",message="password doesn't match")
        
        db.execute("INSERT INTO users (username, password_hash) VALUES(?, ?)", name, generate_password_hash(password))
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        id = rows[0]["id"]
        session["user_id"] = id
        image = Image.open('./static/images/icons/user.png')
        image.save(f'./static/images/user_image/{id}.png')
        return redirect("/")
    
    return render_template("register.html") 


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        if not name or not password:
            return render_template("login.html",message="Empty field")
        Name = db.execute("SELECT * FROM users where username = (?)",name)
        if not Name or not check_password_hash(Name[0]["password_hash"], password):
            return render_template("login.html",message="invalid username and/or password ")
        session["user_id"] = Name[0]["id"]
        return redirect("/")
    return render_template("login.html") 

# get all posts

def get_post(s):
    id = session["user_id"]
    if s == '*':
        posts = db.execute("SELECT * FROM posts")
    else:
        posts = db.execute("SELECT * FROM posts where user_id is (?)", s)
    for post in posts:
        post["name"] = db.execute("SELECT * FROM users Where id is (?)",post['user_id'])[0]['username']
        if not post['text']:
            post['text'] = " "
        post['like'] = db.execute("SELECT count(*) from post where post_id is (?)",post['id'])[0]['count(*)']
        arr = db.execute("SELECT * from post where post_id is (?) AND user_id is(?)", post['id'], id)
        post['islike'] = len(arr)
    return posts