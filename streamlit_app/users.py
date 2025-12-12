import os
import json

class User:
    def __init__(self, id, name) -> None:
        """Create a new user based on the given name and id"""
        self.name = name
        self.id = id

    def store_data(self) -> None:
        data_to_save = {
            "devices": {
                "1": {"device_name": self.name, "managed_by_user_id": self.id, "is_active": "true"},
            }
        }
        try:
            # Prüfen, ob die Datei existiert und Daten enthält
            if os.path.exists("database.json") and os.path.getsize("database.json") > 0:
                with open("database.json", 'r', encoding='utf-8') as f:
                    db_data = json.load(f)
            else:
                # Erstelle die initiale Struktur, falls die Datei leer ist
                db_data = {"devices": {},"devices_with_subclass":{}}
        except json.JSONDecodeError:
            print(f"Fehler: '{"database.json"}' ist ungültiges JSON. Starte mit leerer Struktur.")
            db_data = {"devices": {}, "devices_with_subclass":{}}
        except Exception as e:
            print(f"Unerwarteter Fehler beim Lesen: {e}")
            return
        db_data["devices"].update(data_to_save["devices"])
        with open("database.json", 'w', encoding='utf-8') as f:
            json.dump(db_data, f, ensure_ascii=False, indent=4)


    def delete(self) -> None:
        try:
            if os.path.exists("database.json") and os.path.getsize("database.json") > 0:
                with open("database.json", 'r', encoding='utf-8') as f:
                    db_data = json.load(f)
            else:
                print(f"Fehler: Die Datei '{"database.json"}' existiert nicht oder ist leer.")
                return
        except (json.JSONDecodeError, Exception) as e:
            print(f"Fehler beim Lesen der Datei: {e}")
            return

        if "devices" in db_data:
            devices = db_data["devices"]
            if self.id in devices:
                # Löschen des Geräts aus dem Dictionary
                del devices[self.id]
                print(f"Gerät mit ID '{self.id}' erfolgreich entfernt.")
            else:
                print(f"Warnung: Gerät mit ID '{self.id}' wurde nicht gefunden.")
                return  # Keine Änderung, daher kein Zurückschreiben nötig
        else:
            print("Fehler: 'devices'-Schlüssel fehlt in der Datenbankstruktur.")
            return

        try:
            with open("database.json", 'w', encoding='utf-8') as f:
                json.dump(db_data, f, indent=4)
            print("Datenbank erfolgreich aktualisiert.")
        except Exception as e:
            print(f"Fehler beim Schreiben der Datei: {e}")


    def __str__(self):
        return f"User {self.id} - {self.name}"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def find_all(cls) -> list:
        """Find all users in the database"""
        pass

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str) -> 'User':
        """From the matches in the database, select the user with the given attribute value"""
        pass
