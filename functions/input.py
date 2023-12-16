import json
import os


def inputHandler(event, context):
    try:
        current_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(current_dir, './genres.json')

        with open(json_file_path, 'r') as file:
            genres = json.load(file)
            return list(genres.values())

    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
