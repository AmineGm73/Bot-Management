from flask import Flask, render_template, request, redirect
import threading
import subprocess
import time

app = Flask(__name__)

# Define your bot's token and prefix
BOT_TOKENS = {
    'DBolt': 'YOUR_BOT1_TOKEN',
    'RACUBot': 'YOUR_BOT2_TOKEN'
    # Add more bots as needed
}

# Define the bot processes


class BotProcess(threading.Thread):
    def __init__(self, bot_name):
        super().__init__()
        self.bot_name = bot_name
        self._stop_event = threading.Event()
        self._is_alive = True
        self.image_path = f'images/{bot_name}_image.png'

    def run(self):
        print(f'Starting bot process for {self.bot_name}...')
        try:
            script_path = f'Bots/{self.bot_name}/main.py'
            while not self._stop_event.is_set():
                try:
                    print(subprocess.run(['py', script_path], check=True))
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

    def is_alive(self):
        return self._is_alive

    def stop(self):
        self._stop_event.set()
        self._is_alive = False


def serialize_bot_process(bot_process: BotProcess):
    return {
        'bot_name': bot_process.bot_name,
        'status': 'Running' if bot_process.is_alive() else 'Stopped',
        'image_path': bot_process.image_path  # Assuming the images are in the 'static' folder
    }


def create_bot_processes():
    return [BotProcess('DBolt'), BotProcess('RACUBot')]


bot_processes = create_bot_processes()

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
    if bot_name in BOT_TOKENS:
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


if __name__ == '__main__':
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={'host': "0.0.0.0", 'debug': True, 'use_reloader': False})
    flask_thread.start()

    # Start the bot processes
    bot_processes = create_bot_processes()
    for process in bot_processes:
        process.start()

    try:
        while any(process.is_alive() for process in bot_processes):
            for process in bot_processes:
                if process.is_alive():
                    process.join(1)
    except KeyboardInterrupt:
        print("Interrupted. Stopping bots...")
        for process in bot_processes:
            process.stop()
        print("All bot processes terminated.")
        flask_thread.join()
        quit() 
