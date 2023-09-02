# SagedBucks
#### Video Demo:  https://www.youtube.com/watch?v=hjblwrCX0IA
#### Description:
SagedBucks is a website that allows users to create accounts and share images with the public, similar to Instagram.

The main files and folders are:

- app.py: This is the main Python file that contains the logic and routes for the website. Each route has a corresponding function that handles the requests and responses.
- helpers.py: This file contains two helper functions:
  - login_required: This function checks if the user is logged in before accessing certain routes.
  - is_valid_image: This function validates the image format and size before uploading.
- DataBase.db: This is the database file that stores the user and post information. It has three tables:
  - users: This table tracks the user accounts and passwords.
  - posts: This table stores the details of each post, such as the image, caption, date, and likes.
  - post: This table tracks which users have liked which posts.
- templates: This folder contains the HTML files for the website. It has two main layouts:
  - login.html: This is the layout for the login and register pages.
  - layout.html: This is the layout for the home and profile pages.
- static: This folder contains the CSS and JS files for the website. It has two subfolders:
  - css/js: This subfolder has four CSS files and two JS files:
    - loging.css: This file styles the login and register pages.
    - postProf.css: This file styles the home page.
    - profile.css: This file styles the profile page.
    - style.css: This file styles the canvas animation that appears on the login page.
    - app.js: This file creates the canvas animation that appears on the login page.
    - app2.js: This file handles the functionality of the website, such as uploading images, liking posts, and editing profiles.
  - images: This subfolder has three subfolders:
    - icons: This subfolder contains the icon images, such as the heart for the like button.
    - post_images: This subfolder stores the images that users upload as posts.
    - user_image: This subfolder stores the images that users upload as profile pictures.


More information about app.py
# app.py

This file contains the main Python code for the website. It imports the necessary modules and libraries, such as Flask, SQL, and PIL. It also sets up the database connection and the session configuration.

The file has several routes that handle different requests and responses for the website. Each route has a corresponding function that performs some logic and renders a template or redirects to another route. The routes and functions are:

- @app.after_request
  - This function ensures that the responses are not cached by the browser, so that the website always shows the latest information.
- @app.route("/profile", methods=["GET", "POST"])
  - This function displays the profile page of a user. If the user is logged in, it shows their own profile page, where they can edit their about section and upload a profile picture. If the user is not logged in, or if they visit another user's profile page, it shows a different template with less options. The function also queries the database to get the posts of the user whose profile is being viewed.
- @app.route("/")
  - This function displays the home page of the website, where all the posts from all users are shown. The function also queries the database to get the posts and the user information. The user can like or dislike posts from this page.
- @app.route("/like", methods=["POST"])
  - This function handles the request when a user likes a post. It inserts a record into the post table in the database, which tracks which users have liked which posts. It then redirects to the home page.
- @app.route("/dislike", methods=["POST"])
  - This function handles the request when a user dislikes a post. It deletes a record from the post table in the database, which tracks which users have liked which posts. It then redirects to the home page.
- @app.route("/upload", methods=["POST"])
  - This function handles the request when a user uploads a new post. It validates the image format and size, and inserts a record into the posts table in the database, which stores the details of each post. It then saves the image file into a folder with a unique name based on the post id. It then redirects to the profile page.
- @app.route("/delete", methods=["POST"])
  - This function handles the request when a user deletes a post. It checks if the user is authorized to delete the post, and deletes a record from the posts table in the database, which stores the details of each post. It then removes the image file from the folder. It then redirects to the profile page.
- @app.route("/logout")
  - This function logs out the user by clearing their session data. It then redirects to the login page.
- @app.route("/register", methods=["GET", "POST"])
  - This function registers a new user by getting their username and password from a form. It checks if the username is available and if the password matches with the confirmation. It then hashes the password and inserts a record into the users table in the database, which tracks
the user accounts and passwords. It then logs in the user and redirects to their profile page.


# to run this 
flask --app app.py --debug run
