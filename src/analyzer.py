from src.data_provider import Provider
import matplotlib.pyplot as plt
import plotly.express as px


class Analyzer:
    def __init__(self):
        self.provider = Provider()

    def plot(self, country, state):
        data = self.provider.get(country, state)
        dates = [i.date for i in data]
        dates.reverse()
        confirmed_cases = [i.confirmed for i in data]
        confirmed_cases.reverse()
        recovered_cases = [i.confirmed for i in data]
        recovered_cases.reverse()
        deaths_cases = [i.confirmed for i in data]
        deaths_cases.reverse()

        fig = px.line(deaths_cases, confirmed_cases)
        fig.show()
