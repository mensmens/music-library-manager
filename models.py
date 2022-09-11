import json, os


class Datastorage:
    def __init__(self):
        """
        Sets default path and creates file if not existend.
        """
        self.path: str = "./data.json"
        if not self.exists():
            self.write([])
    
    def exists(self) -> bool:
        """
        Checks if the file exists.

        Returns:
            bool: True if it exists and is a file else False.
        """
        if os.path.exists(self.path) and os.path.isfile(self.path):
            return True
        return False

    def read(self) -> list:
        """
        Returns the content of the file.

        Returns:
            list: Content of the file.
        """
        with open(self.path, "r", encoding="utf-8") as f:
            data: list = json.load(f)
        return data
    
    def write(self, data: list) -> bool:
        """
        Writes given data to file.

        Args:
            data (list): Whole content of the file. Must be a list!

        Returns:
            bool: True if succeeded.
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    
    def add_artist(self, name: str, alternative_names: tuple[str]=tuple()) -> bool:
        if len(self.get_artist(name)) != 0:
            return False
        data: list = self.read()
        data.append(
            {
                "name": name,
                "alternative_names": alternative_names
            }
        )
        self.write(data)
        return True
    
    def change_artist(self, name: str, **kwargs) -> bool:
        artists: list = self.get_artist(name)
        if len(artists) != 1:
            return False
        artist: dict = artists[0]
        for key, val in kwargs.items():
            artist[key] = val
        self.overwrite_artist(name, artist)
        return True
    
    def change_artist_name(self, name: str, new_name: str) -> bool:
        matches: list = self.get_artist(new_name)
        if len(matches) > 0:
            return False
        matches: list = self.get_artist(name)
        if len(matches) != 1:
            return False
        artist: dict = matches[0]
        artist["name"] = new_name
        self.overwrite_artist(name, artist)
        return True

    def overwrite_artist(self, name: str, artist: dict) -> bool:
        data: list = self.read()
        for index, element in enumerate(data):
            if element["name"] == name:
                data.pop(index)
                data.append(artist)
                self.write(data)
                break
        else:
            return False
        return True

    def get_artist(self, search_name: str) -> list:
        return [ element for element in self.read() if element["name"] == search_name ]
    
    def truncate(self) -> bool:
        if self.write([]):
            return True
        return False
    
    def delete(self) -> bool:
        try:
            os.remove(self.path)
        except:
            return False
        return True




if __name__ == "__main__":
    # example code for testing
    # delete later
    datastorage: Datastorage = Datastorage()
    datastorage.add_artist("Artist Name 1", ("Alternative", "names", "of", "artist"))
    datastorage.add_artist("Artist Name 2", ("Some", "other", "alternative", "names"))
    if not datastorage.change_artist("Artist Name 1", alternative_names=["New", "alternative", "names"]):
        print("Did not change ist.")
    if not datastorage.change_artist_name("Artist Name 1", "Artist Name 2"):
        input("Could not change the name. Press ENTER to continue")
    datastorage.truncate()
    datastorage.delete()
