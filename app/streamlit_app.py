import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model import RiskAssessmentModel
from src.pdf_generator import RiskMatrixPDF
from src.config import Config

def load_model():
    model_path = 'data/model/risk_model.joblib'
    return RiskAssessmentModel.load_model(model_path)

def main():
    st.title('Valutazione Rischi Aziendali')
    
    # Caricamento modello
    model = load_model()
    
    # Form inputs
    st.header('Inserisci i dati aziendali')
    
    settore = st.selectbox('Settore Attività', model.label_encoder.classes_)
    n_dipendenti = st.number_input('Numero Dipendenti', min_value=1, value=50)
    metri_quadri = st.number_input('Metri Quadri', min_value=1, value=100)
    numero_sedi = st.number_input('Numero Sedi', min_value=1, value=1)
    perc_determinato = st.slider('Percentuale Tempo Determinato', 0, 100, 20)
    iso_45001 = st.checkbox('Certificazione ISO 45001')
    
    st.header('Caratteristiche Ambiente Lavoro')
    macchinari = st.checkbox('Presenza Macchinari Pesanti')
    quota = st.checkbox('Lavoro in Quota')
    chimici = st.checkbox('Presenza Sostanze Chimiche')
    rumore = st.slider('Rumorosità (dB)', 40, 100, 60)
    vdt = st.checkbox('Presenza Videoterminali')
    temperatura = st.slider('Temperatura Ambiente (°C)', 15, 35, 22)
    elettrico = st.checkbox('Presenza Sistemi Elettrici')
    n_macchinari = st.number_input('Numero Macchinari', min_value=0, value=5)
    q_chimiche = st.number_input('Quantità Sostanze Chimiche (kg)', min_value=0, value=0)
    
    if st.button('Genera Valutazione'):
        # Preparazione input
        input_data = pd.DataFrame({
            'settore_attivita': [settore],
            'n_dipendenti': [n_dipendenti],
            'metri_quadri': [metri_quadri],
            'numero_sedi': [numero_sedi],
            'percentuale_tempo_determinato': [perc_determinato],
            'certificazione_iso_45001': [int(iso_45001)],
            'settore_regolamentato': [1 if settore in ['Energia', 'Industria manifatturiera'] else 0],
            'presenza_macchinari_pesanti': [int(macchinari)],
            'lavoro_in_quota': [int(quota)],
            'presenza_sostanze_chimiche': [int(chimici)],
            'rumorosita_db': [rumore],
            'presenza_videoterminali': [int(vdt)],
            'temperatura_ambiente': [temperatura],
            'presenza_sistemi_elettrici': [int(elettrico)],
            'numero_macchinari': [n_macchinari],
            'quantita_sostanze_chimiche': [q_chimiche]
        })
        
        # Predizione
        predictions = model.predict(input_data)
        
        # Creazione PDF
        pdf_generator = RiskMatrixPDF()
        pdf_path = 'valutazione_rischi.pdf'
        pdf_generator.create_pdf(pdf_path, input_data.iloc[0].to_dict(), predictions)
        
        # Preview risultati
        st.header('Risultati Valutazione')
        for risk, value in predictions.items():
            if value > 0.1:
                st.write(f"{risk.replace('_', ' ').title()}: {value:.2f}")
                if value < 0.3:
                    st.success("Rischio Basso")
                elif value < 0.7:
                    st.warning("Rischio Medio")
                else:
                    st.error("Rischio Alto")
        
        # Download button per il PDF
        with open(pdf_path, 'rb') as file:
            st.download_button(
                label='Download Documento Valutazione (PDF)',
                data=file,
                file_name='valutazione_rischi.pdf',
                mime='application/pdf'
            )

if __name__ == '__main__':
    main()