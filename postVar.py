
from wtforms import Form, StringField, SubmitField, SelectField, TextAreaField, IntegerField, validators

class Post(Form):
    title = StringField('Title',[validators.DataRequired()])
    text = TextAreaField('Text', [validators.DataRequired()])
    submit = SubmitField('', [validators.DataRequired()])

class Announcement(Form):
    announcement = StringField('Announcement', [validators.DataRequired()])
    content = TextAreaField('Content', [validators.DataRequired()])
    submit = SubmitField('', [validators.DataRequired()])

class Contact(Form):
    email = StringField('Email Address:', [validators.DataRequired()])
    subject = StringField('Subject:', [validators.DataRequired()])
    message = TextAreaField('Your message:', [validators.DataRequired()])
    submit = SubmitField('', [validators.DataRequired()])

class User_recipe(Form):
    name = StringField('Food Name', [validators.DataRequired()])
    type = SelectField('Type', [validators.DataRequired()], choices=[('Healthy', 'Healthy'), ('Unhealthy', 'Unhealthy')])
    prep_time = IntegerField('Preparation Time (in minutes)', [validators.DataRequired()])
    cooking_time = IntegerField('Cooking Time (in minutes)', [validators.DataRequired()])
    calories = IntegerField('Calories', [validators.DataRequired()])
    ingredients = StringField('Ingredients', [validators.DataRequired()])
    recipes = TextAreaField('Recipes', [validators.DataRequired()])
    submit = SubmitField('', [validators.DataRequired()])