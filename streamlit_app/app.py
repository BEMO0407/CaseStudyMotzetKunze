import streamlit as st

st.set_page_config(page_title="Geräteverwaltung", layout="centered")

st.title("Geräteverwaltung - Hochschule")


#hier kommt die sidebar mit überunterschriften 
main_page= st.sidebar.selectbox(
    "Bereich auswählen",
    [ "Geräte verwalten", "Nutzer-Verwaltung","Reservierungssystem", "Wartungs-Management"]
)

sub_page = None

if main_page == "Geräte verwalten":
    sub_page = st.sidebar.selectbox(
        "Option auswählen",
        ["Gerät anlegen", "Geräte ändern"]
    )

elif main_page == "Nutzer-Verwaltung":
    sub_page= st.sidebar.selectbox(
        "",
        ["Nutzer anlegen"]
    )

elif main_page == "Wartungs-Management":
    sub_page = st.sidebar.selectbox(
        "",
        ["Wartungen anzeigen", "Wartungskosten anzeigen"]
    )

elif main_page == "Reservierungssystem":
    sub_page = st.sidebar.selectbox(
        "",
        ["Reservierungen anzeigen", "Reservierung ein/ austragen"]
    )

st.header(f"{main_page} -> {sub_page}")
st.write("Hier kommt später Inhalt rein.")