from flask import Flask, render_template,redirect, request
import smtplib
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import datetime

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYpEfBA6O6donzWlSihBXox7C0sKR6'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///posts.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
ckeditor = CKEditor(app)
Bootstrap(app)
db = SQLAlchemy()
db.init_app(app)

class Form(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    name = StringField("Your Name", validators=[DataRequired()])
    url = StringField("Blog Image Url", validators=[DataRequired()])
    content = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit")

class blog_post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(250), nullable=False, unique=True)
    date = db.Column(db.VARCHAR(250),nullable=False)
    body = db.Column(db.TEXT, nullable=False)
    author = db.Column(db.VARCHAR(250), nullable=False)
    img_url = db.Column(db.VARCHAR(250), nullable=False)
    subtitle = db.Column(db.VARCHAR(250), nullable=False)
with app.app_context():
    c = blog_post.query.all()


@app.route("/")
def home():
    c = blog_post.query.all()
    return render_template("index.html",l=c)
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        mes = request.form["message"]
        h = "Successfully sent your message"
        sub = "Someone Contacted You"
        body = f"Hi\nName = {name}\nEmail = {email}\nPhone = {phone}\nMessage = {mes}"
        sender_add = 'champion.coc212@gmail.com'
        sender_pass = 'xdtnxbfuishleozw'
        receiver = ['champion.coc212@gmail.com']
        send_email(sub, body, sender_add, receiver, sender_pass)
        return render_template("contact.html", hed=h)
    else:
        h = "Contact Me"
        return render_template("contact.html", hed=h)
@app.route("/posts/<num>")
def pos(num):
    c = blog_post.query.all()
    return render_template("post.html", l=c,n=num)

@app.route("/new-post", methods = ["GET","POST"])
def new_post():
    form = Form()
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        title = form.title.data
        subtitle = form.subtitle.data
        img = form.url.data
        cont = form.content.data
        x = datetime.datetime.now()
        blog = blog_post(title=title, date=f"{x.strftime('%B')} {x.strftime('%d')},{x.strftime('%Y')}", body=cont,
                         author="Krish", img_url=img, subtitle=subtitle)
        db.session.add(blog)
        db.session.commit()
        return redirect("/")
    return render_template('new_post.html',form=form,c=0)
@app.route("/edit-post/<num>", methods = ["GET","POST"])
def edit(num):
    c = db.session.query(blog_post).filter_by(id=int(num)+1).first()
    form = Form()
    if request.method == "GET":
        form.title.data = c.title
        form.subtitle.data = c.subtitle
        form.url.data = c.img_url
        form.content.data = c.body
        form.name.data = c.author
        return render_template("new_post.html",form=form,c=1)
    if request.method == "POST" and form.validate_on_submit():
        c.title = form.title.data
        c.subtitle = form.subtitle.data
        c.img_url = form.url.data
        c.body = form.content.data
        c.author = form.name.data
        db.session.commit()
        return redirect(f"/posts/{num}")
@app.route("/delete/<num>")
def dele(num):
    c = db.session.query(blog_post).filter_by(id=int(num)).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/")
# @app.route("/login", methods=["GET","POST"])
# def login():
#     if request.method == "POST":
#         name = request.form["name"]
#         email = request.form["email"]
#         phone = request.form["phone"]
#         mes = request.form["message"]
#         return f"<h1>Success<br> name-{name}<br>email-{email}<br>phone-{phone}<br>message-{mes}</h1>"



if __name__ == "__main__":
    app.run(debug=True)