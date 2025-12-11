import streamlit as st

# Grundeinstellungen für die Seite
st.set_page_config(page_title="Geräteverwaltung", layout="centered")

st.title("Geräteverwaltung – Hochschule")

# ---------- HAUPTBEREICH IN DER SIDEBAR ----------
main_page = st.sidebar.selectbox(
    "Bereich auswählen",
    ["","Geräte verwalten", "Nutzer-Verwaltung", "Reservierungssystem", "Wartungs-Management"]
)

# ---------- MITTLERER BEREICH: HEADER ----------
st.subheader(main_page)

# ---------- UNTERBEREICHE IN DER MITTE ----------
if main_page == "":
    st.write("Wählen Sie ihre Option in der Sidebar")




elif main_page == "Geräte verwalten":
    sub_page = st.radio(
        "Aktion auswählen:",
        ["Gerät anlegen", "Geräte-Liste anzeigen"],
        horizontal=True
    )

    if sub_page == "Gerät anlegen":
        st.write("Hier kommt später das Formular zum Anlegen eines Geräts hin. (Placeholder)")
    elif sub_page == "Geräte-Liste anzeigen":
        st.write("Hier wird später eine Tabelle mit allen Geräten stehen. (Placeholder)")




elif main_page == "Nutzer-Verwaltung":
    sub_page = st.radio(
        "Aktion auswählen:",
        ["Nutzer anlegen", "Nutzer-Liste anzeigen"],
        horizontal=True
    )

    if sub_page == "Nutzer anlegen":
        st.write("Hier kommt später das Formular zum Anlegen von Nutzern hin. (Placeholder)")
    elif sub_page == "Nutzer-Liste anzeigen":
        st.write("Hier steht später eine Übersicht aller Nutzer. (Placeholder)")

elif main_page == "Reservierungssystem":
    sub_page = st.radio(
        "Aktion auswählen:",
        ["Neue Reservierung", "Reservierungen anzeigen"],
        horizontal=True
    )

    if sub_page == "Neue Reservierung":
        st.write("Hier wird später eine neue Reservierung angelegt. (Placeholder)")
    elif sub_page == "Reservierungen anzeigen":
        st.write("Hier werden alle Reservierungen gelistet. (Placeholder)")

elif main_page == "Wartungs-Management":
    sub_page = st.radio(
        "Aktion auswählen:",
        ["Wartung planen", "Wartungshistorie anzeigen"],
        horizontal=True
    )

    if sub_page == "Wartung planen":
        st.write("Hier planst du zukünftige Wartungen. (Placeholder)")
    elif sub_page == "Wartungshistorie anzeigen":
        st.write("Hier wird die Wartungshistorie angezeigt. (Placeholder)")
