import os
from tinydb import TinyDB, Query
from serializer import serializer


class User:
    # Wir nutzen die database_user.json, wie von dir oben definiert
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database_user.json'),
                          storage=serializer).table('users')

    def __init__(self, user_name: str, user_email: str) -> None:
        """Create a new user based on the given name and email (id)"""
        self.user_name = user_name
        self.user_email = user_email  # Das ist deine ID

    def store_data(self) -> None:
        # Wir speichern die Daten direkt in den db_connector der Klasse
        data_to_save = {
            "user_name": self.user_name,
            "user_email": self.user_email
        }

        UserQuery = Query()
        # Prüfen, ob User schon existiert
        result = self.db_connector.search(UserQuery.user_email == self.user_email)
        if result:
            self.db_connector.update(data_to_save, doc_ids=[result[0].doc_id])
            print(f"Nutzer {self.user_name} aktualisiert.")
        else:
            doc_id = self.db_connector.insert(data_to_save)
            print(f"Nutzer erfolgreich mit Document ID: {doc_id} eingefügt.")

    def delete(self) -> None:
        try:
            UserQuery = Query()
            removed_count = self.db_connector.remove(UserQuery.user_email == self.user_email)
            if removed_count:
                print(f"Erfolg: Nutzer '{self.user_name}' gelöscht.")
            else:
                print(f"Warnung: Kein Nutzer mit E-Mail '{self.user_email}' gefunden.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

    def __str__(self):
        return f"User {self.user_email} - {self.user_name}"

    def __repr__(self):
        return self.__str__()

    @classmethod  # Geändert von staticmethod zu classmethod, damit cls funktioniert
    def find_all(cls) -> list:
        """Find all users in the database"""
        try:
            # Wir geben direkt Objekte der Klasse User zurück
            return [cls(d['user_name'], d['user_email']) for d in cls.db_connector.all()]
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return []

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str) -> 'User':
        """Select the user with the given attribute value"""
        UserQuery = Query()
        user_data = cls.db_connector.get(UserQuery[by_attribute] == attribute_value)
        if user_data:
            return cls(
                user_data.get("user_name"),
                user_data.get("user_email")
            )
        return None