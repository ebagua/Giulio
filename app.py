
import streamlit as st
import pandas as pd
import calendar
from datetime import date, timedelta

# 🌴 Tema visivo vacanziero
def sfondo_tema_vacanza():
    st.markdown("""
        <style>
        .stApp {
            background-image: url("https://i.imgur.com/MTrvF7S.jpg");
            background-size: cover;
            background-attachment: fixed;
        }
        .block-container {
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 15px;
            padding: 2rem;
        }
        h1, h2, h3, label, .stNumberInput label, .stSelectbox label, .stSlider label {
            color: #FFE600 !important;
        }
        .stDataFrame, .stMetric {
            background-color: rgba(255,255,255,0.9);
        }
        footer {
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)

# 📄 Config pagina
st.set_page_config(page_title="Casa Vacanze Pietra Ligure", page_icon="🌴", layout="wide")
sfondo_tema_vacanza()

# 🌞 Titolo
st.markdown("<h1 style='text-align: center; color: #FFE600;'>🌴 Casa Vacanza – Via Rocca Crovara, Pietra Ligure</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Calcola il prezzo dinamico per ogni giorno e visualizza il tuo guadagno netto</h3>", unsafe_allow_html=True)

# 🏷️ Impostazioni
prezzo_base = st.number_input("💶 Prezzo base per notte (€)", value=150)
mese_selezionato = st.selectbox("🗓️ Mese", list(calendar.month_name)[1:], index=date.today().month - 1)
anno = date.today().year

# 🗓️ Giorni in italiano
giorni_settimana_it = {
    'Monday': 'Lunedì', 'Tuesday': 'Martedì', 'Wednesday': 'Mercoledì',
    'Thursday': 'Giovedì', 'Friday': 'Venerdì', 'Saturday': 'Sabato', 'Sunday': 'Domenica'
}

# 🎉 Festività italiane
festivita = ["01/01", "06/01", "25/04", "01/05", "02/06", "15/08", "01/11", "08/12", "25/12", "26/12"]

# 📅 Lista giorni
mese_numero = list(calendar.month_name).index(mese_selezionato)
num_giorni = calendar.monthrange(anno, mese_numero)[1]
date_mese = [date(anno, mese_numero, g) for g in range(1, num_giorni + 1)]

# 📌 Prenotazioni
prenotati = st.multiselect("📌 Seleziona le date già prenotate", date_mese, format_func=lambda d: d.strftime("%d %B %Y"))

# 📊 Tabella prezzi
records = []
for giorno in date_mese:
    nome_giorno = giorni_settimana_it[giorno.strftime('%A')]
    giorno_label = f"{nome_giorno} {giorno.day:02d} {mese_selezionato}"

    prezzo = prezzo_base

    if nome_giorno in ["Venerdì", "Sabato"]:
        prezzo *= 1.2

    if giorno.strftime("%d/%m") in festivita:
        prezzo *= 1.3

    durata = st.slider(f"📆 Soggiorno dal {giorno.day:02d}/{mese_numero:02d}", 1, 14, 1, key=str(giorno))
    if durata >= 7:
        prezzo *= 0.9

    prezzo = round(prezzo, 2)
    guadagno_netto = round(prezzo * 0.75, 2)

    records.append({
        "Data": giorno_label,
        "Prezzo (€)": prezzo,
        "Guadagno Netto (~€)": guadagno_netto,
        "Prenotato": "✅" if giorno in prenotati else ""
    })

# 📋 Mostra tabella
df = pd.DataFrame(records)
st.dataframe(df, use_container_width=True)

# 📈 Totali
totale = df[df["Prenotato"] != "✅"]["Guadagno Netto (~€)"].sum()
prenotati_count = df[df["Prenotato"] == "✅"]["Guadagno Netto (~€)"].sum()

st.markdown("---")
st.subheader("📈 Riepilogo")
col1, col2 = st.columns(2)
col1.metric("💰 Guadagno Netto Stimato (disponibili)", f"{totale:.2f} €")
col2.metric("🔒 Già Prenotati", f"{prenotati_count:.2f} €")

# 👣 Footer
st.markdown("<hr><center style='color:white;'>🏖️ Realizzato per la tua casa vacanza a Pietra Ligure | via Rocca Crovara</center>", unsafe_allow_html=True)
