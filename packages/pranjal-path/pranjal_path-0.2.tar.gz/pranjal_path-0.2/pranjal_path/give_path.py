import os
import json
    
def environment(dir_path):
    
    with open(os.path.join(dir_path, 'keys.json')) as keys_file:
        json_data=json.load(keys_file)
    
    return json_data