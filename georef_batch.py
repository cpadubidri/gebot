from georef import main
import os
from tqdm import tqdm
from guiHandler import getFolder

def batchGeoref():
    try:
        folder_path = getFolder()
        if not folder_path:
            raise Exception("No folder selected")
    except Exception as e:
        print(f"GUI failed or no folder selected ({e}). Please enter the folder path manually:")
        folder_path = input("Enter the folder path: ")

    savefolder = None
    start = stop = None

    acq_list = os.listdir(folder_path)
    count = len(acq_list)
    for acq in acq_list:
        print(f"Processing Acqisition {acq} and remaining is {count}")
        imagePath = os.path.join(folder_path,acq)
        main(imagePath=imagePath, vrt=True, saveFolder=savefolder, start=start, stop=stop)
        count-=1

if __name__=="__main__":
    batchGeoref()


#/home/savvas/SUPER-NAS/USERS/Chirag/PERIOPSIS/202405-Greece/Data/Larissa/larissa