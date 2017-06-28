from flask import Flask
import theseus
import threading

## HTTP SERVER ##
app = Flask(__name__)

@app.route('/')
def main_route():
    return 'OK'

def start_bot():
    theseus.run()

# Python sets the __name__ var as equal to __main__ when this code runs without being imported, so will be true when executed as file.
if __name__ == '__main__':
    # Start the http server as a process in a child thread
    bot_task = threading.Thread(target=start_bot)
    bot_task.start()
    # Start our slack communication event poller
    app.run()