import typing
from datetime import datetime

from src.data_sources import RecordManager, Record


class Provider:
    def __init__(self):
        self.manager = RecordManager()
        self.data = {}
        self.build()

    def build(self):
        self.data = {}
        for obj in self.manager.records:
            if obj.parent in self.data:
                if obj.label in self.data[obj.parent]:
                    self.data[obj.parent][obj.label].append(obj)
                else:
                    self.data[obj.parent][obj.label] = [obj]
            else:
                self.data[obj.parent] = {obj.label: [obj]}
        self.sort()
        self.append_countries()

    def append_countries(self):
        for country in self.data.keys():
            confirmed = sum([self.data[country][key][0].confirmed for key in self.data[country].keys()])
            recovered = sum([self.data[country][key][0].recovered for key in self.data[country].keys()])
            deaths = sum([self.data[country][key][0].deaths for key in self.data[country].keys()])
            self.data[country]['Country'] = Record(
                country, 'Country', datetime.now().date(), 0, 0, confirmed, recovered, deaths
            )

    def refresh(self):
        self.manager.refresh()
        self.build()

    def sort(self):
        for parent_key in self.data.keys():
            for child_key in self.data[parent_key].keys():
                self.data[parent_key][child_key].reverse()

    def validate_country(self, country):
        assert country in self.data

    def validate_city(self, country, city):
        self.validate_country(country)
        assert city in self.data[country]

    def get_latest(self, country, city=None):
        self.validate_country(country)
        if not city:
            message = f'{country}: ' \
                      f'{self.data[country]["Country"].deaths}/{self.data[country]["Country"].confirmed} deaths, ' \
                      f'{self.data[country]["Country"].recovered}/{self.data[country]["Country"].confirmed} recovered.'
        else:
            self.validate_city(country, city)
            confirmed = self.data[country][city][0].confirmed
            recovered = self.data[country][city][0].recovered
            deaths = self.data[country][city][0].deaths
            message = f'{city}({country}): {deaths}/{confirmed} deaths, {recovered}/{confirmed} recovered.'

        print(message)

    def get(self, country, city=None) -> typing.List:
        self.validate_country(country)
        if not city:
            data = self.data[country]['Country']
        else:
            self.validate_city(country, city)
            data = self.data[country][city]
        return data
