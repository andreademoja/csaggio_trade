import pandas as pd

class DataLoader:
    def __init__(self, path, parser):
        self.path = path
        self.parser = parser

    def load(self):
        df = pd.read_csv(self.path, parse_dates=[0], index_col=0)
        return self.parser(df)
