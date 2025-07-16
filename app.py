import streamlit as st
import pandas as pd
import calendar
from datetime import date, timedelta

# Configurazione pagina
st.set_page_config(page_title="Affitti Pietra Ligure", page_icon="🏖️", layout="wide")

# Stile personalizzato (tema vacanza con palme)
st.markdown("""
    <style>
    body {
        background-color: #f0f8ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 1rem;
        max-width: 900px;
        margin: auto;
    }
    h1, h2, h3 {
        color: #008080;
        text-align: center;
    }
    .st-bd {
        font-size: 18px;
    }
    .css-18e3th9 {
        padding-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Titolo e descrizione
st.markdown("<div class='main'>", unsafe_allow_html=True)
st.markdown("<h1>🏖️ Affitti Brevi - Pietra Ligure</h1>", unsafe_allow_html=True)
st.markdown("<h3>Gestione Prezzi, Guadagni e Prenotazioni</h3>", unsafe_allow_html=True)

# Prezzo base e mese
prezzo_base = st.number_input("💶 Prezzo base per notte (€)", value=140)
mese_selezionato = st.selectbox("📆 Seleziona il mese", list(calendar.month_name)[1:], index=date.today().month - 1)
anno_corrente = date.today().year

# Giorni in italiano
giorni_settimana_it = {
    'Monday': 'Lunedì', 'Tuesday': 'Martedì', 'Wednesday': 'Mercoledì',
    'Thursday': 'Giovedì', 'Friday': 'Venerdì', 'Saturday': 'Sabato', 'Sunday': 'Domenica'
}

# Festività principali italiane
festivita = ["01/01", "06/01", "25/04", "01/05", "02/06", "15/08", "01/11", "08/12", "25/12", "26/12"]

# Costruisci il calendario
mese_num = list(calendar.month_name).index(mese_selezionato)
num_giorni = calendar.monthrange(anno_corrente, mese_num)[1]
giorni = [date(anno_corrente, mese_num, g) for g in range(1, num_giorni + 1)]

# Date prenotate
prenotati = st.multiselect("🔴 Seleziona le date già prenotate", giorni, format_func=lambda d: d.strftime("%d %B %Y"))

# Tabella dati
dati = []

for giorno in giorni:
    nome_giorno = giorni_settimana_it[giorno.strftime('%A')]
    data_label = f"{nome_giorno} {giorno.day:02d} {mese_selezionato}"

    prezzo = prezzo_base

    # Aumento weekend
    if nome_giorno in ["Venerdì", "Sabato"]:
        prezzo *= 1.2

    # Aumento festività
    if giorno.strftime("%d/%m") in festivita:
        prezzo *= 1.3

    # Sconto per soggiorno lungo (da 7 giorni in su)
    soggiorno = st.slider(f"Soggiorno da {giorno.day:02d}/{mese_num:02d}", 1, 14, 1, key=str(giorno))
    if soggiorno >= 7:
        prezzo *= 0.9

    prezzo = round(prezzo, 2)
    netto = round(prezzo * 0.75, 2)  # 25% trattenuto da Booking circa

    dati.append({
        "Data": data_label,
        "Prezzo (€)": prezzo,
        "Guadagno Netto (~€)": netto,
        "Prenotato": "✅" if giorno in prenotati else ""
    })

df = pd.DataFrame(dati)
st.dataframe(df, use_container_width=True)

# Riepilogo
tot_netto = df[df["Prenotato"] != "✅"]["Guadagno Netto (~€)"].sum()
tot_prenotato = df[df["Prenotato"] == "✅"]["Guadagno Netto (~€)"].sum()

st.markdown("---")
st.subheader("📊 Riepilogo Totale")
c1, c2 = st.columns(2)
c1.metric("🟢 Guadagno Netto Stimato (libero)", f"{tot_netto:.2f} €")
c2.metric("🔴 Guadagno Netto Prenotato", f"{tot_prenotato:.2f} €")

# Calendario visivo con date prenotate
st.markdown("---")
st.subheader("🗓️ Calendario Prenotazioni")

calendar_table = pd.DataFrame({
    "Data": [d.strftime("%d/%m/%Y") for d in giorni],
    "Prenotato": ["🔴" if d in prenotati else "🟢" for d in giorni]
})

st.dataframe(calendar_table, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
