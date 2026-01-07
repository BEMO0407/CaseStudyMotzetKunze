import streamlit as st
import devices, users

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
        st.write("### Neuen Nutzer hinzufügen")
        with st.form("user_form", clear_on_submit=True):
            u_name = st.text_input("Name des Nutzers")
            u_mail = st.text_input("E-Mail Adresse")

            submit_user = st.form_submit_button("Nutzer speichern")

            if submit_user:
                if u_name and u_mail:
                    new_user = users.User(user_name=u_name, user_email=u_mail)
                    new_user.store_data()
                    st.success(f"Nutzer {u_name} wurde angelegt.")
                else:
                    st.error("Bitte alle Felder ausfüllen.")

    elif sub_page == "Nutzer-Liste anzeigen":
        st.write("### Übersicht aller Nutzer")
        all_users = users.User.find_all()

        if all_users:
            for u in all_users:
                with st.expander(f"{u.user_name} ({u.user_email})"):
                    # Hier suchen wir die zugehörigen Geräte aus der Device-DB
                    user_devices = devices.Device.find_by_attribute("managed_by_user_id", u.user_email,
                                                                    num_to_return=10)

                    if user_devices:
                        st.write("**Zugeordnete Geräte:**")
                        # Falls nur ein Gerät gefunden wird, ist es kein Array (wegen deiner find_by_attribute Logik)
                        if isinstance(user_devices, list):
                            for d in user_devices:
                                st.write(f"- {d.device_name}")
                        else:
                            st.write(f"- {user_devices.device_name}")
                    else:
                        st.info("Diesem Nutzer sind aktuell keine Geräte zugeordnet.")
        else:
            st.info("Keine Nutzer gefunden.")
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

