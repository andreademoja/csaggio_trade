import pandas as pd
import matplotlib.pyplot as plt

class DrawdownCurve:
    def __init__(self, results):
        self.results = results

    def to_dataframe(self):
        df = pd.DataFrame(self.results)
        equity = df["equity"]
        roll_max = equity.cummax()
        drawdown = equity / roll_max - 1
        return pd.DataFrame({"t": df["t"], "drawdown": drawdown})

    def plot(self, path):
        df = self.to_dataframe()
        plt.figure(figsize=(12, 6))
        plt.plot(df["t"], df["drawdown"], label="Drawdown", color="red")
        plt.title("Drawdown Curve")
        plt.xlabel("Time")
        plt.ylabel("Drawdown")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
