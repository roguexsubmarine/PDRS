import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import random, shutil
from zipfile import ZipFile
from plagiarism import calculate_similarity
from scrape_code import get_code
from scrape_subjective import get_data
from codediff import codediff
from scrape_code import get_code
from scrape_subjective import get_data
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user,LoginManager
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from datetime import datetime
#from models import User
#from forms import regform,loginform
from flask_login import login_user , current_user , logout_user ,login_required ,UserMixin,LoginManager
from flask_sqlalchemy import SQLAlchemy
from selenium1 import ai_detection


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
Session(app)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),unique=True, nullable=False)
    email= db.Column(db.String(120),unique=True, nullable=False)
    password=db.Column(db.String(120),nullable=False)

    def repr(self):
        return f"User('{self.name}','{self.email}')"

class regform(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('That username is already been taken.Please try some other username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already been taken.Please try some other email')
        
class loginform(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Login')

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return redirect('/login')

@app.route("/home")
def home():
    return render_template("educator.html")


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


@app.route("/student")
def student():
    return render_template("student.html")



@app.route("/login", methods=['POST','GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=loginform()
    if form.validate_on_submit():
        user=User.query.filter_by(name=form.name.data , email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            return redirect(url_for('home'))
        
        else:
            flash('Incorrect Login Credentials. Please check your Login details', 'danger')
    return render_template('log.html',title='Login',form=form)


@app.route("/register", methods=['POST','GET'])
def signup():
    form =regform()
    if  form.validate_on_submit():
        hashedpassword=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(name=form.name.data,email=form.email.data,password=hashedpassword)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. Go to Login to login to your account!', 'success')
        return redirect(url_for('home'))
    return render_template('reg.html',title='Register',form=form)

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

@app.route("/extract", methods=['POST'])
def extract():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    print("extracting...")

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Check if the file is a ZIP file
        if file.filename.endswith('.zip'):

            print("checked zip")
            assignment_aim = request.form['assignment_aim']
            print("assignment aim : ", assignment_aim)
            prog_lang = request.form['prog_lang']
            # Check if the 'submissions' directory exists, if not, create it
            submissions_folder = os.path.join(os.getcwd(), 'submissions')
            if not os.path.exists(submissions_folder):
                os.makedirs(submissions_folder, exist_ok=True)
            
            clear_submissions_directory()
            print("clear earlier directory")

            # Save the ZIP file to the submissions folder
            zip_path = os.path.join(submissions_folder, file.filename)
            file.save(zip_path)

            # Extract the contents of the ZIP file directly into the submissions folder
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(submissions_folder)

            # Optionally, you can delete the uploaded ZIP file
            os.remove(zip_path)

            # File uploaded and extracted successfully!
            print(zip_path)
            
            # prog_lang = '0'

            
            p = zip_path.replace('.zip', '')
            print(p)
            if (prog_lang == '0'):
                print("Fetching Answers from the web \n\n\n")
                get_data(assignment_aim)
            else :
                print(prog_lang)
                print("Fetching Code from the web \n\n\n")
                get_code(assignment_aim)
            # calling ai
            if assignment_aim:
                ai_detection(assignment_aim, p)


            session['path_to_files'] = p
            data,stmts = calculate_similarity(p)


            sorted_data = sorted(data, key=lambda x: x[2])
            sorted_data = sorted_data[::-1]
            session['sorted_data'] = sorted_data
            session['stmts'] = stmts


            return redirect("/result")
            

        else:
            return "Uploaded file is not a ZIP file."

    return redirect("/home")

@app.route("/result")
def result():
    data = session.get('sorted_data', None)
    

    if data is None:
        return "Data not found. Please sort first."
    # print(data)
    return render_template("report.html", data=data)

@app.route("/list")
def list():
    data = session.get('sorted_data', None)
    # print("\n\n\nqwerty",data[0])
    return render_template("list.html", data=data)

@app.route("/heatmap")
def heatmap():
    return render_template("heatmap.html")

@app.route("/cluster")
def cluster():
    return render_template("cluster.html")


@app.route("/singlecomparison", methods=['POST'])
def single_comparison():
    data = session.get('sorted_data', None)
    student = request.form['student']
    newdata = []
    
    for i in data:
        if i[0] == student:
            newdata.append([student, i[1], i[2]])
        if i[1] == student:
            newdata.append([student, i[0], i[2]])
    
    # print(newdata)
    return render_template("singlecomparison.html", data=newdata)


@app.route("/compare", methods=['POST'])
def compare():
    print("comparing...")

    student1 = request.form['student1']
    student2 = request.form['student2']

    path = session.get('path_to_files', None)

    full_path1 = path + "/" + student1
    full_path2 = path + "/" + student2

    print(full_path1)

    texts = codediff(full_path1, full_path2)
    text1=texts[0]
    text2=texts[1]
    l = min(len(text1), len(text2))

    if len(text1) > len(text2):
        remaining = 1
    else:
        remaining = -1

    

    # print(texts[0])

    return render_template("codecompare.html", text1=text1, text2=text2, student1=student1, student2=student2, l=l, remaining=remaining)




from flask import send_file
import pdfkit
from jinja2 import Environment, FileSystemLoader

@app.route('/download_pdf')
def download_pdf():
    # 1. Retrieve data from the database (replace this with your database query)
    data = session.get('sorted_data', None)

    # 2. Create a Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('./templates/template.html')

    # 3. Render the template with the dynamic data
    html_content = template.render(data=data)

    # 4. Convert HTML content to PDF
    pdf_file_path = './static/output.pdf'  # Provide the desired path to save the PDF
    pdfkit.from_string(html_content, pdf_file_path)

    # 5. Send the PDF file as an attachment
    return send_file(pdf_file_path, as_attachment=True)




from fpdf import FPDF

@app.route('/download_pdf_image')
def download_pdf_image():
    #image_path = os.path.join(app.root_path, 'static', 'clustermap.png')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    images= ['clustermap.png','similarityheatmap.png']
    page_width = 210  # Width of the page in mm
    image_width = 105  # Width of each image in mm
    # right_margin = 10 
    for index, image in enumerate(images):
        image_path = os.path.join(app.root_path, 'static', image)
        x = (page_width - image_width)/2
        y = 10 + index * 100
        pdf.image(image_path, x=x, y=y, w=image_width)

    pdf_file = os.path.join(app.root_path, 'static', 'images.pdf')
    pdf.output(pdf_file)
    return send_file(pdf_file, as_attachment=True)

@app.route("/chatgpt")
def chatgpt():
    # assignment_aim = session.get('assignment_aim', None)
    assignment_aim = "taylor swift"
    filepath = session.get('path_to_files', None)

    ai_detection(assignment_aim, filepath)


