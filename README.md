# Bot-Management
This is a Bot Management where you can stop or run codes and manage them as you need

## Requirements
- Install the requirements by running: `pip install -r requirements.txt`.
- You need a module called [Json Module](https://github.com/AmineGm73/Json-Module). After downloading the zip, extract it into the `Lib` folder of your Virtual Environment or the `Lib` directory where Python is located (on Windows). The structure of the folder must be:
```
json_m/
    __init__.py
    json_m.py
```

## Explanation
- The main folder contains various subfolders, but the essential one is `Bots`.
- Within the `Bots` folder, there are two sample folders that you can delete and replace with your own. Ensure they follow the same structure as the provided ones.
- Each bot folder contains `main.py` and `config.json`.
  - `config.json`: Contains data, with a focus on the `"props"` section, which provides parameters used by `main.py`.
  - `main.py`: Contains a variable `config_props`, initialized by retrieving data from `config.json` using the provided Json Module.
- Additionally, there's a `data` folder containing `bot.log`.

- Here's an example of the structure and content of `main.py`, `config.json`, and the `data/bot.log` file:

    * **main.py:**
    ```python
    from json_m.json_m import json_file, Operation

    config_props = json_file("config.json", Operation.GET, "props")

    # Main Code Start
    while True:
        pass
    ```


    * **config.json**
    ```json
    {
        "name": "DBolt",
        "id": 0,
        "on_start_run": true,
        "props": {
            "command_prefix": "?",
            "bot_token": "uhygtfrdessdf"
        }
    }
    ```
    
    * **data/bot.log**
    ```log
    2024-03-24 10:51:36,480 - __main__ - INFO - Bot started successfuly.
    2024-03-24 10:51:36,480 - __main__ - INFO - Bot started successfuly.
    ```
