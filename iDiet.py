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

    database_workout = root.child('workout').get()

    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template("health.html", namer=database_recipes, name1=database_workout)

    users = root.child("users/" + userId).get()
    return render_template("health.html", namer=database_recipes, name1=database_workout, user=users)

@app.route("/updateToFirebase")
def updateToFirebase():
    DPS = request.args.get("bmis")
    print(DPS)
    try:
        userId = session["logged_in"]
    except KeyError:
        return jsonify(False)
    users = root.child("users/" + userId)
    users.update({"BMIgraph": DPS})

    return jsonify(True)

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
    except KeyError:
        return render_template("community.html")
    users = root.child("users/" + userId).get()
    return render_template("community.html", user=users)

@app.route('/community/announcements', methods=['GET'])
def announcements():
    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template("announcements.html")
    users = root.child("users/" + userId).get()
    return render_template("announcements.html", user=users)

@app.route('/community/general')
def general():
    try:
        userId = session["logged_in"]
        users = root.child("users/" + userId).get()
    except KeyError:
        users = None

    posts = root.child("posts").get()
    if posts == None:
        noPosts = 'There are no current posts.'
        if users != None:
            return render_template('general.html', generals=noPosts, user=users)
        else:
            return render_template('general.html', generals=noPosts)

    titles = []
    for i in posts:
        postDetail = posts[i]
        user_title = postDetail['title']
        titles.append(user_title)
    if users != None:
        return render_template("general.html", title=titles, user=users)
    else:
        return render_template("general.html", title=titles)


@app.route('/community/recipes')
def recipes():
    try:
        userId = session["logged_in"]
        users = root.child("users/" + userId).get()
    except KeyError:
        users = None

    postsR = root.child('user_recipes').get()
    if postsR == None:
        noPostsR = 'There are no current recipes.'
        if users != None:
            return render_template('recipes.html', recipes=noPostsR, user=users)
        else:
            return render_template('recipes.html', recipes=noPostsR)

    names = []
    for i in postsR:
        postRDetail = postsR[i]
        user_name = postRDetail['name']
        names.append(user_name)
    if users != None:
        return render_template('recipes.html', name=names, user=users)
    else:
        return render_template('recipes.html', name=names)


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
    except KeyError:
        return render_template("contactus.html", contact=contact)

    users = root.child("users/" + userId).get()
    return render_template("contactus.html", contact=contact, user=users)

@app.route('/community/faq')
def faq():
    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template("faq.html")
    users = root.child("users/" + userId).get()
    return render_template("faq.html", user=users)

@app.route('/community/general/<title_url>', methods=['GET','POST'])
def append(title_url):
    posts = root.child("posts").get()
    user = root.child('users').get()
    for i in posts:
        user_details = posts[i]
        if user_details['title'] == title_url:
            poster = user[user_details['databaseid']]
            titled = user_details['title']
            texted = user_details['text']
    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template("append.html", poster=poster, titled=titled, texted=texted)
    users = root.child("users/" + userId).get()
    return render_template("append.html", poster=poster, titled=titled, texted=texted, user=users)

@app.route('/community/recipes/<name_url>')
def append2(name_url):
    postsR = root.child('user_recipes').get()
    user = root.child('users').get()
    for i in postsR:
        user_details = postsR[i]
        if user_details['name']== name_url:
            posterR = user[user_details['databaseid']]
            named = user_details['name']
            typed = user_details['type']
            prep_timed = user_details['prep_time']
            cooking_timed = user_details['cooking_time']
            caloried = user_details['calories']
            ingrediented = user_details['ingredients']
            reciped = user_details['recipes']
            i=i
            comments = user_details["comments"]


    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template('append2.html',alluser=user,i=i, comments=comments, userID=userId, posterR=posterR, named=named, typed=typed, prep_timed=prep_timed, cooking_timed=cooking_timed, caloried=caloried, ingrediented=ingrediented, reciped=reciped)
    users = root.child('users/' + userId).get()
    return render_template('append2.html',alluser=user,i=i, comments=comments, userID=userId, posterR=posterR, named=named, typed=typed, prep_timed=prep_timed, cooking_timed=cooking_timed, caloried=caloried, ingrediented=ingrediented, reciped=reciped, user=users)

@app.route('/addComment')
def addComment():
    try:
        userId = session["logged_in"]
    except KeyError:
        return jsonify(False)

    processComment = request.args.get("comment")
    processUserRecipesID = request.args.get("posterRID")
    processUserID = request.args.get("userID")
    post_db = root.child('user_recipes/' + processUserRecipesID + "/comments")
    post_db.push({
        "userID" : processUserID,
        "comment" : processComment
    })

    return jsonify(True)


@app.route('/community/general/post', methods=['POST', 'GET'])
def post():
    post = Post(request.form)
    try:
        userId = session["logged_in"]
        if request.method == 'POST':
            title = post.title.data
            text = post.text.data
            posts = postObj(title, text)
            post_db = root.child('posts')
            post_db.push({
                'databaseid': userId,
                'title': posts.get_title(),
                'text': posts.get_text(),
            })
            return redirect(url_for("general"))

    except KeyError:
        return render_template("post.html", post=post)
    users = root.child("users/" + userId).get()
    return render_template("post.html", post=post, user=users)

@app.route('/community/recipes/post_recipe', methods=['POST', 'GET'])
def post_recipe():
    postR = User_recipe(request.form)
    try:
        userId = session["logged_in"]
        if request.method == 'POST':
            name = postR.name.data
            type = postR.type.data
            prep_time = postR.prep_time.data
            cooking_time = postR.cooking_time.data
            calories = postR.calories.data
            ingredients = postR.ingredients.data
            recipes = postR.recipes.data
            postsR = recipeObj(name, type, prep_time,cooking_time, calories, ingredients, recipes)
            postR_db = root.child('user_recipes')
            postR_db.push({
                'databaseid' : userId,
                "comments" : "",
                'name': postsR.get_name(),
                'type': postsR.get_type(),
                'prep_time': postsR.get_prep_time(),
                'cooking_time': postsR.get_cooking_time(),
                'calories': postsR.get_calories(),
                'ingredients': postsR.get_ingredients(),
                'recipes': postsR.get_recipes(),
            })
            return redirect(url_for("recipes"))
    except KeyError:
        return render_template('post_recipe.html', postR=postR)
    users = root.child('users/' + userId).get()
    return render_template("post_recipe.html", postR=postR, user=users)

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
