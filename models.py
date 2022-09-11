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
        """
        Adds an artist to file.

        Args:
            name (str): The name of the artist
            alternative_names (tuple[str], optional): Sets the alternative names of the artist.

        Returns:
            bool: True if sucess else False
        """
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
        """
        Changes the additional information of an artist.

        Args:
            name (str): Name of the artist for recognition.

        Returns:
            bool: True on success else False
        """
        artists: list = self.get_artist(name)
        if len(artists) != 1:
            return False
        artist: dict = artists[0]
        for key, val in kwargs.items():
            artist[key] = val
        self.overwrite_artist(name, artist)
        return True
    
    def change_artist_name(self, name: str, new_name: str) -> bool:
        """
        Changes the artist name.

        Args:
            name (str): The current name of the artist.
            new_name (str): The future name of the artist.

        Returns:
            bool: True if success else False
        """
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
        """
        Overwrites the artist dictionary in the file.

        Args:
            name (str): Name of the artist for recognition.
            artist (dict): The artist as a dictionary.

        Returns:
            bool: True if success else False
        """
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
        """
        Gets all artist which name matches with the given name.

        Args:
            search_name (str): The name of the artist you want to search.

        Returns:
            list: All artist which name matches with the search_name.
        """
        return [ element for element in self.read() if element["name"] == search_name ]
    
    def truncate(self) -> bool:
        """
        Clears the file.

        Returns:
            bool: True on success else False.
        """
        if self.write([]):
            return True
        return False
    
    def delete(self) -> bool:
        """
        Deletes the file.

        Returns:
            bool: True on success else False.
        """
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
