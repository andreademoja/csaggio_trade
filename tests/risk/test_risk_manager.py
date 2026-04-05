from csaggio_trade.risk.manager import RiskManager

def test_risk_manager_returns_position_size():
    rm = RiskManager(
        risk_per_trade=0.01,
        account_size=10000,
        atr_multiplier=2
    )

    # Dummy signal
    signal = {"side": "long", "action": "open"}

    # Dummy portfolio
    class DummyPortfolio:
        def get_atr(self):
            return 0.005  # ATR arbitrario per test

    size = rm.size(
        t=0,
        signal=signal,
        portfolio=DummyPortfolio()
    )

    # Calcolo atteso:
    # risk_per_trade * account_size = 100
    # stop_distance = ATR * atr_multiplier = 0.005 * 2 = 0.01
    # size = 100 / 0.01 = 10000 units
    assert size == 10000
