from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from app import app,db

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(255))
    body = db.Column(db.Text)
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/")
def index():
    return redirect("/blog")

@app.route("/blog")
def blog():
    blogs = Blog.query.all()
    blog_id = request.args.get("id")
    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template("selectedblog.html", blog=blog)
    return render_template("blog.html", blogs=blogs)

@app.route("/newblog", methods=['POST', 'GET'])
def new_post():
    title_error = ""
    body_error = ""
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']    
        if title == "":
            title_error = "All blogs need a title!."
        if body == "":
            body_error = "Please make blog."
        if len(title) > 0 and len(body) > 0:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            post_url = "/blog?id=" + str(new_blog.id)
            return redirect(post_url)
    return render_template("newblog.html", title_error=title_error, body_error=body_error)

if __name__ == '__main__':
    app.run()