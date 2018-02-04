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
from postVar import Announcement

from getPost import postObj
from getPost import contactObj
from getPost import recipeObj
from getPost import announcementsObj

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
    recipes = []
    getRecipe = root.child("recipe").get()

    for i in getRecipe:
        recipeDetail = getRecipe[i]
        recipes.append(recipeDetail["likes"])
        recipes.sort(key=int, reverse=True)
    for iterate in getRecipe:
        numberOfLikes = getRecipe[iterate]["likes"]
        if numberOfLikes == recipes[0]:
            home_recipe.append(getRecipe[iterate])
    for iterate in getRecipe:
        numberOfLikes = getRecipe[iterate]["likes"]
        if numberOfLikes == recipes[1]:
            home_recipe.append(getRecipe[iterate])

    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template("home.html", list=home_recipe)
    users = root.child("users/" + userId).get()
    return render_template("home.html", list=home_recipe, user=users)

@app.route('/home/home_health', methods=['POST', 'GET'])
def home_health():
    articles = root.child("articles/health").get()
    try:
        adminID = session["logged_in_admin"]
    except KeyError:
        try:
            userId = session["logged_in"]
        except KeyError:
            return render_template("home_health.html", articles=articles)
        users = root.child("users/" + userId).get()
        return render_template("home_health.html", user=users, articles=articles)

    adminData = root.child("admins/" + adminID).get()
    return render_template('home_health.html', admin=adminData, articles=articles)

@app.route('/home/home_family', methods=['POST', 'GET'])
def home_family():
    try:
        adminID = session["logged_in_admin"]
    except KeyError:
        try:
            userId = session["logged_in"]
        except KeyError:
            return render_template("home_family.html")
        users = root.child("users/" + userId).get()
        return render_template("home_family.html", user=users)

    adminData = root.child("admins/" + adminID).get()
    return render_template('home_family.html', admin=adminData)


@app.route('/home/home_travel', methods=['POST', 'GET'])
def home_travel():
    try:
        adminID = session["logged_in_admin"]
    except KeyError:
        try:
            userId = session["logged_in"]
        except KeyError:
            return render_template("home_travel.html")
        users = root.child("users/" + userId).get()
        return render_template("home_travel.html", user=users)

    adminData = root.child("admins/" + adminID).get()
    return render_template('home_travel.html', admin=adminData)


@app.route('/home/home_food', methods=['POST', 'GET'])
def home_food():
    try:
        adminID = session["logged_in_admin"]
    except KeyError:
        try:
            userId = session["logged_in"]
        except KeyError:
            return render_template("home_food.html")
        users = root.child("users/" + userId).get()
        return render_template("home_food.html", user=users)

    adminData = root.child("admins/" + adminID).get()
    return render_template('home_food.html', admin=adminData)

@app.route("/articleUpdate")
def articleUpdate():
    header = request.args.get("header")
    content = request.args.get("content")
    direct = request.args.get("direct")
    articles = root.child("articles/" + direct)
    articles.update({
        "content": content,
        "header": header
    })
    return jsonify()


#RECIPE (Ernest)
@app.route('/recipe')
def Recipe():
    database_recipes = root.child('recipe').get()
    name = []
    for i in database_recipes:
        recipe_detail = database_recipes[i]
        name.append(recipe_detail)
    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template("recipe.html", name=name)
    users = root.child("users/" + userId).get()
    return render_template("recipe.html", name=name, user=users)


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

@app.route("/achievement4")
def achievement4():
    processList = request.args.get("list")
    print(processList)

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
    try:
        adminID = session["logged_in_admin"]
    except KeyError:
        try:
            userId = session["logged_in"]
        except KeyError:
            return render_template("community.html")
        users = root.child("users/" + userId).get()
        return render_template("community.html", user=users)
    adminData = root.child("admins/" + adminID).get()
    return render_template("community.html", admin=adminData)

#Credit to Sugianto
@app.route('/community/announcements', methods=['GET'])
def announcements():
    postsA = root.child("announcements").get()

    if postsA == None:
        noNews = 'There are no current announcements.'
    else:
        announcements = []
        for i in postsA:
            postDetail = postsA[i]
            user_announcement = postDetail['announcement']
            announcements.append(user_announcement)
    try:
        adminID = session["logged_in_admin"]
        adminData = root.child("admins/" + adminID).get()
    except KeyError:
        try:
            userId = session["logged_in"]
            users = root.child("users/" + userId).get()
        except KeyError:
            if postsA == None:
                return render_template('announcements.html', noNews=noNews)
            else:
                return render_template('announcements.html', announcement=announcements)
        if postsA == None:
            return render_template("announcements.html", noNews=noNews, user=users)
        else:
            return render_template("announcements.html", announcement=announcements, user=users)
    if postsA == None:
        return render_template("announcements.html",noNews=noNews, admin=adminData)
    else:
        return render_template("announcements.html",announcement=announcements, admin=adminData)

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

@app.route('/community/announcements/<announcement_url>', methods=['GET','POST'])
def append3(announcement_url):
    postsA = root.child("announcements").get()
    admins = root.child('admins').get()
    for i in postsA:
        announcement_detail = postsA[i]
        if announcement_detail['announcement'] == announcement_url:
            posterA = admins[announcement_detail['databaseid']]
            announced = announcement_detail['announcement']
            contented = announcement_detail['content']
            i = i
            comments = announcement_detail["comments"]
            break

    postId = announcement_detail['databaseid']
    user = root.child('users').get()

    try:
        adminID = session["logged_in_admin"]
        admin = root.child("admins/" + adminID).get()
    except KeyError:
        try:
            userId = session["logged_in"]
        except KeyError:
            return render_template("append3.html",alluser=user, i=i, comments=comments, posterA=posterA, announced=announced, contented=contented, postID=postId)
        users = root.child("users/" + userId).get()
        return render_template("append3.html",alluser=user, i=i, comments=comments, userID=userId, posterA=posterA, announced=announced, contented=contented, user=users, postID=postId)

    return render_template("append3.html",alluser=user, i=i, comments=comments, posterA=posterA, announced=announced, contented=contented, postID=postId, admin=admin)


#@app.route('/community')
#def community():
#    try:
#        adminID = session["logged_in_admin"]
#    except KeyError:
#        try:
#            userId = session["logged_in"]
#        except KeyError:
#            return render_template("community.html")
#        users = root.child("users/" + userId).get()
#        return render_template("community.html", user=users)
#    adminData = root.child("admins/" + adminID).get()
#    return render_template("community.html", admin=adminData)

@app.route('/addComment3')
def addComment3():
    try:
        userId = session["logged_in"]
    except KeyError:
        return jsonify(False)
    processComment = request.args.get("comment")
    processUserPostsID = request.args.get("posterAID")
    processUserID = request.args.get("userID")
    post_db = root.child('announcements/' + processUserPostsID + "/comments")
    post_db.push({
        "userID" : processUserID,
        "comment" : processComment,
    })

@app.route("/announcementUpdate")
def announcementUpdate():
    announcement = request.args.get("announcement")
    content = request.args.get("content")
    posterA = request.args.get("posterA")
    articles = root.child("announcements/" + posterA)
    articles.update({
        "announcement": announcement,
        "content": content,
    })
    return jsonify()

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
            i = i
            comments = user_details["comments"]
            break

    postId = user_details['databaseid']
    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template("append.html",alluser=user, i=i, comments=comments, poster=poster, titled=titled, texted=texted, postID=postId)
    users = root.child("users/" + userId).get()
    return render_template("append.html",alluser=user, i=i, comments=comments, userID=userId, poster=poster, titled=titled, texted=texted, user=users, postID=postId)

@app.route('/addComment2')
def addComment2():
    try:
        userId = session["logged_in"]
    except KeyError:
        return jsonify(False)
    processComment = request.args.get("comment")
    processUserPostsID = request.args.get("posterID")
    processUserID = request.args.get("userID")
    post_db = root.child('posts/' + processUserPostsID + "/comments")
    post_db.push({
        "userID" : processUserID,
        "comment" : processComment
    })

    return jsonify(True)

@app.route("/generalUpdate")
def generalUpdate():
    title = request.args.get("title")
    text = request.args.get("text")
    poster = request.args.get("poster")
    articles = root.child("posts/" + poster)
    articles.update({
        "title": title,
        "text": text,
    })
    return jsonify()


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
            break

    postId = user_details['databaseid']
    try:
        userId = session["logged_in"]
    except KeyError:
        return render_template('append2.html',alluser=user,i=i, comments=comments, posterR=posterR, named=named, typed=typed, prep_timed=prep_timed, cooking_timed=cooking_timed, caloried=caloried, ingrediented=ingrediented, reciped=reciped, postID=postId)
    users = root.child('users/' + userId).get()
    return render_template('append2.html',alluser=user,i=i, comments=comments, userID=userId, posterR=posterR, named=named, typed=typed, prep_timed=prep_timed, cooking_timed=cooking_timed, caloried=caloried, ingrediented=ingrediented, reciped=reciped, user=users, postID=postId)

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

@app.route("/recipeUpdate")
def recipeUpdate():
    name = request.args.get("name")
    type = request.args.get("type")
    prep_time = request.args.get("prep_time")
    cooking_time = request.args.get("cooking_time")
    calorie = request.args.get("calorie")
    ingredients = request.args.get("ingredients")
    recipe = request.args.get("recipe")
    posterR = request.args.get("posterR")
    articles = root.child("user_recipes/" + posterR)
    articles.update({
        "name": name,
        "type": type,
        "prep_time": prep_time,
        "cooking_time": cooking_time,
        "calorie": calorie,
        "ingredients": ingredients,
        "recipe": recipe,
    })
    return jsonify()

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
                "comments": "",
                'title': posts.get_title(),
                'text': posts.get_text(),
            })
            return redirect(url_for("general"))

    except KeyError:
        return render_template("post.html", post=post)
    users = root.child("users/" + userId).get()
    return render_template("post.html", post=post, user=users)

@app.route('/community/announcements/post', methods=['POST', 'GET'])
def post_announcements():
    postA = Announcement(request.form)

    admin = session["logged_in_admin"]
    if request.method == 'POST':
        announcement = postA.announcement.data
        content = postA.content.data
        postAs = announcementsObj(announcement, content)
        postA_db = root.child('announcements')
        postA_db.push({
            'databaseid': admin,
            "comments": "",
            'announcement': postAs.get_announcement(),
            'content': postAs.get_content(),
        })
        return redirect(url_for("announcements"))

    return render_template("post_announcements.html", postA=postA, admin=admin)

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

#LOGIN
@app.route("/login", methods=["POST","GET"])
def login():
    session.pop("logged_in", None)
    session.pop("logged_in_admin", None)
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
