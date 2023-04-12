from flask import Flask, render_template,redirect, request
import smtplib
from email.mime.text import MIMEText
import requests

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

@app.route("/")
def home():
    c = requests.get("https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/fc31e41f8e1a6b713eafb9859f3f7e335939d518/data.json")
    c = c.json()
    return render_template("index.html",l=c)
@app.route("/posts")
def red_home():
    c = requests.get("https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/fc31e41f8e1a6b713eafb9859f3f7e335939d518/data.json")
    c = c.json()
    return redirect("/")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/posts/about")
def red_about():
    return redirect("/about")
@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        mes = request.form["message"]
        h = "Successfully sent your message"
        sub = "Someone Contacted you"
        body = f"Hi\nName = {name}\nemail = {email}\nphone = {phone}\nmessage = {mes}"
        sender_add = 'sender_email'
        sender_pass = 'sender_pass'
        receiver = ['receiver_mail']
        send_email(sub, body, sender_add, receiver, sender_pass)
        return render_template("contact.html", hed=h)
    else:
        h = "Contact Me"
        return render_template("contact.html", hed=h)
@app.route("/posts/contact")
def red_contact():
    return redirect("/contact")
@app.route("/posts/<num>")
def pos(num):
    c = requests.get("https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/fc31e41f8e1a6b713eafb9859f3f7e335939d518/data.json")
    c = c.json()
    return render_template("post.html", l=c,n=num)

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