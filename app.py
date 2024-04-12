import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import random, shutil
from zipfile import ZipFile

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)



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


@app.route("/")
def index():
    return redirect('/home')

@app.route("/adduser", methods=['GET', 'POST'])
def adduser():
    print("in adduser")
    username = request.form['name']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    cpassword = generate_password_hash(request.form['cpassword'])
    if check_password_hash(password, cpassword):
        print("pass same")
        return render_template('home.html', error="Passwords do not match")
    return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    # if request.method == 'POST':

@app.route("/authenticate", methods=['POST'])
def authenticate():
    print("in authenticate")
    if request.method == 'POST':
        print("in authenticate post")
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']
        
        conn = sqlite3.connect('users.db')

        return redirect('/home')
    else:
        print("in authenticate get")
        return render_template("login.html")

@app.route("/register", methods=['GET','POST'])
def register():
    print("in register")
    return render_template("register.html")

def clear_submissions_directory():
    submissions_folder = os.path.join(os.getcwd(), 'submissions')
    for filename in os.listdir(submissions_folder):
        file_path = os.path.join(submissions_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

@app.route("/extract", methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file:
            # Check if the file is a ZIP file
            if file.filename.endswith('.zip'):
                # Check if the 'submissions' directory exists, if not, create it
                submissions_folder = os.path.join(os.getcwd(), 'submissions')
                if not os.path.exists(submissions_folder):
                    os.makedirs(submissions_folder, exist_ok=True)

                # Clear the submissions directory first
                clear_submissions_directory()

                # Save the ZIP file to the submissions folder
                zip_path = os.path.join(submissions_folder, file.filename)
                file.save(zip_path)

                # Extract the contents of the ZIP file
                with ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(submissions_folder)

                # Optionally, you can delete the uploaded ZIP file
                os.remove(zip_path)

                # File uploaded and extracted successfully!
                return "File uploaded and extracted successfully!"

            else:
                return "Uploaded file is not a ZIP file."

    return redirect(request.url)



@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/home")
def home():
    return render_template("educator.html")
