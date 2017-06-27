#This function differentiates between a (generic) greeting and another message or question
def greeting_differentiator (message):
    #array with generic or common greetings created
    potential_greetings = ["hello", "hey", "hi", "greetings", "hiya", "good morning", "good evening", "g'day", "howdy"]

    def split_line():
        message = ("this is random text we want to split")
        splitupmessage = message.split(" ")
        print (splitupmessage)