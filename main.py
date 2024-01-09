from gebot import ImageDownloader
import pandas as pd
from statusIndicator import GEBotInfoDisplay
import tkinter as tk
import os

if __name__=='__main__':

    # downloader = ImageDownloader()
    data = pd.read_csv('./resources/grid_points_csv.csv')

    start = 0
    latitude = data['Lat'][start:20]
    longitude = data['Long'][start:20]
    img_id = data['id'][start:20]

    downloader = ImageDownloader()
    downloader.download_images(latitude, longitude, img_id=img_id, sleep_time=100, sleep_after=200)



    # root = tk.Tk()
    # gebot_display = GEBotInfoDisplay(root)

    
    # # Update information using the update_info method
    # status_dic = {"status":"Running", 
    #               "speed": "15 MB/s", 
    #               "expected_finish_time":"2 hours", 
    #               "remaining_images":"50%", 
    #               "images_downloaded":"100"}
    # gebot_display.update_info(status_dic=status_dic)

    # # root.mainloop()
    # import time

    # images_downloaded = 100
    # for i in range (1,10):
    #     images_downloaded = images_downloaded+1
        
    #     # Update information using the update_info method
    #     status_dic = {"status":"Running", 
    #                 "speed": "15 MB/s", 
    #                 "expected_finish_time":"2 hours", 
    #                 "remaining_images":"50%", 
    #                 "images_downloaded":images_downloaded}
    #     gebot_display.update_info(status_dic=status_dic)
    #     root.update() 
    #     time.sleep(2)
    # root.mainloop()

