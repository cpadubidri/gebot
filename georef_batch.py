from georef import main
import os
from tqdm import tqdm

def batchGeoref(folder_path, savepath=None):
    savefolder = savepath
    start = None
    stop = 5

    acq_list = os.listdir(folder_path)
    count = len(acq_list)
    for acq in acq_list[:1]:
        print(f"Processing Acqisition {acq} and remaining is {count}")
        imagePath = os.path.join(folder_path,acq)
        main(imagePath=imagePath, vrt=True, saveFolder=os.path.join(savefolder, acq+'_GEOTAGGED'), start=start, stop=stop)
        count-=1

if __name__=="__main__":
    folder_path = '/home/savvas/SUPER-NAS/USERS/Chirag/PERIOPSIS/202405-Greece/Data/Trikala/trikala'

    if folder_path==None:
        folder_path = input("Enter the folder path: ")
    batchGeoref(folder_path, savepath=folder_path)

