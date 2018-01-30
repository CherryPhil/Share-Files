class postObj():
    def __init__(self, title, comment):
        self.__title = title
        self.__comment = comment

    def get_title(self):
        return self.__title

    def get_comment(self):
        return self.__comment

    def set_title(self, title):
        self.__title = title

    def set_comment(self, comment):
        self.__comment = comment

class contactObj():
    def __init__(self, email, subject, message):
        self.__email = email
        self.__subject = subject
        self.__message = message

    def get_email(self):
        return self.__email

    def get_subject(self):
        return self.__subject

    def get_message(self):
        return self.__message

    def set_email(self, email):
        self.__email = email

    def set_subject(self, subject):
        self.__subject = subject

    def set_message(self, message):
        self.__message = message

class recipeObj():
    def __init__(self, name, type, prep_time, cooking_time, calories, ingredients, recipes):
        self.__name = name
        self.__type = type
        self.__prep_time = prep_time
        self.__cooking_time = cooking_time
        self.__calories = calories
        self.__ingredients = ingredients
        self.__recipes = recipes

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_prep_time(self):
        return self.__prep_time

    def get_cooking_time(self):
        return self.__cooking_time

    def get_calories(self):
        return self.__calories

    def get_ingredients(self):
        return self.__ingredients

    def get_recipes(self):
        return self.__recipes

    def set_name(self, name):
        self.__name = name

    def set_type(self, type):
        self.__type = type

    def set_prep_time(self, prep_time):
        self.__prep_time = prep_time

    def set_cooking_time(self, cooking_time):
        self.__cooking_time = cooking_time

    def set_calories(self, calories):
        self.__calories = calories

    def set_ingredients(self, ingredients):
        self.__ingredients = ingredients

    def set_recipes(self, recipes):
        self.__recipes = recipes