from json_m.json_m import json_file, Operation

props = json_file("config.json", Operation.GET, "props")

while True:
    #print(f"Running with '{props['command_prefix']}' as command prefix")
    pass