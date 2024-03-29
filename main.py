# from gebot import ImageDownloader
import pandas as pd
import datetime
import json
import time

def main(path, start=0,stop=None, config_path='./resources/config.json'):
    with open(config_path) as file:
        config = json.load(file)
    emailIDs = config['emailID']
    machineID = config['machineID']


    data = pd.read_csv(path)
    start = 0 if start==0 else start-1

    latitude = data['Lat'][start:stop]
    longitude = data['Long'][start:stop]
    img_id = data['id'][start:stop]


    print(f"{datetime.datetime.now().replace(microsecond=0)} Google Earth Bot initialized")
    print(f"{datetime.datetime.now().replace(microsecond=0)} Bot id: {machineID}, and the notification email: {emailIDs}")
    time.sleep(1)
    print(f"{datetime.datetime.now().replace(microsecond=0)} Input data processed. Number of files in the batch is {len(img_id)}")
    
    
    downloader = ImageDownloader()
    print(f"{datetime.datetime.now().replace(microsecond=0)} Download initilized")
    downloader.download_images(latitude, longitude, img_id=img_id, sleep_time=100, sleep_after=200)

if __name__=='__main__':
    ge_pts_path = './resources/grid_points_csv.csv'

    main(ge_pts_path, start=0, stop=None)

    

