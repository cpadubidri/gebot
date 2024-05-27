from georef import main
import os
from tqdm import tqdm

if __name__=="__main__":
    folder_path = input("Enter the folder path : ")
    savefolder = None
    start = stop = None

    acq_list = os.listdir(folder_path)
    count = len(acq_list)
    for acq in acq_list:
        print(f"Processing Acqisition {acq} and remaining is {count}")
        imagePath = os.path.join(folder_path,acq)
        print(imagePath)
        main(imagePath=imagePath,vrt=True, saveFolder=savefolder, start=start, stop=stop)
        count-=1


#/home/savvas/SUPER-NAS/USERS/Chirag/PERIOPSIS/202405-Greece/Data/Larissa/larissa