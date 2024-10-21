import pandas as pd
import numpy as np
from typing import List, Dict
from src.config import Config
from src.utils import setup_logging

class RiskDataGenerator:
    def __init__(self):
        self.settori = ['Agricoltura', 'Industria manifatturiera', 'Servizi', 'Commercio', 
                       'Tecnologia', 'Telecomunicazioni', 'Energia', 'Edilizia', 
                       'Trasporti e logistica', 'Finanza e assicurazioni', 'Sanità', 
                       'Educazione', 'Media e intrattenimento', 'Turismo']
        
        self.rischi = ['rischio_meccanico', 'rischio_caduta', 'rischio_chimico', 
                      'rischio_rumore', 'rischio_elettrico', 'rischio_termico',
                      'rischio_vibrazioni', 'rischio_biologico', 'rischio_movimentazione',
                      'rischio_posturale', 'rischio_stress', 'rischio_inquinamento',
                      'rischio_eventi_naturali', 'rischio_informatica', 'rischio_regolamentato']
        
        self.settori_regolamentati = ['Energia', 'Industria manifatturiera']

    def generate_sample(self) -> Dict:
        settore = np.random.choice(self.settori)
        
        sample = {
            'settore_attivita': settore,
            'n_dipendenti': np.random.randint(5, 1000),
            'metri_quadri': np.random.randint(50, 10000),
            'numero_sedi': np.random.randint(1, 10),
            'percentuale_tempo_determinato': np.random.uniform(0, 100),
            'certificazione_iso_45001': np.random.choice([0, 1]),
            'settore_regolamentato': 1 if settore in self.settori_regolamentati else 0,
            'presenza_macchinari_pesanti': np.random.choice([0, 1]),
            'lavoro_in_quota': np.random.choice([0, 1]),
            'presenza_sostanze_chimiche': np.random.choice([0, 1]),
            'rumorosita_db': np.random.uniform(40, 100),
            'presenza_videoterminali': np.random.choice([0, 1]),
            'temperatura_ambiente': np.random.uniform(15, 35),
            'presenza_sistemi_elettrici': np.random.choice([0, 1]),
            'numero_macchinari': np.random.randint(0, 100),
            'quantita_sostanze_chimiche': np.random.uniform(0, 1000)
        }
        
        # Generazione rischi basata sulle caratteristiche
        rischi = {}
        
        # Rischio meccanico
        if sample['presenza_macchinari_pesanti'] or sample['numero_macchinari'] > 20:
            rischi['rischio_meccanico'] = np.random.uniform(0.6, 1.0)
        else:
            rischi['rischio_meccanico'] = np.random.uniform(0, 0.3)
            
        # Rischio caduta
        if sample['lavoro_in_quota']:
            rischi['rischio_caduta'] = np.random.uniform(0.7, 1.0)
        else:
            rischi['rischio_caduta'] = np.random.uniform(0, 0.2)
            
        # Rischio chimico
        if sample['presenza_sostanze_chimiche']:
            rischi['rischio_chimico'] = np.clip(sample['quantita_sostanze_chimiche'] / 1000, 0, 1)
        else:
            rischi['rischio_chimico'] = 0
            
        # Altri rischi...
        rischi['rischio_rumore'] = np.clip((sample['rumorosita_db'] - 40) / 60, 0, 1)
        rischi['rischio_elettrico'] = 0.8 if sample['presenza_sistemi_elettrici'] else 0.1
        rischi['rischio_informatica'] = 0.7 if sample['presenza_videoterminali'] else 0.2
        
        sample.update(rischi)
        return sample

    def generate_dataset(self, n_samples: int = 1000) -> pd.DataFrame:
        data = []
        for _ in range(n_samples):
            data.append(self.generate_sample())
        return pd.DataFrame(data)

def main():
    generator = RiskDataGenerator()
    df = generator.generate_dataset(n_samples=1000)
    df.to_csv('data/training_data.csv', index=False)

if __name__ == "__main__":
    main()