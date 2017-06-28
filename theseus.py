import time
import slackclient
import sys
from fuzzywuzzy import fuzz

## DEFINE CONSTANTS ##

# delay in seconds before checking for new events
LOOP_DELAY = 1

# credentials
BOT_NAME = 'theseus'
BOT_TOKEN = 'TOKEN'
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
        if (fuzz.partial_ratio(phrase, message) > 80):
            print ("found one")
            return True
   # if the 'percentage match' (fuzzy match) is less than 80 then return False     
        
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

