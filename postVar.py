from wtforms import Form, StringField, SubmitField, SelectField, TextAreaField, validators

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
    food = StringField('Food')
    food_type = SelectField('Type', choices=[('Fish'), ('Chicken'), ('Beef'), ('Pork'), ('Lamb'), ('Vege')], default='')
    recipes = TextAreaField('Recipe')
    submit = SubmitField('Post')