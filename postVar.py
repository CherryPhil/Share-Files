from wtforms import Form, StringField, SubmitField, SelectField, TextAreaField, RadioField, IntegerField, validators

class Post(Form):
    title = StringField('Title', [validators.Length(min=1, max=50)])
    comment = TextAreaField('Text')
    submit = SubmitField('Post')

class Contact(Form):
    email = StringField('Email Address:')
    subject = StringField('Subject:')
    message = TextAreaField('Your message:')
    submit = SubmitField('Submit')

class User_recipe(Form):
    name = StringField('Food Name', [validators.Length(min=4, max=20)])
    type = RadioField('Type', choices=[('H', 'Healthy'), ('U', 'Unhealthy')], default='H')
    prep_time = IntegerField('Preparation Time (in minutes)')
    cooking_time = IntegerField('Cooking Time (in minutes)')
    calories = IntegerField('Calories')
    ingredients = StringField('Ingredients')
    recipes = TextAreaField('Recipes')
    submit = SubmitField('Post')