from georef import main
import os
from tqdm import tqdm

def batchGeoref(folder_path, savepath=None):
    savefolder = savepath
    start = stop = None

    acq_list = os.listdir(folder_path)
    count = len(acq_list)
    for acq in acq_list:
        print(f"Processing Acqisition {acq} and remaining is {count}")
        imagePath = os.path.join(folder_path,acq)
        main(imagePath=imagePath, vrt=True, saveFolder=os.path.join(savefolder, acq+'_GEOTAGGED'), start=start, stop=stop)
        count-=1

if __name__=="__main__":
    folder_path = input("Enter the folder path: ")
    batchGeoref(folder_path, savepath='/home/savvas/StorageNVME2/Greece-Dumping/Trikala')


#/home/savvas/SUPER-NAS/USERS/Chirag/PERIOPSIS/202405-Greece/Data/Larissa/larissa