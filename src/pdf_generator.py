from fpdf import FPDF
import pandas as pd
from datetime import datetime

class RiskMatrixPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        # Dizionario con descrizioni e misure per ogni tipo di rischio
        self.risk_details = {
            'rischio_meccanico': {
                'descrizione': 'Rischi derivanti dall\'uso di macchinari, attrezzature e utensili che possono causare lesioni da schiacciamento, taglio, urto o trascinamento.',
                'misure': [
                    'Formazione specifica per gli operatori',
                    'Manutenzione periodica dei macchinari',
                    'Installazione di dispositivi di protezione',
                    'Segnaletica di sicurezza',
                    'Procedure operative di sicurezza'
                ]
            },
            'rischio_chimico': {
                'descrizione': 'Rischi derivanti dall\'esposizione a sostanze chimiche pericolose che possono causare danni alla salute per inalazione, contatto o ingestione.',
                'misure': [
                    'Schede di sicurezza disponibili e aggiornate',
                    'DPI specifici per sostanze chimiche',
                    'Sistemi di ventilazione adeguati',
                    'Procedure di manipolazione sicura',
                    'Formazione sul rischio chimico'
                ]
            },
            'rischio_elettrico': {
                'descrizione': 'Rischi derivanti da contatti diretti o indiretti con parti elettriche in tensione che possono causare shock elettrici o ustioni.',
                'misure': [
                    'Manutenzione impianti elettrici',
                    'Verifiche periodiche messa a terra',
                    'Procedure di lockout/tagout',
                    'Formazione specifica',
                    'Segnaletica di sicurezza elettrica'
                ]
            },
            'rischio_caduta': {
                'descrizione': 'Rischi derivanti da lavori in quota o presenza di dislivelli che possono causare cadute dall\'alto o scivolamenti.',
                'misure': [
                    'Installazione parapetti e linee vita',
                    'Utilizzo DPI anticaduta',
                    'Formazione lavori in quota',
                    'Manutenzione scale e ponteggi',
                    'Procedure di emergenza specifiche'
                ]
            },
            'rischio_ergonomico': {
                'descrizione': 'Rischi derivanti da posture incongrue, movimenti ripetitivi o movimentazione manuale dei carichi.',
                'misure': [
                    'Postazioni di lavoro ergonomiche',
                    'Formazione sulla movimentazione carichi',
                    'Pause programmate',
                    'Ausili meccanici per movimentazione',
                    'Rotazione delle mansioni'
                ]
            },
            'rischio_rumore': {
                'descrizione': 'Rischi derivanti dall\'esposizione a rumore che può causare danni all\'apparato uditivo e stress.',
                'misure': [
                    'Valutazione specifica del rumore',
                    'DPI uditivi appropriati',
                    'Manutenzione antirumore macchinari',
                    'Cabine o barriere fonoassorbenti',
                    'Turnazione del personale'
                ]
            }
        }
        self.add_page()
        self.set_font('Arial', 'B', 16)
        
    def create_header(self):
        self.cell(0, 10, 'Valutazione dei Rischi Aziendali', 0, 1, 'C')
        self.ln(10)
        
    def add_info_table(self, data):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        
        col_width = self.w / 2 - 20
        
        self.cell(col_width, 10, 'Caratteristica', 1, 0, 'C', True)
        self.cell(col_width, 10, 'Valore', 1, 1, 'C', True)
        
        self.set_font('Arial', '', 10)
        for key, value in data.items():
            key_formatted = key.replace('_', ' ').title()
            
            if isinstance(value, bool):
                value = 'Sì' if value else 'No'
            elif isinstance(value, float):
                value = f"{value:.2f}"
            elif isinstance(value, int):
                value = str(value)
                
            self.multi_cell(col_width, 10, key_formatted, 1, 'L')
            self.set_xy(self.get_x() + col_width, self.get_y() - 10)
            self.multi_cell(col_width, 10, str(value), 1, 'C')
            
    def add_risk_matrix(self, predictions):
        self.add_page()
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Matrice dei Rischi', 0, 1, 'C')
        self.ln(5)
        
        for risk, value in predictions.items():
            if value > 0.1:  # Mostra solo rischi significativi
                # Determinazione livello di rischio e colore
                if value < 0.3:
                    level = 'Basso'
                    self.set_fill_color(144, 238, 144)  # Verde chiaro
                elif value < 0.7:
                    level = 'Medio'
                    self.set_fill_color(255, 255, 153)  # Giallo chiaro
                else:
                    level = 'Alto'
                    self.set_fill_color(255, 182, 193)  # Rosa chiaro
                    
                # Titolo del rischio
                self.set_font('Arial', 'B', 12)
                risk_formatted = risk.replace('_', ' ').title()
                self.cell(0, 10, f"{risk_formatted} - Livello: {level} ({value:.2f})", 1, 1, 'L', True)
                
                # Reset colore di riempimento
                self.set_fill_color(255, 255, 255)
                
                # Descrizione del rischio
                self.set_font('Arial', 'B', 10)
                self.cell(0, 8, 'Descrizione:', 0, 1, 'L')
                self.set_font('Arial', '', 10)
                if risk in self.risk_details:
                    self.multi_cell(0, 6, self.risk_details[risk]['descrizione'], 0, 'L')
                else:
                    self.multi_cell(0, 6, 'Descrizione non disponibile', 0, 'L')
                self.ln(3)
                
                # Misure da intraprendere
                self.set_font('Arial', 'B', 10)
                self.cell(0, 8, 'Misure di Prevenzione e Protezione:', 0, 1, 'L')
                self.set_font('Arial', '', 10)
                if risk in self.risk_details:
                    for misura in self.risk_details[risk]['misure']:
                        self.cell(10, 6, chr(149), 0, 0, 'R')  # Bullet point
                        self.cell(0, 6, misura, 0, 1, 'L')
                else:
                    self.multi_cell(0, 6, 'Misure non disponibili', 0, 'L')
                
                self.ln(5)
                
    def create_pdf(self, output_path, input_data, predictions):
        # Creazione intestazione
        self.create_header()
        
        # Aggiunta data generazione
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'Data generazione: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'R')
        self.ln(5)
        
        # Aggiunta tabella informazioni
        self.add_info_table(input_data)
        
        # Aggiunta matrice dei rischi
        self.add_risk_matrix(predictions)
        
        # Salvataggio PDF
        self.output(output_path)