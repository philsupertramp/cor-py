from datetime import datetime

from src.analyzer import Analyzer

last_refresh = datetime.now()


if __name__ == '__main__':
    analyzer = Analyzer()
    while True:
        country = input('Country: ')
        state = input('State: ')
        if (datetime.now() - last_refresh).seconds > 60:
            analyzer.provider.refresh()
        try:
            analyzer.plot(country, state)
        except AssertionError:
            print('Not found.')
        except TypeError:
            print('Can\'t plot record.')
