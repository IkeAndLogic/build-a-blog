from flask import Flask, request, redirect, render_template
import cgi
from flask_sqlalchemy import SQLAlchemy
import datetime
import pytz


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://AllBlogs:BeHappy@localhost:8889/AllBlogs'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)




class Build_Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    record = db.Column(db.String(40))



    def __init__(self, title, body, record):
        self.title = title
        self.body =body
        self.record = record



# index/main/homepage where all the 
# blogs will appear. it will be the first page the user sees
#and it will have the link to add blog post page
@app.route("/")
def index():
    all_blogs = Build_Blog.query.all()
    number_of_blogs = len(all_blogs)
    return render_template("allBlogs.html", pageTitle ="Show all Blogs",number_of_blogs =number_of_blogs, all_blogs =all_blogs)


# default add post page
@app.route("/addPost")
def addPost():
    return render_template("addPost.html", pageTitle ="Add Blog Page")


#posts data to data page and displays it on new post page
@app.route("/newPost" , methods = ["POST"])
def newPost():

    if request.form["blogTitle"] and request.form["blogBody"]:
        title = request.form["blogTitle"]
        body = request.form["blogBody"]
         # to create date and time
        centralTime = datetime.datetime.now(tz = pytz.timezone("US/Central"))
        formattedDateTime = centralTime.strftime("%B %d, %Y %H:%M:%S%p")
        
        new_blog = Build_Blog(title, body, formattedDateTime)
        db.session.add(new_blog)

       
        db.session.commit()
        return render_template("newPost.html",pageTitle ="Blog Added Page", blogTitle = title, blogBody = body, record = formattedDateTime)
    
    else:
        title_error = ""
        body_error= ""
        if not request.form["blogTitle"]:
            title_error = "Please provide a title"

        if not request.form["blogBody"]:
            body_error = "Please provide a body"

    return render_template("addPost.html",pageTitle ="Blog Added Page", title_error = title_error, body_error = body_error)
        





if __name__ == "__main__":
    app.run()





    
