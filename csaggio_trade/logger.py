"""
Logging Configuration for csaggio_trade
=======================================

Configurazione semplice, robusta e ben strutturata per il backtesting framework.
"""

import logging
import sys
from pathlib import Path

# Crea la cartella logs se non esiste
Path("logs").mkdir(exist_ok=True)

def setup_logging(level=logging.INFO):
    """
    Configura il logging per tutto il progetto in modo semplice e affidabile.
    
    Args:
        level: Livello di logging (INFO, DEBUG, WARNING, ERROR)
    """
    # Configurazione principale
    logging.basicConfig(
        level=level,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),                    # Output su console
            logging.FileHandler("logs/csaggio_trade.log", 
                              encoding='utf-8', 
                              mode='a')                           # Output su file
        ],
        force=True  # Forza la riconfigurazione (utile quando si ri-esegue)
    )

    # Riduce il rumore di librerie esterne
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("pandas").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logger = logging.getLogger("csaggio_trade")
    logger.setLevel(level)
    
    logger.info("🚀 Logging configurato correttamente (livello: %s)", 
                logging.getLevelName(level))
    
    return logger


def get_logger(name: str = None):
    """Restituisce un logger per un modulo specifico"""
    if name:
        return logging.getLogger(f"csaggio_trade.{name}")
    return logging.getLogger("csaggio_trade")


# Logger di default per il package
logger = get_logger()

# Per compatibilità con il codice esistente
get_package_logger = get_logger
get_module_logger = get_logger

__all__ = ['setup_logging', 'get_logger', 'logger', 'get_package_logger', 'get_module_logger']