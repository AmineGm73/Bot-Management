from json_m.json_m import *


def transform_snake_case_to_title(string: str):
    words = string.split('_')
    title_case_words = [word.capitalize() for word in words]
    return ' '.join(title_case_words)

def format_seconds_into_time(seconds):
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}min {seconds % 60}s"
    elif seconds < 86400:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}min"
    else: return f"{seconds // 86400}day {(seconds % 86400) // 3600}h"

def update_bot_data(newdata):
    bot_name = newdata["bot_name"]
    del newdata["bot_name"]
    print(json_file(f"../Bots/{bot_name}/config.json", Operation.CHANGE, "props", newdata))