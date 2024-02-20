from iiif_prezi3 import Collection, config
import os
import json
import csv
import click


class CollectionBuilder:
    """Generates a IIIF Collection from a CSV file."""
    def __init__(self, csv_file, label, id, export_file='manifest.json'):
        self.label = label
        self.id = id
        self.csv_file = csv_file
        self.export_file = export_file
        self.config = config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"
        self.collection = self.__build_collection()

    def __build_collection(self):
        collection = Collection(
            id=self.id,
            label=self.label,
        )
        ids = []
        with open(self.csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['url'] in ids:
                    raise(ValueError(f"Duplicate ID: {row['url']}"))
                else:
                    ids.append(row['url'])
                collection.make_manifest(
                    id=row['url'],
                    label=row['label'],
                )
        with open(self.export_file, 'w') as outfile:
            outfile.write(collection.json(indent=2))

@click.command()
@click.option('--csv_file', help='Your CSV file.')
@click.option('--export_file', default="manifest.json", help='Export file name.')
@click.option('--id', help='Where your collection will be hosted.')
@click.option('--label', help='Your label.')
def main(csv_file, export_file, id, label):
    CollectionBuilder(
        id=id,
        csv_file=csv_file,
        export_file=export_file,
        label=label
    )


if __name__ == "__main__":
    main()