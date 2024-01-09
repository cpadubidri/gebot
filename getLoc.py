import json
from datetime import datetime
import pyautogui

class LocationGetter:
    __version__='1.1'
    """
    **Location Getter**

    This class is designed to facilitate the manual retrieval and storage of Google Earth Pro GUI button locations, and update the configuration data in 'config.json'.
    The script serves as a setup script that must be run before configuring GEBOT. It guides the user through the necessary steps to obtain the required configuration file.

    Parameters
    ----------
    None

    Attributes
    ----------
    location_report : dict
        A dictionary to store mouse locations for different elements.

    Methods
    -------
    __init__()
        Initializes the LocationGetter.

        Parameters
        ----------
        None

        Returns
        -------
        None

    get_location(message)
        Retrieves the mouse location after user input.

        Parameters
        ----------
        message : str
            The message to display to the user.

        Returns
        -------
        tuple
            x and y coordinates of the mouse position.

    collect_locations()
        Collects mouse locations for the search bar, uncheck, save image, and save button.

        Parameters
        ----------
        None

        Returns
        -------

    print_location_report()
        Saves the location report as a JSON file and prints the location report.

        Parameters
        ----------
        None

        Returns
        -------

    """

    def __init__(self):
        """
        Initializes the LocationGetter.

        Parameters
        ----------
        None
        """
        self.location_report = {"search_loc": 0, "uncheck": 0, "save_image_loc": 0, "save_button_loc": 0}

    def get_location(self, message):
        """
        Retrieves the mouse location after user input.

        Parameters
        ----------
        message : str
            The message to display to the user.

        Returns
        -------
        tuple
            x and y coordinates of the mouse position.
        """
        input("Move the mouse-pointer to {} and press 'Enter'".format(message))
        return pyautogui.position()

    def collect_locations(self):
        """
        Collects mouse locations for the search bar, uncheck, save image, and save button.

        Parameters
        ----------
        None
        """
        # Search bar location
        search_loc = self.get_location("Search bar")
        self.location_report['search_loc'] = (search_loc[0], search_loc[1])

        # Uncheck coordinates tab location
        uncheck = self.get_location("Uncheck coordinates tab")
        self.location_report['uncheck'] = (uncheck[0], uncheck[1])

        # Save image button
        save_image_loc = self.get_location("Save Image button")
        self.location_report['save_image_loc'] = (save_image_loc[0], save_image_loc[1])

        pyautogui.click(save_image_loc[0], save_image_loc[1])

        # Save button
        save_button_loc = self.get_location("Save button")
        self.location_report['save_button_loc'] = (save_button_loc[0], save_button_loc[1])

    def print_location_report(self):
        """
        Saves the location report as a JSON file and prints the location report.

        Parameters
        ----------
        None
        """
        print("{} Saving configuration file: './resources/config.json'".format(datetime.now().replace(microsecond=0)))
        with open('./resources/config.json', 'r') as file:
            data = json.load(file)

        data["locationReport"] = self.location_report
        data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open('./resources/config.json', 'w') as file:
            json.dump(data, file)
    

    def __getattr__(self, attrib):
        if attrib=="__version__":
            return self.__version__
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attrib}'")


if __name__ == '__main__':
    location_getter = LocationGetter()
    location_getter.collect_locations()
    location_getter.print_location_report()
    # with open('config.json','r')  as file:
    #     data = json.load(file)
    
    # print(data)
