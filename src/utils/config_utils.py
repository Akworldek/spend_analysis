import yaml
import os

def read_category_config():
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../configs/category_dictionary.yml")
    with open(path) as yaml_file:
        category_dict = yaml.safe_load(yaml_file)

    return category_dict