import pandas as pd
from src.model import RiskAssessmentModel
from src.config import Config

def main():
    # Caricamento dati
    df = pd.read_csv('data/training_data.csv')
    
    # Training modello
    model = RiskAssessmentModel()
    scores = model.train(df)
    
    # Stampa scores
    print("Model Scores:")
    for risk, score in scores.items():
        print(f"{risk}: {score:.4f}")
    
    # Salvataggio modello
    model.save_model('data/model/risk_model.joblib')

if __name__ == "__main__":
    main()