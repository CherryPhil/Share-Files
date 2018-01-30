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
    def __init__(self, food, food_type, recipes):
        self.__food = food
        self.__food_type = food_type
        self.__recipes = recipes

    def get_food(self):
        return self.__food

    def get_food_type(self):
        return self.__food_type

    def get_recipes(self):
        return self.__recipes

    def set_food(self, food):
        self.__food = food

    def set_food_type(self, food_type):
        self.__food_type = food_type

    def set_recipes(self, recipes):
        self.__recipes = recipes