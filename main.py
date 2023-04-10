from flask import Flask, render_template,redirect
import requests

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
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/posts/contact")
def red_contact():
    return redirect("/contact")
@app.route("/posts/<num>")
def pos(num):
    c = requests.get("https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/fc31e41f8e1a6b713eafb9859f3f7e335939d518/data.json")
    c = c.json()
    return render_template("post.html", l=c,n=num)
if __name__ == "__main__":
    app.run(debug=True)