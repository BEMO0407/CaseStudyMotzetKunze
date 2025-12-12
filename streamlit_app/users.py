from tinydb import TinyDB, Query


class User:
    def __init__(self, id, name) -> None:
        """Create a new user based on the given name and id"""
        self.name = name
        self.id = id

    def store_data(self) -> None:
        data_to_save ={
            "device_name": self.name,
             "managed_by_user_id": self.id,
             "is_active": True
        }

        db = TinyDB("database.json")
        devices_table = db.table("devices")
        doc_id = devices_table.insert(data_to_save)
        print(f"Gerät erfolgreich mit Document ID: {doc_id} eingefügt.")
        db.close()

    def delete(self) -> None:
        try:
            db = TinyDB("database.json")
            devices_table = db.table("devices")
            Device = Query()

            removed_count = devices_table.remove(Device.device_name == self.name)
            db.close()
            if removed_count > 0:
                print(f"Erfolg: {removed_count} Gerät(e) mit dem Namen '{self.name}' gelöscht.")
            else:
                print(f"Warnung: Kein Gerät mit dem Namen '{self.name}' in der Datenbank gefunden.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")


    def __str__(self):
        return f"User {self.id} - {self.name}"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def find_all(cls) -> list:
        """Find all users in the database"""
        try:
            db = TinyDB("database.json")
            devices_table = db.table("devices")
            return list(devices_table.all())
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return []

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str) -> 'User':
        """From the matches in the database, select the user with the given attribute value"""

        db = TinyDB("database.json")
        user_table = db.table("devices")
        UserQuery = Query()
        user_data = user_table.get(UserQuery[by_attribute] == attribute_value)
        db.close()
        if user_data:
            return cls(
                user_data.get("managed_by_user_id"),
                user_data.get("device_name")
             )
        return None

