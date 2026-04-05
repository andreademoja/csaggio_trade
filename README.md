# csaggio_trade — Backtesting Framework Professionale per Strategie Forex

`csaggio_trade` è un framework modulare per il backtesting di strategie di trading su serie storiche Forex.  
È progettato con una chiara separazione delle responsabilità:

- **Data Handler** → fornisce i dati OHLCV
- **Strategy** → genera segnali
- **Execution Engine** → converte segnali in ordini
- **Risk Manager** → calcola la size della posizione
- **Portfolio** → gestisce posizioni, PnL, equity
- **Reporter** → registra eventi, equity curve e trade log
- **Backtester** → orchestra l’intero processo

Il framework è completamente testato tramite `pytest` ed è pensato per essere estendibile, leggibile e robusto.

---

# 🚀 Risultati Recenti

Abbiamo confrontato la strategia **Mean Reversion PRO** su due mercati:

- **EURUSD (H1)** → mercato storicamente poco mean‑reverting  
- **GBPJPY (H1)** → mercato molto più volatile e mean‑reverting  

## 📉 EURUSD — Mean Reversion PRO (leva 1:500, rischio 3%)

| Metrica | Valore |
|--------|--------|
| Profit % | **-8.90%** |
| PnL | -178.05 |
| Win Rate | 56.62% |
| Profit Factor | 0.83 |
| Expectancy | -1.31 |
| Max Drawdown | -12.09% |
| Equity finale | 1821.94 |

**Conclusione:**  
EURUSD H1 non è adatto alla mean reversion pura.  
La strategia entra bene (win rate > 55%) ma non riesce a monetizzare (PF < 1).

---

## 📈 GBPJPY — Mean Reversion PRO (leva 1:500, rischio 20%)

| Metrica | Valore |
|--------|--------|
| Profit % | **+218.50%** |
| PnL | +4369.93 |
| Win Rate | 67.77% |
| Profit Factor | **1.30** |
| Expectancy | 36.12 |
| Max Drawdown | -76.31% |
| Equity finale | 6369.93 |

**Conclusione:**  
GBPJPY è un mercato molto più mean‑reverting.  
La strategia mostra edge reale (PF 1.30, win rate 67%).  
Il drawdown elevato è dovuto al rischio 20% + leva 500.

---

# 📊 Confronto Diretto EURUSD vs GBPJPY

| Caratteristica | EURUSD | GBPJPY |
|----------------|--------|--------|
| Volatilità | Bassa | Alta |
| Mean Reversion | Debole | Forte |
| Profit Factor | 0.83 | **1.30** |
| Win Rate | 56% | **68%** |
| PnL | Negativo | **Molto positivo** |
| Drawdown | Moderato | Estremo (per via del rischio 20%) |

**Sintesi:**  
La Mean Reversion PRO funziona, ma solo su mercati adatti.  
GBPJPY è uno di questi.

---

# 🧪 Come eseguire i test

Assicurati di essere nella root del progetto.

### 1. Attivare il virtual environment

```bash
source venv/bin/activate
```

Su Windows (PowerShell):

```powershell
.\venv\Scripts\activate
```

### 2. Installare le dipendenze
```bash
pip install -r requirements.txt
```

### 3. Eseguire tutti i test
```bash
pytest -q
```

### 4. Eseguire un singolo test
```bash
pytest tests/core/test_backtester.py -q
```

### ▶️ Come eseguire un backtest
Assicurati che il venv sia attivo, poi:

``` bash
python3 run_backtest.py
```

Il sistema genererà:

- equity curve (backtest_results.csv)

- trade log (trade_log.csv)

- metriche di performance in console
