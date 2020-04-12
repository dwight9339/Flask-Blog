from flask import Flask, render_template
app = Flask(__name__)

posts = [
    {
        "author": "Heidi Helmsworth",
        "title": "Blog Post 1",
        "content": "My first post......",
        "date_posted": "April 12, 2018"
    }
]

@app.route("/")
def hello():
    return render_template("home.html", posts=posts, title="Home")

@app.route("/about")
def about():
    return render_template("about.html", title="About Me")

if __name__ == "__main__":
    app.run(debug=True)