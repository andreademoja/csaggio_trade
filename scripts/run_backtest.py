from csaggio_trade.core.engine import Engine
from csaggio_trade.data.loader import DataLoader
from csaggio_trade.strategies.mean_reversion import MeanReversionStrategy
from csaggio_trade.config.presets import FOREX_MEAN_REVERSION

def identity_parser(df):
    return df

loader = DataLoader("data/AUDUSD.csv", identity_parser)
strategy = MeanReversionStrategy(**FOREX_MEAN_REVERSION)

engine = Engine(
    loader=loader,
    strategy=strategy,
    execution=None,   # li aggiungeremo dopo
    portfolio=None,
    reporter=None
)

engine.run()
