from flask import Flask, render_template, request, redirect, url_for, jsonify, session
#Firebase
import firebase_admin
from firebase_admin import credentials, db

from formLogin import LoginForm
from formRegister import RegisterForm

from postVar import Post
from postVar import Contact
from postVar import User_recipe

from getPost import postObj
from getPost import contactObj
from getPost import recipeObj

from objRegister import RegisterObject


cred = credentials.Certificate('cred/idiet-229a2-firebase-adminsdk-f5ibn-9f138ec335.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://idiet-229a2.firebaseio.com/'
})

root = db.reference()


app = Flask(__name__)

#HOME
@app.route("/")
def home():
    home_recipe = []
    getRecipe = root.child("recipe").get()
    count = 0
    for i in getRecipe:
        recipeDetail = getRecipe[i]
        home_recipe.append(recipeDetail)
        count += 1
        if count == 2:
            break
    return render_template("home.html", list=home_recipe)

@app.route('/home_health')
def home_health():
    return render_template('home_health.html')

#RECIPE
@app.route('/recipe')
def Recipe():
    database_recipes = root.child('recipe').get()
    name = []
    for i in database_recipes:
        recipe_detail = database_recipes[i]
        name.append(recipe_detail)
    return render_template('recipe.html', name=name)

#HEALTH
@app.route("/health")
def health():
    database_recipes = root.child('recipe').get()
    name = []
    for i in database_recipes:
        recipe_detail = database_recipes[i]
        name.append(recipe_detail)

    database_workout = root.child('workout').get()
    name1 = []
    for i in database_workout:
        workout_detail = database_workout[i]
        name1.append(workout_detail)

    return render_template("health.html", name=name, name1=name1)

#FUN
@app.route("/fun")
def fun():
    #ADD FOR EVERYONE
    try:
        userId = session["logged_in"]
    except:
    #ADD FOR EVERYONE
        return render_template("fun.html", cha1=-2, cha2=-2, cha3=-2)
    users = root.child("users/"+userId).get()
    username = users["username"]
    if "challenge1" in users:
        cha1 = users["challenge1"]
    else:
        cha1 = -1

    if "challenge2" in users:
        cha2 = users["challenge2"]
    else:
        cha2 = -1

    if "challenge3" in users:
        cha3 = users["challenge3"]
    else:
        cha3 = -1
    return render_template("fun.html", cha1=cha1, cha2=cha2, cha3=cha3, username=username)

@app.route("/userScoreProcess")
def userScoreProcess():
    processScore = request.args.get("userScore")
    questionNum = request.args.get("Qnum")
    try:
        userId = session["logged_in"]
    except:
        return jsonify(-2)
    user_db = root.child("users/"+userId)

    userInfo = user_db.get()
    if not("challenge"+questionNum in userInfo):
        user_db.update({"challenge" + questionNum: processScore})
    elif userInfo["challenge"+questionNum] > processScore:
        return jsonify(userInfo["challenge"+questionNum])
    user_db.update({"challenge"+questionNum : processScore})
    return jsonify(processScore)

#COMMUNITY
@app.route('/community')
def community():
    try:
        userId = session["logged_in"]
    except:
        return render_template("community.html")
    users = root.child("users/" + userId).get()
    return render_template("community.html", user=users)

@app.route('/community/announcements', methods=['GET'])
def announcements():
    try:
        userId = session["logged_in"]
    except:
        return render_template("announcements.html")
    users = root.child("users/" + userId).get()
    return render_template("announcements.html", user=users)

@app.route('/community/general')
def general():
    try:
        userId = session["logged_in"]
        users = root.child("users/" + userId).get()
    except:
        users = None

    posts = root.child("posts").get()
    if posts == None:
        noPosts = 'There are no current posts.'
        if users != None:
            return render_template('general.html', generals=noPosts, user=users)
        else:
            return render_template('general.html', generals=noPosts)

    titles = []
    comments = []
    for i in posts:
        postDetail = posts[i]
        user_title = postDetail['title']
        user_comment = postDetail['comment']
        titles.append(user_title)
        comments.append(user_comment)
    if users != None:
        return render_template("general.html", title=titles, comment=comments, user=users)
    else:
        return render_template("general.html", title=titles, comment=comments)


@app.route('/community/recipes')
def recipes():
    try:
        userId = session["logged_in"]
    except:
        return render_template("recipes.html")
    users = root.child("users/" + userId).get()
    return render_template("recipes.html", user=users)

@app.route('/community/contactus', methods=['POST', 'GET'])
def contactus():
#code
    contact = Contact(request.form)
    if request.method == 'POST':
        email = contact.email.data
        subject = contact.subject.data
        message = contact.message.data
        contacts = contactObj(email, subject, message)
        contact_db = root.child('messages')
        contact_db.push({
            'email': contacts.get_email(),
            'subject': contacts.get_subject(),
            'message': contacts.get_message(),
        })
        return redirect(url_for('contactus'))
#code
    try:
        userId = session["logged_in"]
    except:
        return render_template("contactus.html", contact=contact)

    users = root.child("users/" + userId).get()
    return render_template("contactus.html", contact=contact, user=users)

@app.route('/community/faq')
def faq():
    try:
        userId = session["logged_in"]
    except:
        return render_template("faq.html")
    users = root.child("users/" + userId).get()
    return render_template("faq.html", user=users)

@app.route('/community/announcements/<title_url>', methods=['GET','POST'])
def append(title_url):
    posts = root.child("posts").get()
    for i in posts:
        user_details = posts[i]
        if user_details['title'] == title_url:
            titled = user_details['title']
            commented = user_details['comment']
    return render_template("append.html", titled=titled, commented=commented)

@app.route('/community/general/post', methods=['POST', 'GET'])
def post():
    #code
    post = Post(request.form)
    if request.method == 'POST':
        title = post.title.data
        comment = post.comment.data
        posts = postObj(title, comment)
        post_db = root.child('posts')
        post_db.push({
            'title': posts.get_title(),
            'comment': posts.get_comment(),
        })
    #code
    try:
        userId = session["logged_in"]
    except:
        return render_template("post.html", post=post)
    users = root.child("users/" + userId).get()
    return render_template("post.html", post=post, user=users)

@app.route('/community/recipes/post_recipe', methods=['POST', 'GET'])
def post_recipe():
    postR = User_recipe(request.form)
    if request.method == 'POST':
        food = postR.food.data
        food_type = postR.food_type.data
        recipes = postR.recipes.data
        postRs = recipeObj(food, food_type, recipes)
        postR_db = root.child('recipes')
        postR_db.push({
            'food': postRs.get_food(),
            'food_type': postRs.get_food_type,
            'recipes': postRs.get_recipes,
        })
        return redirect(url_for('recipes'))

    return render_template("post_recipe.html", postR=postR)

#LOGIN
@app.route("/login", methods=["POST","GET"])
def login():
    session.pop("logged_in", None)
    form = LoginForm(request.form)
    regform = RegisterForm(request.form)

    users = root.child("users").get()

    if request.method == "POST" and form.login.data:
        username = form.username.data
        password = form.password.data

        for userid in users:
            userDetail = users[userid]
            if userDetail["username"] == username and userDetail["password"] == password:
                session["logged_in"] = userid
                return redirect(url_for('home'))
        error="Please check your Username and Password."
        return render_template("login.html", form=form, regform=regform, checkuser=users, error=error)

    elif request.method == "POST" and regform.register.data:
        username = regform.username.data
        firstname = regform.firstname.data
        lastname = regform.lastname.data
        password = regform.password.data

        user = RegisterObject(username, firstname, lastname, password)
        user_db = root.child("users")
        user_db.push({
            "username": user.get_username(),
            "firstname": user.get_firstname(),
            "lastname": user.get_lastname(),
            "password": user.get_password()
        })
        return render_template("login.html", form=form, regform=regform, checkuser=users)

    return render_template("login.html", form=form, regform=regform, checkuser=users)

#PROFILE

@app.route("/profile")
def profile():
    return render_template("profile.html")

#OTHERS
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms&conditions")
def terms_and_conditions():
    return render_template("terms&conditions.html")

if __name__ == "__main__":
    app.secret_key = 'iDiet123'
    app.run(debug=True)
