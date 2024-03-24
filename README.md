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

## Get Started
To get started with Bot Management, follow these steps:

1. **Run Flask App**: Navigate to the root directory of your project where `app.py` is located. Run the Flask app by executing the command:
   ```bash
   python app.py
   ```
   This will start the Flask app and make it accessible locally.

2. **Access the App**: Once the Flask app is running, you can access it by opening a web browser and navigating to:
    - `http://localhost:2010`
    - `http://YOUR_LOCAL_WIFI_IP:2010`

3. **Manage Bots**: Upon accessing the app, you'll see a grid displaying the bots from the Bots folder. You can stop or run each bot by clicking the corresponding buttons in the grid.

4. **Configure Bot Settings**:
    - **Settings Icon**: Click the settings icon next to each bot entry to access its settings.
    - **Modify Bot Props**: On the settings page, you can modify the properties of the bot, such as name, command prefix, and bot token, you can remove them and add you own properties by changing the `config.json` file in the Bot directory.
    - **Save Changes**: After making modifications, click the "Save" button to save the changes to the JSON file corresponding to that bot.

## **License**:
This project is licensed under the terms of the MIT license. See [LICENSE](https://github.com/AmineGm73/Bot-Management?tab=MIT-1-ov-file#mit-license) for more information.
---

That's it! You're now ready to manage your bots efficiently using the Bot Management system.

Feel free to adjust the instructions as needed to fit your specific application and audience.


Copyright - 2024 shah1345 (Shah Newaz) From [UiVerse](https://uiverse.io/)
