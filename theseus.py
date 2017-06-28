import time
import slackclient
import config
import sys
import os
from fuzzywuzzy import fuzz

## DEFINE CONSTANTS ##

# delay in seconds before checking for new events
LOOP_DELAY = 1

# credentials
BOT_NAME = 'theseus'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
print(BOT_TOKEN)
BOT_ID = 'U60S6CM3Q'

## HELPER FUNCTIONS ##

#function that logs event
def log_event(event, out=sys.stdout):
    out.write('\n-- NEW EVENT LOG -- \n')
    out.write('\nUSER: ' + str(event.get('user')))
    out.write('\nCHANNEL: ' + str(event.get('channel')))
    out.write('\nTYPE: ' + str(event.get('type')))
    out.write('\nTEXT: ' + str(event.get('text')))
    out.write(' ')

# This function differentiates between a (generic) greeting and another message or question
def is_a_greeting(message):
    potential_greetings = ["hello", "hey", "hi", "greetings", "hiya", "good morning", "good evening", "g\'day", "howdy", "welcome", "how are you","yo"]
# sets sent message to lowercase
    message = message.lower()
# Splits the words in the message sent
    message_words_split_list = message.split()
# compares message (that has been split up into words) with potential_greetings list of keywords
    if any(word in message_words_split_list for word in potential_greetings):
        return True
 # returns false if there is no match   
    else:
        return False

# function for opening hour questions sent in messages w/t key phrases array
def opening_hours_questions(message):
    opening_hours_key_phrases = ["when are you open?", "what time are you open until?", "are you closed?", "are you open?", "what time do you open?", "what time do you close?", "what are your opening hours?","what time are you open until?","hours","time","opening","closed"]
 # se  ts sent message all to lowercase
    message = message.lower()

# uses 'fuzzy search' to find a percentage match to the key phrases that would be asked/ compares message to opening hours key phrases
    for phrase in opening_hours_key_phrases:
        print ("message: "+ message)
        print ("phrase: "+ phrase)
        print ("fuzzy match score: " + str(fuzz.partial_ratio(phrase, message)))
        if (fuzz.partial_ratio(phrase, message) > 75):
            print ("found one")
            return True
   # if the 'percentage match' (fuzzy match) is less than 80 then return False     
        
    return False

# function for queries about loans
def min_and_max_loan_query(message):
    loans_key_phrases = ["What is the minimum loan?", "What is the maximum loan?", "What is the maximum loan?", "How much can I loan?", "How much can I borrow?" , "minimum", "maximum", "borrow"]
    message = message.lower()
# checks the fuzz match score
    for phrase in loans_key_phrases:
        print ("message: "+ message)
        print ("phrase: "+ phrase)
        print ("fuzzy match score: " + str(fuzz.partial_ratio(phrase, message)))
        if (fuzz.partial_ratio(phrase, message) > 80):
            print ("found one")
            return True
    
    return False

# funnction for questions about fees
def arrangement_fee_query(message):
    extra_fee_key_phrases = ["Do you charge an arrangement fee?", "Admin fee", "Will I be charged for admin?", "Is there a charge for an arrangement fee?", "Are there any extra charges?","Admin Fee", "Extra","Charge","Fee","Admin"]
    message = message.lower()
# checks the fuzz match score
    for phrase in extra_fee_key_phrases:
        print ("message: "+ message)
        print ("phrase: "+ phrase)
        print ("fuzzy match score: " + str(fuzz.partial_ratio(phrase, message)))  
        if (fuzz.partial_ratio(phrase, message) > 80):
            print ("found one")
            return True

    return False

#function for questions about 'likely loans'
def likely_loans_queries(message):
    likely_loan_phrases = ["who are likely?", "who are likely loans?" "what are likely loans?", "likely loans?"]
    message = message.lower()
    for phrase in likely_loan_phrases:
        print ("message: "+ message)
        print ("phrase: "+ phrase)
        print ("fuzzy match score: " + str(fuzz.partial_ratio(phrase, message)))  
        if (fuzz.partial_ratio(phrase, message) > 75):
            print ("found one")
            return True

    return False

# functions for questions about oakbrook finance
def oakbrook_finance_query(message):
    oakbrook_finance_key_phrases = ["Who is Oakbrook Finance?", "What is Oakbrook Finance?", "Oakbrook Finance", "Oakbrook"]
    message = message.lower()
    for phrase in oakbrook_finance_key_phrases:
        print ("message: "+ message)
        print ("phrase: "+ phrase)
        print ("fuzzy match score: " + str(fuzz.partial_ratio(phrase, message))) 
        if (fuzz.partial_ratio(phrase, message) > 80):
                print ("found one")
                return True

    return False
## MAIN PROGRAM ##

# intialise our slack client
slack_client = slackclient.SlackClient(BOT_TOKEN)

# This functions handles direct messages sent to our slack bot
def handle_message(message, user, channel):
    if is_a_greeting(message):
        post_message(message='Hi, how can I help?', channel=channel)
    elif opening_hours_questions(message):
        post_message(message = "We are open from 8:00 am to 20:00 pm today", channel=channel)
    
    elif min_and_max_loan_query(message): 
        post_message(message = "The minimum loan is 1,000 pounds and the maximum is 5,000 pounds", channel=channel)

    elif arrangement_fee_query(message):
        post_message(message = "No, we do not charge any initial fees", channel=channel)

    elif likely_loans_queries(message):
        post_message(message= "Likely Loans provides you with unsecured personal loans if you are experiencing difficulty in obtaining credit", channel=channel)
    elif oakbrook_finance_query(message):
        post_message(message= "Oakbrook Finance is the parent company for Likely Loans.", channel=channel)
    else: 
        post_message(message='Sorry, I don\'t know what that means!', channel=channel)

# This function uses the slack client to post a message back in the channel passed in as an arg
def post_message(message, channel):
    slack_client.api_call('chat.postMessage', channel=channel,text=message, as_user=True)

# This is the main function, which when ran
# - creates a 1 second infinite loop
# - gets any events registered through the rtm connection
# - for each event post a hello message to the channel of the inbound event
def run():
    # Check real time connection is live
    if slack_client.rtm_connect():
        print'[.] Testbot is ON...'
        while True:
            # gets events
            event_list = slack_client.rtm_read()
            # if there are any then...
            if len(event_list) > 0:
                for event in event_list:
                    user = event.get('user')
                    if user != BOT_ID and event.get('type') == "message": 
                        log_event(event)
                        # call our handler function which posts a message to the channel of the incoming event
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(LOOP_DELAY)
    else:
        print '[!] Connection to Slack failed.'

# Python sets the __name__ var as equal to __main__ when this code runs without being imported, so will be true when executed as file.
if __name__ == '__main__':
    run()

