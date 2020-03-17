import csv
import typing
import requests
from datetime import datetime

EXIT_COMMANDS = ['q', 'quit', 'exit']
ATTRIBUTE_NAMES = ['parent', 'label', 'date', 'lon', 'lat', 'confirmed', 'recovered', 'deaths']


class SourceClient:
    def __init__(self):
        self.url = 'https://interaktiv.morgenpost.de/corona-virus-karte-infektionen-deutschland-weltweit/data/' \
                   'Coronavirus.history.v2.csv'
        self.file_name = 'Coronavirus.history.v2.csv'

    def fetch(self):
        response = requests.get(self.url)
        with open(self.file_name, 'wb') as file:
            file.write(response.content)


class Record:
    def __init__(self,
                 parent,
                 label,
                 date,
                 lon,
                 lat,
                 confirmed,
                 recovered,
                 deaths):
        self.parent = parent
        self.label = label
        self.date = date
        self.lon = lon
        self.lat = lat
        self.confirmed = confirmed
        self.recovered = recovered
        self.deaths = deaths

    @classmethod
    def from_list(cls, lst):
        return cls(
            lst[0], lst[1], datetime.strptime(lst[2], "%Y-%m-%d"), lst[3],
            lst[4], int(lst[5]), int(lst[6]), int(lst[7]),
        )

    def __str__(self):
        return f'{self.label} ({self.parent}): ' \
               f'{self.recovered}/{self.confirmed} ({(self.recovered / self.confirmed * 100.0)}%) recovered ' \
               f'{self.deaths}/{self.confirmed} ({(self.deaths / self.confirmed * 100.0)}%) deaths'


class RecordManager:
    ACTION_MAP = {
        'query': 'query',
        'refresh': 'refresh',
        'not_found': 'not_found',
    }

    def __init__(self, _records: typing.List):
        self.records = _records
        self.client = SourceClient()

    def __get_action(self, name):
        try:
            return getattr(self, self.ACTION_MAP[name], self.__not_found)
        except KeyError:
            return self.__not_found

    def refresh(self):
        self.client.fetch()
        self.records = self.read_file('Coronavirus.history.v2.csv')
        return ['Successfully downloaded new data.']

    def get(self, *args):
        q = args[0]
        q.replace(' ', '')
        q = q.split('=')
        # ensure it's a safe command.
        assert q[0] in ATTRIBUTE_NAMES

        results = []
        for obj in self.records:
            if getattr(obj, q[0]) == q[1]:
                results.append(obj)

        return results

    def __not_found(self):
        print('Command not found!')

    def query(self):
        """
        no whitespaces
        Example::
            GET country=Germany
        :return:
        """
        query = input('> ')
        if query in EXIT_COMMANDS:
            return
        query_list = query.split(' ')

        query_type = query_list[0]
        actual_query = query_list[1]

        return self.get(actual_query)

    def execute(self, _action):
        foo = self.__get_action(_action)
        result = foo()
        for i in result:
            print(i)

    @staticmethod
    def read_file(file_name) -> typing.List:
        records = []
        with open(file_name, newline='') as file:
            spamreader = csv.reader(file, delimiter=',', quotechar='|')
            for index, row in enumerate(spamreader):
                if index != 0:
                    records.append(Record.from_list(row))

        return records


if __name__ == '__main__':
    records = RecordManager.read_file('Coronavirus.history.v2.csv')

    manager = RecordManager(records)

    while True:
        action = input('Action: ')

        if action in EXIT_COMMANDS:
            exit(0)

        manager.execute(action)
