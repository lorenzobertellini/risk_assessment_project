import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
from typing import List, Dict, Tuple

class RiskAssessmentModel:
    def __init__(self):
        self.feature_columns = ['settore_attivita', 'n_dipendenti', 'metri_quadri', 
                              'numero_sedi', 'percentuale_tempo_determinato', 
                              'certificazione_iso_45001', 'settore_regolamentato',
                              'presenza_macchinari_pesanti', 'lavoro_in_quota',
                              'presenza_sostanze_chimiche', 'rumorosita_db',
                              'presenza_videoterminali', 'temperatura_ambiente',
                              'presenza_sistemi_elettrici', 'numero_macchinari',
                              'quantita_sostanze_chimiche']
        
        self.target_columns = ['rischio_meccanico', 'rischio_caduta', 'rischio_chimico',
                             'rischio_rumore', 'rischio_elettrico', 'rischio_informatica']
        
        self.label_encoder = LabelEncoder()
        self.models = {}

    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        X = df[self.feature_columns].copy()
        y = df[self.target_columns].copy()
        
        # Encoding delle categorie
        X['settore_attivita'] = self.label_encoder.fit_transform(X['settore_attivita'])
        
        return X, y

    def train(self, df: pd.DataFrame) -> Dict:
        X, y = self.preprocess_data(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        scores = {}
        for risk in self.target_columns:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train[risk])
            score = model.score(X_test, y_test[risk])
            scores[risk] = score
            self.models[risk] = model
            
        return scores

    def predict(self, input_data: pd.DataFrame) -> Dict[str, float]:
        X = input_data[self.feature_columns].copy()
        X['settore_attivita'] = self.label_encoder.transform(X['settore_attivita'])
        
        predictions = {}
        for risk in self.target_columns:
            pred = self.models[risk].predict(X)[0]
            predictions[risk] = pred
            
        return predictions

    def save_model(self, path: str):
        joblib.dump(self, path)

    @staticmethod
    def load_model(path: str):
        return joblib.load(path)