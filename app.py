
[CODICE APP.PY — omesso per brevità in questo commento ma sarà ricreato nel file]
import streamlit as st
import pandas as pd
import calendar
from datetime import date, datetime, timedelta

# Configurazione pagina
st.set_page_config(page_title="Affitto Pietra Ligure", page_icon="🌴", layout="wide")
st.title("🌴 Calcolatore Affitto a Pietra Ligure")
st.markdown("Personalizza i prezzi per ogni giorno, visualizza il guadagno netto e segna le date già prenotate.")

# Impostazioni utente
prezzo_base = st.number_input("💶 Prezzo base per notte (€)", value=150)
mese_selezionato = st.selectbox("🗓️ Mese", list(calendar.month_name)[1:], index=date.today().month - 1)
anno = date.today().year

# Traduzione giorni
giorni_settimana_it = {
    'Monday': 'Lunedì', 'Tuesday': 'Martedì', 'Wednesday': 'Mercoledì',
    'Thursday': 'Giovedì', 'Friday': 'Venerdì', 'Saturday': 'Sabato', 'Sunday': 'Domenica'
}

# Festività italiane principali
festivita = ["01/01", "06/01", "25/04", "01/05", "02/06", "15/08", "01/11", "08/12", "25/12", "26/12"]

# Crea lista giorni del mese
mese_numero = list(calendar.month_name).index(mese_selezionato)
num_giorni = calendar.monthrange(anno, mese_numero)[1]
date_mese = [date(anno, mese_numero, g) for g in range(1, num_giorni + 1)]

# Seleziona giorni già prenotati
prenotati = st.multiselect("📌 Seleziona le date già prenotate", date_mese, format_func=lambda d: d.strftime("%d %B %Y"))

# Tabella prezzi
records = []

for giorno in date_mese:
    nome_giorno = giorni_settimana_it[giorno.strftime('%A')]
    giorno_label = f"{nome_giorno} {giorno.day:02d} {mese_selezionato}"

    prezzo = prezzo_base

    # Aumento weekend
    if nome_giorno in ["Venerdì", "Sabato"]:
        prezzo *= 1.2

    # Aumento festività
    if giorno.strftime("%d/%m") in festivita:
        prezzo *= 1.3

    # Sconto lunga permanenza
    durata = st.slider(f"📆 Soggiorno dal {giorno.day:02d}/{mese_numero:02d}", 1, 14, 1, key=str(giorno))
    if durata >= 7:
        prezzo *= 0.9  # 10% di sconto

    prezzo = round(prezzo, 2)
    guadagno_netto = round(prezzo * 0.75, 2)  # 25% trattenuto da Booking

    records.append({
        "Data": giorno_label,
        "Prezzo (€)": prezzo,
        "Guadagno Netto (~€)": guadagno_netto,
        "Prenotato": "✅" if giorno in prenotati else ""
    })

# Mostra tabella
df = pd.DataFrame(records)
st.dataframe(df, use_container_width=True)

# Totale guadagno netto stimato
totale = df[df["Prenotato"] != "✅"]["Guadagno Netto (~€)"].sum()
prenotati_count = df[df["Prenotato"] == "✅"]["Guadagno Netto (~€)"].sum()

st.markdown("---")
st.subheader("📈 Riepilogo")
col1, col2 = st.columns(2)
col1.metric("💰 Guadagno Netto Stimato (disponibili)", f"{totale:.2f} €")
col2.metric("🔒 Già Prenotati", f"{prenotati_count:.2f} €")

st.markdown("🌺 App sviluppata su misura per te! Vuoi aggiungere il calendario visivo o esportare PDF? Scrivimelo 😊")
