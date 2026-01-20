import streamlit as st
from datetime import datetime

from devices_inheritance import Device
from users_inheritance import User
from reservation_service import ReservationService
import wartungs_management
from datetime import time

st.set_page_config(page_title="Geräteverwaltung", layout="centered")

st.title("Geräteverwaltung")

# ---------- HAUPTBEREICH----------
main_page = st.sidebar.selectbox(
    "Bereich auswählen",
    ["", "Geräte verwalten", "Nutzer-Verwaltung", "Reservierungssystem", "Wartungs-Management"]
)

# ---------- HEADER ----------
if main_page:
    st.subheader(main_page)

# ---------- LOGIK ----------

if main_page == "":
    st.info("Bitte wählen Sie eine Option in der Sidebar.")

# ==========================
# GERÄTE VERWALTUNG
# ==========================
elif main_page == "Geräte verwalten":
    sub_page = st.radio(
        "Aktion auswählen:",
        ["Gerät anlegen", "Geräte-Liste anzeigen"],
        horizontal=True
    )

    if sub_page == "Gerät anlegen":
        st.write("### Neues Gerät hinzufügen")

        users_list = User.find_all()
        user_options = {u.id: f"{u.name} ({u.id})" for u in users_list} if users_list else {}

        with st.form("device_form", clear_on_submit=True):
            device_id = st.text_input("Geräte-ID / Name", placeholder="z.B. Device1")

            if user_options:
                managed_by = st.selectbox("Verantwortlicher Nutzer", options=list(user_options.keys()),
                                          format_func=lambda x: user_options[x])
            else:
                managed_by = st.text_input("Verantwortlicher Nutzer (User-ID/Email)", placeholder="email@mci.edu")
                st.warning("Keine Nutzer gefunden. Bitte erst Nutzer anlegen oder ID manuell eingeben.")

            submit_button = st.form_submit_button("Gerät speichern")

            if submit_button:
                if device_id and managed_by:
                    if Device.find_by_attribute("id", device_id):
                        st.error(f"Ein Gerät mit der ID '{device_id}' existiert bereits.")
                    else:
                        new_device = Device(id=device_id, managed_by_user_id=managed_by)
                        new_device.store_data()
                        st.success(f"Gerät '{device_id}' wurde erfolgreich angelegt!")
                else:
                    st.error("Bitte alle Felder ausfüllen.")

    elif sub_page == "Geräte-Liste anzeigen":
        st.write("### Übersicht aller Geräte")

        all_devices = Device.find_all()

        if all_devices:
            device_data = []
            for d in all_devices:
                device_data.append({
                    "Geräte-ID": d.id,
                    "Verantwortlich": d.managed_by_user_id,
                    "Aktiv": "Ja" if d.is_active else "Nein",
                    "End of Life": d.end_of_life
                })
            st.dataframe(device_data, use_container_width=True)
        else:
            st.info("Noch keine Geräte in der Datenbank vorhanden.")


# ==========================
# NUTZER VERWALTUNG
# ==========================
elif main_page == "Nutzer-Verwaltung":
    sub_page = st.radio(
        "Aktion auswählen:",
        ["Nutzer anlegen", "Nutzer-Liste anzeigen"],
        horizontal=True
    )

    if sub_page == "Nutzer anlegen":
        st.write("### Neuen Nutzer hinzufügen")
        with st.form("user_form", clear_on_submit=True):
            u_id = st.text_input("E-Mail Adresse (Dient als ID)", placeholder="name@mci.edu")
            u_name = st.text_input("Name des Nutzers")

            submit_user = st.form_submit_button("Nutzer speichern")

            if submit_user:
                if u_id and u_name:
                    if User.find_by_attribute("id", u_id):
                        st.error("Dieser Nutzer (ID) existiert bereits.")
                    else:
                        new_user = User(id=u_id, name=u_name)
                        new_user.store_data()
                        st.success(f"Nutzer {u_name} wurde angelegt.")
                else:
                    st.error("Bitte alle Felder ausfüllen.")

    elif sub_page == "Nutzer-Liste anzeigen":
        st.write("### Übersicht aller Nutzer")
        all_users = User.find_all()

        if all_users:
            for u in all_users:
                with st.expander(f"{u.name} ({u.id})"):
                    user_devices = Device.find_by_attribute("managed_by_user_id", u.id, num_to_return=-1)  # -1 für alle

                    if user_devices:
                        st.write("**Verwaltete Geräte:**")
                        if isinstance(user_devices, list):
                            for d in user_devices:
                                st.write(f"- {d.id}")
                        else:
                            st.write(f"- {user_devices.id}")
                    else:
                        st.info("Diesem Nutzer sind aktuell keine Geräte zugeordnet.")
        else:
            st.info("Keine Nutzer gefunden.")


# ==========================
# RESERVIERUNGSSYSTEM
# ==========================
elif main_page == "Reservierungssystem":
    sub_page = st.radio(
        "Aktion auswählen:",
        ["Neue Reservierung", "Reservierungen anzeigen"],
        horizontal=True
    )

    res_service = ReservationService()

    if sub_page == "Neue Reservierung":
        st.write("### Gerät reservieren")

        users_list = User.find_all()
        devices_list = Device.find_all()

        if not users_list or not devices_list:
            st.error("Es müssen zuerst Nutzer und Geräte angelegt werden.")
        else:
            with st.form("res_form"):
                user_options = {u.id: f"{u.name} ({u.id})" for u in users_list}
                device_options = {d.id: f"{d.id}" for d in devices_list}

                selected_user_id = st.selectbox("Nutzer", options=list(user_options.keys()),
                                                format_func=lambda x: user_options[x])
                selected_device_id = st.selectbox("Gerät", options=list(device_options.keys()),
                                                  format_func=lambda x: device_options[x])

                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Startdatum")
                    start_time = st.time_input("Startzeit")
                with col2:
                    end_date = st.date_input("Enddatum")
                    end_time = st.time_input("Endzeit")

                submit_res = st.form_submit_button("Reservieren")

                if submit_res:
                    dt_start = datetime.combine(start_date, start_time)
                    dt_end = datetime.combine(end_date, end_time)

                    if dt_start >= dt_end:
                        st.error("Das Enddatum muss nach dem Startdatum liegen.")
                    else:
                        try:
                            res_service.create_reservation(
                                user_id=selected_user_id,
                                device_id=selected_device_id,
                                start_date=dt_start,
                                end_date=dt_end
                            )
                            st.success("Reservierung erfolgreich erstellt!")
                        except ValueError as e:
                            st.error(f"Fehler: {e}")

    elif sub_page == "Reservierungen anzeigen":
        st.write("### Alle Reservierungen")
        reservations = res_service.find_all_reservations()

        if reservations:
            res_data = []
            for r in reservations:
                res_data.append({
                    "Gerät": r.device_id,
                    "Nutzer": r.user_id,
                    "Von": r.start_date,
                    "Bis": r.end_date
                })
            st.dataframe(res_data, use_container_width=True)
        else:
            st.info("Keine Reservierungen vorhanden.")

# ==========================
# WARTUNGS MANAGEMENT
# ==========================
elif main_page == "Wartungs-Management":
    st.write("### Wartungs-Management")

    next_maintenance = wartungs_management.Maintenance.get_next_maintenance()

    if next_maintenance:
        date_str = next_maintenance.appointment_date.strftime("%d.%m.%Y")
        time_str = next_maintenance.appointment_date.strftime("%H:%M")

        st.info(f"🔧 **Nächster Wartungstermin:** {date_str} um {time_str} Uhr\n\n**Grund:** {next_maintenance.reason}")


    st.divider()

    st.write("#### Neuen Wartungstermin planen")

    with st.form("maintenance_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            m_date = st.date_input("Datum")
        with col2:
            m_time = st.time_input("Uhrzeit", value=time(9, 0))

        m_reason = st.text_input("Grund für die Wartung", placeholder="z.B. Server-Update, Hardware-Austausch")

        submit_maint = st.form_submit_button("Termin speichern")

        if submit_maint:
            if m_reason:
                dt_appointment = datetime.combine(m_date, m_time)

                new_maint = wartungs_management.Maintenance(appointment_date=dt_appointment, reason=m_reason)
                new_maint.store_data()

                st.success("Wartungstermin wurde erfolgreich eingetragen.")

                st.rerun()
            else:
                st.error("Bitte geben Sie einen Grund für die Wartung an.")