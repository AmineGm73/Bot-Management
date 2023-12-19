import json
from enum import Enum

class Operation(Enum):
  ADD = 'add'
  CHANGE = 'change'
  REMOVE = 'remove'
  GET = 'get'


def json_file(file_path, operation, key=None, new_value=None):
  try:
    with open(file_path, 'r') as file:
      json_data = json.load(file)

    if operation == Operation.GET and key is not None:
      if isinstance(json_data, dict):
        return json_data.get(key, None)
      elif isinstance(json_data, list):
        for item in json_data:
          if isinstance(item, dict):
            if key in item:
              return item[key]
        return None

    elif operation == Operation.ADD and key is not None and new_value is not None:
      if isinstance(json_data, dict):
        json_data[key] = new_value
      elif isinstance(json_data, list):
        json_data.append(new_value)

    elif operation == Operation.CHANGE and new_value is not None:
      if isinstance(json_data, dict):
        if key is not None and key in json_data:
          json_data[key] = new_value
        elif key is None:
          for k in json_data:
            json_data[k] = new_value
        else:
          if isinstance(json_data, dict):
            json_data[key] = new_value
          elif isinstance(json_data, list):
            json_data.append(new_value)
      elif isinstance(json_data, list):
        for item in json_data:
          if isinstance(item, dict):
            if key is not None and key in item:
              item[key] = new_value
            elif key is None:
              for k in item:
                item[k] = new_value
            else:
              print(
                  f"Key '{key}' not found in a dictionary. No changes were made."
              )
          else:
            print(
                "Invalid data format inside the list. Expected a dictionary.")
            return None
      else:
        print(
            "Invalid data format. Expected a dictionary or a list of dictionaries."
        )
        return None

    elif operation == Operation.REMOVE and key is not None:
      if isinstance(json_data, dict):
        if key in json_data:
          del json_data[key]
        else:
          print(f"Key '{key}' not found. No changes were made.")
          return json_data
      elif isinstance(json_data, list):
        json_data = [
            item for item in json_data
            if isinstance(item, dict) and key not in item
        ]

    with open(file_path, 'w') as file:
      json.dump(json_data, file, indent=4)

    return json_data

  except Exception as e:
    print(f"An error occurred: {e}")
    return None