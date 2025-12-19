import streamlit as st
import devices

# Grundeinstellungen für die Seite
st.set_page_config(page_title="Geräteverwaltung", layout="centered")

st.title("Geräteverwaltung")

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
        st.write("### Neues Gerät hinzufügen")
        with st.form("device_form", clear_on_submit=True):
            device_name = st.text_input("Gerätename", placeholder="z.B. Laptop")
            managed_by = st.text_input("Verantwortlicher Nutzer (E-Mail)", placeholder="nutzer@mci.edu")

            submit_button = st.form_submit_button("Gerät speichern")

            if submit_button:
                if device_name and managed_by:
                    # Erstellen einer Instanz der Device-Klasse
                    new_device = devices.Device(device_name=device_name, managed_by_user_id=managed_by)

                    new_device.store_data()

                    st.success(f"Gerät '{device_name}' wurde erfolgreich angelegt!")
                else:
                    st.error("Bitte füllen Sie beide Felder aus.")

    elif sub_page == "Geräte-Liste anzeigen":
        st.write("### Übersicht aller Geräte")

        devices = devices.Device.find_all()

        if devices:
            device_data = []
            for d in devices:
                device_data.append({
                    "Gerätename": d.device_name,
                    "Verantwortlich": d.managed_by_user_id,
                    "Aktiv": "Ja" if d.is_active else "Nein"
                })
            st.table(device_data)
        else:
            st.info("Noch keine Geräte in der Datenbank vorhanden.")



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
