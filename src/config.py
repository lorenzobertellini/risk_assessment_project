# config.py

class Config:
    # Paths
    DATA_PATH = 'data/training_data.csv'
    MODEL_PATH = 'data/model/risk_model.joblib'
    OUTPUT_DOC_PATH = 'valutazione_rischi.docx'
    
    # Model parameters
    N_ESTIMATORS = 100
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    # Risk thresholds
    RISK_THRESHOLD_LOW = 0.3
    RISK_THRESHOLD_HIGH = 0.7
    
    # Risk levels
    RISK_LEVELS = {
        'low': {'text': 'Basso', 'action': 'Nessuna azione immediata richiesta'},
        'medium': {'text': 'Medio', 'action': 'Implementare misure di controllo entro 6 mesi'},
        'high': {'text': 'Alto', 'action': 'Azione immediata richiesta'}
    }
    
    # Settori regolamentati
    REGULATED_SECTORS = ['Energia', 'Industria manifatturiera']
    
    # Input validation
    INPUT_RANGES = {
        'n_dipendenti': (1, 10000),
        'metri_quadri': (1, 100000),
        'numero_sedi': (1, 1000),
        'percentuale_tempo_determinato': (0, 100),
        'rumorosita_db': (40, 100),
        'temperatura_ambiente': (15, 35),
        'numero_macchinari': (0, 1000),
        'quantita_sostanze_chimiche': (0, 10000)
    }