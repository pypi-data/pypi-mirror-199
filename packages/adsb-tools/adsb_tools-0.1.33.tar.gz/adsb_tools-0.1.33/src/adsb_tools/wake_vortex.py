import csv


class WakeVortexCategories:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._categories = {}
            cls._instance._category_dict = {}
            cls._instance._parse_csv()
        return cls._instance

    @property
    def categories(self):
        return self._categories

    def get_category_dict(self, category):
        return self._category_dict.get(category.lower())

    def _parse_csv(self):
        with open('wake_vortex_categories.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = row['Category']
                tc = row['TC']
                ca = row['CA']
                icao = row['ICAO']
                description = row['Description']
                category_dict = {
                    'TC': tc,
                    'CA': ca,
                    'ICAO': icao,
                    'Description': description
                }
                self._categories[category] = category_dict
                self._category_dict[category.lower()] = category_dict