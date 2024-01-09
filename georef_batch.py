from georef import main
import os
from tqdm import tqdm

if __name__=="__main__":
    folder_path = input("Enter the folder path")
    savefolder = None
    start = stop = None
    count = 0

    acq_list = os.listdir(folder_path)
    for acq in acq_list:
        print(f"Processing Acqisition {acq} and remaining is {count}")
        imagePath = os.path.join(folder_path,acq)
        print(imagePath)
        main(imagePath=imagePath, saveFolder=savefolder, start=start, stop=stop)
        count+=1
