from iiif_prezi3 import Collection, config
import os
import json


class CollectionBuilder:
    def __init__(self, path):
        self.path = path
        self.config = config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"
        self.collection = self.__build_collection()

    def __build_collection(self):
        collection = Collection(
            id=f"https://raw.githubusercontent.com/markpbaggett/static_iiif/main/collections/abolition-now.json",
            label="Abolition Now!",
        )
        for path, directories, files in os.walk(self.path):
            for file in files:
                with open(f'{self.path}/{file}', 'r') as new_file:
                    data = new_file.read()
                    json_data = json.loads(data)
                    collection.make_manifest(
                        id=json_data['id'],
                        label=json_data['label']['en'][0],
                    )
        with open('collections/abolition-now.json', 'w') as outfile:
            outfile.write(collection.json(indent=2))


if __name__ == "__main__":
    x = CollectionBuilder('manifests/abolition_now')