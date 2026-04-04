from csaggio_trade.core.execution import ExecutionEngine

def test_execution_engine_transforms_signals_into_orders():
    # Dummy risk manager
    class DummyRisk:
        def size(self, t, signal, portfolio):
            return 123  # valore arbitrario per test

    # Dummy portfolio
    class DummyPortfolio:
        pass

    engine = ExecutionEngine(
        risk_manager=DummyRisk(),
        slippage_model=None,
        commission_model=None
    )

    signals = [
        {"side": "long", "action": "open"},
        {"side": "short", "action": "open"},
        {"action": "close_all"}
    ]

    orders = engine.process_signals(
        t=0,
        signals=signals,
        portfolio=DummyPortfolio()
    )

    assert len(orders) == 3

    # Ordine long
    assert orders[0]["side"] == "long"
    assert orders[0]["action"] == "open"
    assert orders[0]["size"] == 123

    # Ordine short
    assert orders[1]["side"] == "short"
    assert orders[1]["action"] == "open"
    assert orders[1]["size"] == 123

    # Ordine di chiusura
    assert orders[2]["action"] == "close_all"
    assert "size" not in orders[2]  # non serve size per chiudere tutto
