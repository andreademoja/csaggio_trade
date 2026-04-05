import matplotlib.pyplot as plt

class EquityCurve:
    def __init__(self, results):
        self.results = results

    def to_dataframe(self):
        df = pd.DataFrame(self.results)
        return df[["t", "equity"]]

    def plot(self, path):
        df = self.to_dataframe()
        plt.figure(figsize=(12, 6))
        plt.plot(df["t"], df["equity"], label="Equity")
        plt.title("Equity Curve")
        plt.xlabel("Time")
        plt.ylabel("Equity")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
