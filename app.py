"""app.py

   for POSTMAN collection is unable to read large file, this can be used to chunk everything.
"""

import json
import os
import subprocess

SRC_FILE = "sample.postman_collection.json"
OUTPUT_FOLDER = "output"


def check_output_folder():
    """check_output_folder

    this checks if the folder exists, if not it creates a new folder. If already present, cleans it.
    """
    if not os.path.exists(OUTPUT_FOLDER):
        print("Creating output directory..")
        os.makedirs(OUTPUT_FOLDER)
    else:
        print("Cleaning output directory..")
        subprocess.run(["rm -rf " + OUTPUT_FOLDER], shell=True)
        os.makedirs(OUTPUT_FOLDER)


def read_json_file_contents(file_location):
    """read_json_file_contents

    read the contents of a file, and parse as JSON"""
    file_contents = "{}"
    with open(file_location) as user_file:
        file_contents = user_file.read()
    return json.loads(file_contents)


def write_json_to_file(file_location, file_content):
    """write_json_to_file

    writes to an output file as JSON"""
    with open(file_location, "w") as outfile:
        json.dump(file_content, outfile)
        outfile.write("\n")


def investigate_postman_level1_collections(file_contents):
    """investigate_postman_level1_collections

    this investigates the details of all first level keys"""
    # level-1
    # print(file_contents.keys()) # dict_keys(['info', 'item', 'variable'])
    print(file_contents.get("info"))
    print(
        file_contents.get("info").keys()
    )  # dict_keys(['_postman_id', 'name', 'schema', '_exporter_id', '_collection_link'])
    print(file_contents.get("info").get("name"))
    print(file_contents.get("info").get("schema"))
    # print(file_contents.get("variable")) # variable, is an array of {'key': 'current-dt', 'value': ''} pairs


def investigate_postman_level2_collections(file_contents):
    """investigate_postman_level1_collections

    this investigates the details of everything under 'item' key"""
    # level-2, check details about 'item'
    item = file_contents.get("item")
    # print(len(item))

    # find unique keys across all items
    # all_keys # ['name', 'item', 'event', 'description']
    for i in item:
        print(i.get("name"))  # are folder names


def chunk_postman_collection_by_folder(file_contents):
    """chunk_postman_collection_by_folder

    make smaller files from the bigger POSTMAN collection"""
    info_obj = file_contents.get("info", None)
    variable_obj = file_contents.get("variable", None)
    file_name = "v2_chunked_"
    items = file_contents.get("item")
    for i in items:
        itm = {}
        indx = items.index(i)
        info_obj["name"] = file_name + str(indx)
        itm["info"] = info_obj
        itm["variables"] = variable_obj
        itm["item"] = [i]
        file_location = OUTPUT_FOLDER + "/" + info_obj.get("name") + ".json"
        write_json_to_file(file_location, itm)


check_output_folder()
file_contents = read_json_file_contents("./" + SRC_FILE)
# investigate_postman_level1_collections(file_contents)
# investigate_postman_level2_collections(file_contents)
chunk_postman_collection_by_folder(file_contents)
