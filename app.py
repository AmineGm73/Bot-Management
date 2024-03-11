import threading
import subprocess
import time
import os
import logging
from flask import Flask, render_template, request, redirect
from json_m.json_m import*
from extensions.socketio import Socket
from datetime import datetime, timedelta
from extensions.utilities import *
from math import *

app = Flask(__name__)

socketio = Socket(app=app)

def run():
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=socketio.start, kwargs={'host': "0.0.0.0", 'debug': True, 'use_reloader': False})
    flask_thread.start()
    
app.jinja_env.globals.update(transform_snake_case_to_title=transform_snake_case_to_title)


def update_bots_json():
    # Get the list of items in the directory
    directory_contents = os.listdir("Bots")

    # Filter out only the directories
    folder_names = [item for item in directory_contents if os.path.isdir(os.path.join("Bots", item))]
    print(folder_names)
    return json_file("Bots\\bots.json", Operation.CHANGE, "bots_names", folder_names)["bots_names"]



# Define your bot's token and prefix

BOTS = update_bots_json()

# Define the bot processes


class BotProcess(threading.Thread):
    def __init__(self, bot_name):
        super().__init__()
        self.bot_name = bot_name
        self._stop_event = threading.Event()
        self._is_alive = False
        self.image_path = f'images/{bot_name}_image.png'
        self.process = None
        self.first_run_time = None
        self.stop_run_time = None
        self.runtime = json_file("Bots\\bots.json", Operation.GET, "bots_runtimes")[self.bot_name]
        # Create a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        # Create a file handler and set its level to DEBUG
        file_handler = logging.FileHandler(f'Bots/{self.bot_name}/data/bot.log')
        file_handler.setLevel(logging.DEBUG)
        # Create a console handler and set its level to INFO
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        # Create a formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def run(self):
        print(f'Starting bot process for {self.bot_name}...')
        self.first_run_time = datetime.now()
        try:
            script_path = f'Bots/{self.bot_name}/main.py'
            while not self._stop_event.is_set():
                try:
                    self.process = subprocess.Popen(['py', script_path])
                    self._is_alive = True
                    self.process.wait()  # Wait for the process to complete
                except subprocess.CalledProcessError as e:
                    print(f'Error in {self.bot_name}: {e.stderr}')
                time.sleep(3600)
        except Exception as e:
            print(f'Error in {self.bot_name}: {str(e)}')
        finally:
            print(f'Bot process for {self.bot_name} terminated.')

    def start(self):
        self._stop_event = threading.Event()
        self._is_alive = True
        super().start()
        self.log("Bot started successfuly.")

    def is_alive(self):
        return self._is_alive

    def stop(self):
        self._stop_event.set()
        self._is_alive = False
        # Terminate the subprocess
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.stop_run_time = datetime.now()
            print(f"{self.bot_name} Process terminated, which was running before {format_seconds_into_time(self.runtime)}")
            self.log(f"Bot Process stopped, which was running before {format_seconds_into_time(self.runtime)}")
            
            
    def save_runtime(self):
        bots_runtimes = json_file("Bots\\bots.json", Operation.GET, "bots_runtimes")
        if self.stop_run_time is None:
            bots_runtimes[self.bot_name] = floor((datetime.now() - self.first_run_time).total_seconds())
            self.runtime = bots_runtimes[self.bot_name]
            json_file("Bots\\bots.json", Operation.CHANGE, "bots_runtimes", bots_runtimes)
            
    def log(self, message):
        # Perform some action
        self.logger.info(message)



def create_bot_processes():
    return [BotProcess(bot_name) for bot_name in BOTS]

@app.route('/')
def index():
    global bot_processes
    return render_template('index.html', bot_processes_list=bot_processes)

@app.route('/start_bot/<bot_name>')
def start_bot(bot_name):
    global bot_processes

    # Check if the bot is not already running
    if [bot for bot in bot_processes if bot.bot_name == bot_name][0].is_alive():
        return f'Bot {bot_name} is already running!'
    
    # Check if the bot_name is valid and has a corresponding token
    if bot_name in BOTS:
        old_process = [bot for bot in bot_processes if bot.bot_name == bot_name][0]
        bot_processes.remove(old_process)
        new_process = BotProcess(bot_name)
        bot_processes.append(new_process)
        new_process.start()

        return redirect("/")
    else:
        return f'Invalid bot name: {bot_name} or missing token!'


@app.route('/stop_bot/<bot_name>')
def stop_bot(bot_name):
    global bot_processes

    # Find the bot process in the list
    process_to_stop = next((process for process in bot_processes if process.bot_name == bot_name), None)

    if process_to_stop is not None:
        try:
            process_to_stop.stop()
            return redirect("/")
        except Exception as e:
            return f'Error stopping bot {bot_name}: {str(e)}'
    else:
        return f'Bot {bot_name} not found or not running!'
    
@app.route('/settings_bot/<bot_name>')
def bot_settings(bot_name):
    global bot_processes
    bot_process = [bot for bot in bot_processes if bot.bot_name == bot_name][0]
    props = json_file(f"Bots/{bot_name}/config.json", Operation.GET, "props")
    return render_template("bot_settings.html", bot=bot_process, props=props)

@app.route('/bot_logs/<bot_name>')
def bot_logs(bot_name):
    global bot_processes
    bot_process = [bot for bot in bot_processes if bot.bot_name == bot_name][0]
    return render_template("bot_log.html", bot=bot_process)

@socketio.socketio.on('saveData')
def handle_message_from_client(data):
    update_bot_data(data)

def update(**kwargs):
    global socketio
    while True:
        bot_processes:BotProcess = kwargs.get("bot_processes")
        runtime_data = {}
        log_data = {}
        for process in bot_processes:
            process.save_runtime()
            runtime_data[process.bot_name] = process.runtime
            with open(f"Bots/{process.bot_name}/data/bot.log", "r") as log_file:
                log_data[process.bot_name] = log_file.read()
        socketio.socketio.emit('runtime_update', runtime_data)
        
        socketio.socketio.emit("log_update", log_data)
        
        time.sleep(1)

if __name__ == '__main__':
    run()

    # Start the bot processes
    bot_processes = create_bot_processes()
    for process in bot_processes:
        run_on_start = json_file(f"Bots/{process.bot_name}/config.json", Operation.GET, "on_start_run")
        if not run_on_start:
            pass
        else:
            process.start()

    try:
        f_update = threading.Thread(target=update, kwargs={"bot_processes": bot_processes})
        f_update.start()
        while any(process.is_alive() for process in bot_processes):
            for process in bot_processes:
                if process.is_alive():
                    process.join(1)
    except KeyboardInterrupt:
        print("Interrupted. Stopping bots...")
        for process in bot_processes:
            process.stop()
        print("All bot processes terminated.")
        f_update.join()
        quit() 

