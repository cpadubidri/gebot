import pyautogui 
import time 
from os.path import exists, join, splitext, getsize
from os import mkdir 
import datetime  
import pandas as pd  
import json 
import tkinter as tk
from statusIndicator import GEBotInfoDisplay
from notificationHandler import SendEmail 
from tqdm import tqdm

class ImageDownloader:
    ___version__='1.1'
    """
    **IMAGE DOWNLOADER**

    ImageDownloader is a class designed for downloading Google Earth images based on coordinates (Longitude, Latitude) retrieved from a CSV database. The images are centered around the specified coordinates.

    To set up the bot, ensure that the 'getLoc.py' script has been executed, and the 'config.json' file is located in the './resources' folder. The 'config_path' parameter in the constructor allows customization of the configuration file path.

    In the current version, the bot is equipped with download logic, a notification handler (to send the status to the registered email on failure), and a status window (to display the bot's status).

    Parameters
    ----------

    config_path : str, optional
        The file path to the configuration file (default is './resources/config.json').

    Examples
    --------
    Initialize the ImageDownloader with a custom configuration file path:
    
    >>> downloader = ImageDownloader(config_path='./custom_config/config.json')

    Methods
    -------
    __init__()
        Initialize ImageDownloader class.

        The configuration file contains all the required parameters to run this class.

        Parameters
        ----------
        config_path : str, optional
            Path to the configuration file (default: './resources/config.json').
        
        Returns
        -------

    download_image(coord, filename, hover_time=4, step_sleep=2)
        Download an image from input coordinates and save it with the given filename. This method gives more control to the user; the user can download a single image and save it with a user-defined filename.

        Parameters
        ----------
        coord : str
            Centre coordinates of the image.
        filename : str
            Name of the file to be saved.
        hover_time : int, optional
            Time to sleep when GE pro is hovering (default: 4).
        step_sleep : int, optional
            Time to sleep (default: 2).
        
        Returns
        -------

    download_images(latitude, longitude, img_id, sleep_time=0, sleep_after=25)
        Download multiple images from coordinates. This method takes a list of parameters and downloads them; the user has less control over the filename but it is faster.

        Parameters
        ----------
        latitude : list
            List of latitudes.
        longitude : list
            List of longitudes.
        img_id : list
            List of image IDs.
        sleep_time : int, optional
            Time to sleep (default: 0).
        sleep_after : int, optional
            Sleep after a certain number of downloads to avoid banning. (default: 25).
        
        Returns
        -------
        
    __check_download_complete__(filename)
        Check if the download is complete for a specific file on the given save path. This is an internal method to check the status of the download.
        Once the download is completed, it sends a trigger flag to the bot to continue downloading. Additionally, if the bot gets into a 'stalled' state and stops downloading, it sends an email to the registered user.

        Parameters
        ----------
        filename : str
            Name of the file to check.
        
        Returns
        -------
    
    __update_status__()
        Internal method. This method is used to update the status on the notification window of the bot after each image download.
        
        Parameters
        ----------
        Returns
        -------

    __get_status__()
        Internal method for updating the status. This method calculates various variables to be displayed on the status window.

        Parameters
        ----------

        Returns
        -------
        dict
            A dictionary containing status-related information.

            - 'status' (str): The current status of the operation.
            - 'speed' (str): The processing speed, represented as seconds per image.
            - 'expected_finish_time' (str): The estimated time for completion in days, hours, and minutes.
            - 'remaining_images' (str): The number of remaining images to process.
            - 'time_elapsed' (str): The time elapsed in days, hours, and minutes since the start of the operation.

        Note
        ----
        The 'speed' is calculated as the time taken per image, and 'expected_finish_time' and 'time_elapsed' are formatted in days, hours, and minutes.

    __sec2dhm__(duration_seconds)
        This is an internal helper method to calculate days, hours, and minutes from the input seconds.

        Parameters
        ----------
        duration_seconds : int
            Time in seconds.

        Returns
        -------
        list
            A list with days, hours, and minutes for input seconds.
            - (days, hours, minutes) (list): Time in Days, Hours, and Minutes

    """

    def __init__(self, config_path='./resources/config.json'):
        """
        Initialize ImageDownloader class.

        The configuration file contains all the required parameters to run this class.

        Parameters
        ----------
        config_path : str, optional
            Path to the configuration file (default: './resources/config.json').
        """
        with open(config_path) as file:
            self.config = json.load(file)
        
        self.save_path = self.config['savePath']
        self.LOCATION_REPORT = self.config['locationReport']
        self.status = "STOPPED"
        self.img_len = 0
        self.bot_start_time = 0
        self.counter = 0
        self.trigger_time = 600  # trigger time to send the stop email in second.

        # Initialize status window
        self.root = tk.Tk()
        self.gebot_display = GEBotInfoDisplay(self.root)
        status_dic = {"status": "Running", 
                      "speed": "15 MB/s", 
                      "expected_finish_time": "2 hours", 
                      "remaining_images": "50%", 
                      "time_elapsed": "100"}
        self.gebot_display.update_info(status_dic=status_dic)

        # Initialize communication channel
        self.se = SendEmail()


    def download_image(self, coord, filename, hover_time=4, step_sleep=2):
        """
        Download an image from input coordinates and save it with the given filename. This method gives more control to the user; the user can download a single image and save it with a user-defined filename.

        Parameters
        ----------
        coord : str
            Centre coordinates of the image.
        filename : str
            Name of the file to be saved.
        hover_time : int, optional
            Time to sleep when GE pro is hovering (default: 4).
        step_sleep : int, optional
            Time to sleep (default: 2).
        """
        # Searching bar lat, long entering
        pyautogui.click(self.LOCATION_REPORT['search_loc'])
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(step_sleep)
        pyautogui.typewrite(coord)
        pyautogui.typewrite(['enter'])

        # Wait for Google Earth to hover to the location
        print("{} Hovering to {}".format(datetime.datetime.now().replace(microsecond=0), coord))
        time.sleep(hover_time)

        # Uncheck coordinate icon
        pyautogui.click(self.LOCATION_REPORT['uncheck'])
        time.sleep(step_sleep)

        # Click on Save Images
        pyautogui.click(self.LOCATION_REPORT['save_image_loc'])
        time.sleep(step_sleep)
        pyautogui.typewrite(filename)
        time.sleep(step_sleep)

        # Click on save button
        pyautogui.click(self.LOCATION_REPORT['save_button_loc'])
        print("{} Saving file: {}".format(datetime.datetime.now().replace(microsecond=0), filename))


    def download_images(self, latitude, longitude, img_id, sleep_time=0, sleep_after=25):
        """
        Download multiple images from coordinates. This method takes a list of parameters and downloads them; the user has less control over the filename but it is faster.

        Parameters
        ----------
        latitude : list
            List of latitudes.
        longitude : list
            List of longitudes.
        img_id : list
            List of image IDs.
        sleep_time : int, optional
            Time to sleep (default: 0).
        sleep_after : int, optional
            Sleep after a certain number of downloads to avoid banning. (default: 25).
        """
        self.status = "Downloading"
        self.img_len = len(img_id)
        self.bot_start_time = time.time()
        
        for lat, long, id in zip(latitude, longitude, img_id):
            filename = "IMG" + str(id).zfill(4) + "_LT" + str(lat) + "_LG" + str(long) + '.png'

            # Download image from coordinates
            self.download_image(coord=str(lat) + "," + str(long), filename=filename)
            # time.sleep(8)

            # Check download completed
            self.__check_download_complete__(filename)
            self.img_len = self.img_len-1

            time.sleep(2)
            self.counter += 1
            self.__update_status__()

            if self.counter % sleep_after == 0:
                print("{} Sleeping".format(datetime.datetime.now().replace(microsecond=0)))
                time.sleep(sleep_time)

    def __check_download_complete__(self, filename):
        """
        Check if the download is complete for a specific file on the given save path. This is an internal method to check the status of the download.
        Once the download is completed, it sends a trigger flag to the bot to continue downloading. Additionally, if the bot gets into a 'stalled' state and stops downloading, it sends an email to the registered user.

        Parameters
        ----------
        filename : str
            Name of the file to check.
        """
        d_complete = False
        size_cr = size_pr = 0
        elapsed_time = time.time()
        emailstatus = False
        while not d_complete:
            if exists(join(self.save_path, filename)):
                size_cr = getsize(join(self.save_path, filename))
                if size_cr == size_pr:  # If saving completes
                    d_complete = True
                size_pr = size_cr
            time.sleep(1)
            if time.time() - elapsed_time > self.trigger_time:
                if not emailstatus:
                    self.se.process_stopped()
                    emailstatus = True
                self.status = "Stopped"
                self.__update_status__()

        print("{} Saved file: {}".format(datetime.datetime.now().replace(microsecond=0), filename))
    
    def __update_status__(self):
        """
        Internal method. This method is used to update the status on the notification window of the bot after each image download.
        """
        status_dic = self.__get_status__()
        self.gebot_display.update_info(status_dic=status_dic)
        self.root.update() 
    
    def __get_status__(self): 
        """
        Internal method for updating the status. This method calculates various variables to be displayed on the status window.

        Returns
        -------
        dict
            A dictionary containing status-related information.

            - 'status' (str): The current status of the operation.
            - 'speed' (str): The processing speed, represented as seconds per image.
            - 'expected_finish_time' (str): The estimated time for completion in days, hours, and minutes.
            - 'remaining_images' (str): The number of remaining images to process.
            - 'time_elapsed' (str): The time elapsed in days, hours, and minutes since the start of the operation.

        Note
        ----
        The 'speed' is calculated as the time taken per image, and 'expected_finish_time' and 'time_elapsed' are formatted in days, hours, and minutes.
        """     
        elp_time  = time.time()-self.bot_start_time
        rm_img = self.img_len-1
        speed = ((elp_time)/self.counter)
        eft = self.__sec2dhm__(speed * rm_img)
        te = self.__sec2dhm__(elp_time)

        return {"status": self.status, 
                "speed": str(round(speed, 2))+' sec per image', 
                "expected_finish_time": f'{eft[0]} days, {eft[1]} hours, {eft[2]} min', 
                "remaining_images": str(rm_img), 
                "time_elapsed": f'{te[0]} days, {te[1]} hours, {te[2]} min'}

    def get_dates(self,csv_path,savepath='./acqimg'):
        import pyscreenshot as ImageGrab
        data = pd.read_csv(csv_path)
        latitude = data['Lat'][2990:]
        longitude = data['Long'][2990:]
        
        
        if not(exists(savepath)):
            mkdir(savepath)

        input("Move the mouse-pointer to search bar and press 'Enter'")
        search_loc = pyautogui.position()
        input("Move the mouse-pointer to timeline pointer and press 'Enter'")
        time_loc = pyautogui.position()

        # print(search_loc)
        # print(time_loc)

        # search_loc = (1186,128)
        # time_loc = (1627,153)
        for lat,lon in tqdm(zip(latitude, longitude), total=len(latitude)):
            # print(lat, lon)
            pyautogui.click(search_loc)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(.2)
            pyautogui.typewrite(str(lat) + "," + str(lon))
            pyautogui.typewrite(['enter'])
            time.sleep(1)
            pyautogui.click(time_loc)
            # time.sleep(.2)
            pyautogui.drag(30, 0, .5, button='left')

            im=ImageGrab.grab(bbox=(time_loc[0]-50,time_loc[1]-20,time_loc[0]+10,time_loc[1]))
            im.save(join(savepath,str(lat)+'_'+str(lon)+'.jpg'))


            # break





    @staticmethod
    def __sec2dhm__(duration_seconds):
        """
        This is an internal helper method to calculate days, hours, and minutes from the input seconds.

        Parameters
        ----------
        duration_seconds : int
            Time in seconds.

        Returns
        -------
        list
            A list with days, hours, and minutes for input seconds.
            - (days, hours, minutes) (list): Time in Days, Hours, and Minutes
        """
        days = duration_seconds // (24 * 3600)
        hours = (duration_seconds % (24 * 3600)) // 3600
        minutes = (duration_seconds % 3600) // 60
        return days, hours, minutes
    
    
    def __version__(self):
        return self._version_
    

if __name__ == '__main__':
    data = pd.read_csv('./resources/grid_points_csv.csv')

    start = 632
    latitude = data['Lat'][start:]
    longitude = data['Long'][start:]
    img_id = data['id'][start:]

    downloader = ImageDownloader()
    # downloader.download_images(latitude, longitude, img_id=img_id, sleep_time=100, sleep_after=200)
    downloader.get_dates('./resources/grid_points_csv.csv')