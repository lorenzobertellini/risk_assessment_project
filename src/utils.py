# utils.py

import logging
from typing import Dict, Any
from config import Config

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

def validate_input(input_data: Dict[str, Any]) -> bool:
    """Validate input data against defined ranges"""
    try:
        for field, value in input_data.items():
            if field in Config.INPUT_RANGES:
                min_val, max_val = Config.INPUT_RANGES[field]
                if not min_val <= value <= max_val:
                    logging.error(f"Validation error: {field} value {value} outside range [{min_val}, {max_val}]")
                    return False
        return True
    except Exception as e:
        logging.error(f"Validation error: {str(e)}")
        return False

def get_risk_level(value: float) -> tuple:
    """Get risk level and recommended action based on value"""
    if value < Config.RISK_THRESHOLD_LOW:
        return Config.RISK_LEVELS['low']['text'], Config.RISK_LEVELS['low']['action']
    elif value < Config.RISK_THRESHOLD_HIGH:
        return Config.RISK_LEVELS['medium']['text'], Config.RISK_LEVELS['medium']['action']
    else:
        return Config.RISK_LEVELS['high']['text'], Config.RISK_LEVELS['high']['action']