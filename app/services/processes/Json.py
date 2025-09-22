from os import listdir, makedirs, getcwd
from os.path import exists, join
from json import load, dump

class Json:
    def __init__(self, data):
        self.data = data

    def createJson(self):
        # Get the absolute path to the current directory
        current_directory = getcwd()

        # Define the directory path where you want to save the JSON file
        directory_path = join(current_directory, "Json")

        # Create the directory if it doesn't exist
        if not exists(directory_path):
            makedirs(directory_path)

        file_path = join(directory_path, f"{self.data['username']}.json")

        # If the file already exists, read its content first
        existing_data = []
        if exists(file_path):
            with open(file_path, 'r') as json_file:
                existing_data = load(json_file)

        # Append the new tweet data to the existing data,
        existing_data.append(self.data)

        # Write the combined data to the JSON file
        with open(file_path, 'w', encoding = 'utf-8') as json_file:
            dump(existing_data, json_file, indent=4)
        
        return file_path
    
    def unicode_arabic(self, txt: str):
        try:
            unicode_text = eval(txt)
            return unicode_text
        
        except SyntaxError as e:
            print("Error:", e)

    def edit_json(self):
        directory_path = join(getcwd())
        file_path = join(directory_path, ".json")

        # Read the JSON data from the file
        with open(file_path) as json_file:
            data = load(json_file)

        for entry in data:
            entry["tweet"] = self.unicode_arabic(entry["tweet"])

        with open(file_path, 'w', encoding='utf-8') as json_file:
            dump(data, json_file, indent=4, ensure_ascii=True)

# JSON combine utility remains the same
def combine_json_files():
    directory_path = join(getcwd(), "Json")
    if not exists(directory_path):
        makedirs(directory_path)

    combined_data = []
    for filename in listdir(directory_path):
        if filename.endswith(".json"):
            with open(join(directory_path, filename), encoding="utf-8") as f:
                combined_data.extend(load(f))

    combined_file_path = join(directory_path, "json_data.json")
    with open(combined_file_path, "w") as f:
        dump(combined_data, f, indent = 4)

    return combined_file_path