from flask import Flask, render_template, request, redirect, url_for, jsonify, session
#Firebase
import firebase_admin
from firebase_admin import credentials, db

from formLogin import LoginForm
from formRegister import RegisterForm
from formProfile import ProfileForm

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
    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template("fun.html", cha1=-2, cha2=-2, cha3=-2)
    users = root.child("users/"+userId).get()
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
    return render_template("fun.html", cha1=cha1, cha2=cha2, cha3=cha3, user=users)

@app.route("/userScoreProcess")
def userScoreProcess():
    processScore = request.args.get("userScore")
    questionNum = request.args.get("Qnum")
    try:
        userId = session["logged_in"]
    except KeyError:
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
    return render_template("community.html")

@app.route('/community/announcements', methods=['GET'])
def announcements():
    return render_template("announcements.html")

@app.route('/community/general')
def general():
    posts = root.child("posts").get()
    if posts == None:
        noPosts = 'There are no current posts.'
        return render_template('general.html', generals=noPosts)
    titles = []
    comments = []
    for i in posts:
        postDetail = posts[i]
        user_title = postDetail['title']
        user_comment = postDetail['comment']
        titles.append(user_title)
        comments.append(user_comment)
    return render_template("general.html", title=titles, comment=comments)

@app.route('/community/recipes')
def recipes():
    return render_template("recipes.html")

@app.route('/community/contactus', methods=['POST', 'GET'])
def contactus():
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

    return render_template("contactus.html", contact=contact)

@app.route('/community/faq')
def faq():
    return render_template("faq.html")

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
        return redirect(url_for('general'))

    return render_template("post.html", post=post)

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
    admins = root.child("admins").get()

    if request.method == "POST" and form.adminlogin.data:
        username = form.adminusername.data
        password = form.adminpassword.data

        for admin in admins:
            adminDetail = admins[admin]
            if adminDetail["username"] == username and adminDetail["password"] == password:
                session["logged_in_admin"] = admin
                return redirect(url_for("home"))
        error = "Please check your Username and Admin Password given."
        return render_template("login.html", form=form, regform=regform, checkuser=users, error=error)

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
            "password": user.get_password(),
            "displaypicture": "/static/images/display_pic.png",
            "displaypicturecolor": "#FF8C00"
        })
        return render_template("login.html", form=form, regform=regform, checkuser=users)

    return render_template("login.html", form=form, regform=regform, checkuser=users)

#PROFILE
@app.route("/profile", methods=["POST","GET"])
def profile():
    try:
        proform = ProfileForm(request.form)
        userId = session["logged_in"]
        users = root.child("users/" + userId).get()

        proform.firstname.data = users["firstname"]
        proform.lastname.data = users["lastname"]
        proform.username.data = users["username"]

        if request.method == "POST" and proform.closeacc.data:
            root.child("users/" + userId).delete()
            return redirect(url_for('login'))

        if request.method == "POST" and proform.changepassword.data:
            user_db = root.child("users/" + userId)
            user_db.update({"password": proform.newpassword.data})
            return redirect(url_for('profile'))

        return render_template("profile.html", proform=proform, user=users)
    except KeyError:
        return redirect(url_for("home"))

@app.route("/updatingData")
def update_data():
    processProfileValue = request.args.get("value")
    processProfileKey = request.args.get("key")

    userId = session["logged_in"]
    user_db = root.child("users/" + userId)
    user_db.update({processProfileKey: processProfileValue})
    users = root.child("users/" + userId).get()
    return jsonify(users)

@app.route("/checkForSameUsername")
def check_sameUsername():
    checkingUsername = request.args.get("checkThis")

    users = root.child("users").get()
    for i in users:
        if users[i]["username"] == checkingUsername:
            return jsonify(False)
    return jsonify(True)

@app.route("/updateDP")
def update_dp():
    processFilePath = request.args.get("filePath")
    processColor = request.args.get("color")

    userId = session["logged_in"]
    user_db = root.child("users/" + userId)
    user_db.update({"displaypicture": processFilePath,
                    "displaypicturecolor": processColor
                    })
    return jsonify()

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
