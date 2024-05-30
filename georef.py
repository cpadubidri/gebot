import math
import numpy as np
import cv2
import rasterio
import os
import argparse
from tqdm import tqdm
from osgeo import gdal


class Geotagger:
    __version__='1.1'
    """
    **Geotagger**

    A class for geotagging images and saving them in TIFF format with spatial information. This should be used only to the images downloaded via GEBOT.

    Note
    ---- 
    Geotagger class should be run using main function. It can take PNG/JPG files and georeference them to TIFF format.

    Parameters
    ----------

    inputpath : str/path
        Path to the image folder.
    outputpath : str/path
        Path of the folder where the georeferenced images should be saved. If set to 'None', a new folder will be created in the imagePath with '_GEOTAGGED' appended to the path.
    start : int
        The starting number for the filenames of the images in the folder for georeferencing. If set to 'None', the function will start from the beginning (start=0).
    stop : int
        The ending number for the filenames of the images in the folder for georeferencing. If set to 'None', the function will perform the action for all the items in the folder.

    
    The 'start' and 'stop' parameters are helpful if we want to terminate the process in the middle and restart it later.

    Examples
    --------
    >>> python georef.py --inputpath path/to/image_folder --outputpath path/to/save_folder --start 10 --stop 20

    Methods
    -------
    __init__()
        Initializes the Geotagger object.

        Parameters
        ----------
        filepath : str
            The path to the image file.
        center_coord : tuple 
            Tuple containing latitude and longitude values of the image center.
        savepath : str
            The path to the folder where geotagged images will be saved.
        pixXRES : float 
            Pixel resolution in the X direction.
        pixYRES : float
            Pixel resolution in the Y direction.

        Returns
        -------
        None

    lat_long() 
        This is a local method to calculates new latitude and longitude with the given offsets.

        Parameters
        ----------
        lat : float
            Latitude.
        lon : float
            Longitude.
        dn : float
            Offset in the north direction.
        de : float
            Offset in the east direction.

        Returns
        -------
        tuple
            Tuple containing new latitude, longitude, and altitude (0).
        
    output_corners()
        Computes the corners of the geotagged image based on center coordinates and pixel resolutions.

        Parameters
        ----------
        lat : float 
            Latitude of the image center.
        lon : float 
            Longitude of the image center.
        width : int 
            Width of the image in pixels.
        height : int 
            Height of the image in pixels.
        offset1 : float 
            Offset in the north direction.
        offset2 : float 
            Offset in the east direction.

        Returns
        -------
        numpy.ndarray
            Array containing the coordinates of the image corners.
        
    name2latlong() 
        Extracts latitude and longitude from the image filename.

        Parameters
        ----------
        filename : str 
            The name of the image file.

        Returns
        -------
        tuple
            Tuple containing latitude and longitude.
    
    getcoord()
        Computes the geotagged image's bounding box and corner coordinates.
        
        Parameters
        ----------
        None

        Returns
        -------
        tuple
            Tuple containing the bounding box coordinates (north, south, west, east) and the image.   
    
    geotag()
        Geotags the image and saves it in TIFF format.
        
        Parameters
        ----------

        Returns
        -------

    """

    def __init__(self, filepath, center_coord, savepath, pixXRES, pixYRES):
        """
        Initializes the Geotagger object.

        Parameters
        ----------
        filepath : str
            The path to the image file.
        center_coord : tuple 
            Tuple containing latitude and longitude values of the image center.
        savepath : str
            The path to the folder where geotagged images will be saved.
        pixXRES : float 
            Pixel resolution in the X direction.
        pixYRES : float
            Pixel resolution in the Y direction.
        Returns
        -------
        """
        self.filepath = filepath
        self.center_coord = center_coord
        self.savepath = savepath
        self.pixXRES = pixXRES
        self.pixYRES = pixYRES

    @staticmethod
    def lat_long(lat, lon, dn, de):
        """
        This is a local method to calculates new latitude and longitude with the given offsets.

        Parameters
        ----------
        lat : float
            Latitude.
        lon : float
            Longitude.
        dn : float
            Offset in the north direction.
        de : float
            Offset in the east direction.

        Returns
        -------
        coordinates : tuple
            Tuple containing new latitude, longitude, and altitude (0).
        """
        # Earth’s radius, sphere
        R = 6378137

        # Coordinate offsets in radians
        dLat = dn / R
        dLon = de / (R * math.cos(math.pi * lat / 180))

        # OffsetPosition, decimal degrees
        lat1 = lat + dLat * 180 / math.pi
        lon1 = lon + dLon * 180 / math.pi
        return lat1, lon1, 0

    @staticmethod
    def output_corners(lat, lon, width, height, offset1, offset2):
        """
        output_corners()
        Computes the corners of the geotagged image based on center coordinates and pixel resolutions.

        Parameters
        ----------
        lat : float 
            Latitude of the image center.
        lon : float 
            Longitude of the image center.
        width : int 
            Width of the image in pixels.
        height : int 
            Height of the image in pixels.
        offset1 : float 
            Offset in the north direction.
        offset2 : float 
            Offset in the east direction.

        Returns
        -------
        coordinates : numpy.ndarray
            Array containing the coordinates of the image corners.
        """
        top_left = Geotagger.lat_long(lat, lon, offset1, -offset2)  # top left corner
        top_right = Geotagger.lat_long(lat, lon, offset1, offset2)  # top right corner
        bottom_right = Geotagger.lat_long(lat, lon, -offset1, offset2)  # bottom right corner
        bottom_left = Geotagger.lat_long(lat, lon, -offset1, -offset2)  # bottom left corner

        # Adjust the latitude of the corners based on the image aspect ratio
        lat_diff = (top_right[0] - top_left[0]) * (height / width)
        bottom_left = (bottom_left[0] - lat_diff, bottom_left[1], bottom_left[2])
        bottom_right = (bottom_right[0] - lat_diff, bottom_right[1], bottom_right[2])

        return np.array([top_left, top_right, bottom_right, bottom_left])

    @staticmethod
    def name2latlong(filename):
        """
        Extracts latitude and longitude from the image filename.

        Parameters
        ----------
        filename : str 
            The name of the image file.

        Returns
        -------
        coordinates : tuple
            Tuple containing latitude and longitude.
        """
        return float(os.path.splitext(filename)[0].split("_")[1][2:]), float(os.path.splitext(filename)[0].split("_")[2][2:])

    def getcoord(self):
        """
        Computes the geotagged image's bounding box and corner coordinates.

        Returns
        -------
        coordinates : tuple
            Tuple containing the bounding box coordinates (north, south, west, east) and the image.
        """
        img = cv2.cvtColor(cv2.imread(self.filepath), cv2.COLOR_RGB2BGR)

        coords = Geotagger.output_corners(
            self.center_coord[0], self.center_coord[1], img.shape[0], img.shape[1],
            img.shape[0] * self.pixYRES / 2, img.shape[1] * self.pixXRES / 2
        )

        n = np.max(coords[:, 0])
        s = np.min(coords[:, 0])
        w = np.min(coords[:, 1])
        e = np.max(coords[:, 1])

        return n, s, w, e, img

    # def get_geotag(self):
    #     """
    #     Returns the bounding box coordinates of the geotagged image.

    #     Returns:
    #         tuple: Tuple containing the bounding box coordinates (north, south, west, east).
    #     """
    #     return self.getcoord()

    def geotag(self):
        """
        Geotags the image and saves it in TIFF format.
        """
        n, s, w, e, img = self.getcoord()

        with rasterio.Env():
            tsfm = rasterio.transform.from_bounds(w, s, e, n, img.shape[1], img.shape[0])
            img = np.moveaxis(img, -1, 0)

            savepath = os.path.join(self.savepath, os.path.splitext(os.path.split(self.filepath)[1])[0] + ".tif")

            with rasterio.open(savepath, 'w', dtype=rasterio.uint8,
                               transform=tsfm,
                               crs=rasterio.crs.CRS.from_epsg(4326),
                               driver='GTiff',
                               width=img.shape[2],
                               height=img.shape[1],
                               count=img.shape[0]) as dst:
                dst.write(img.astype(rasterio.uint8))
    
    def genVRT(self,input_path, output_path):
        print(f'Generating VRT file {output_path}')
        tif_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.tif')]
        gdal.BuildVRT(output_path, tif_files)

    

    def __getattr__(self, attrib):
        if attrib=="__version__":
            return self.__version__
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attrib}'")

def main(imagePath, vrt=False, saveFolder=None, start=None, stop=None):
    """
    
    """
    if saveFolder is None:
        saveFolder = os.path.basename(imagePath) + '_GEOTAGGED'

    parent_folder_path = os.path.abspath(os.path.join(imagePath, os.pardir))
    save_path = os.path.join(parent_folder_path, saveFolder)

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    image_list = os.listdir(os.path.join(imagePath))
    image_list.sort()

    if start is None:
        start = 0
    if stop is None:
        stop = len(image_list)

    length = len(image_list[start:stop])
    
    for image in tqdm(image_list[start:stop]):
        # print("Image: {}, remaining image: {}".format(image, length))
        geotagger = Geotagger(
            filepath=os.path.join(imagePath, image),
            center_coord=Geotagger.name2latlong(image),
            savepath=os.path.join(save_path),
            pixYRES=0.17475,  # parameter controlling height
            pixXRES=0.17475  # parameter controlling width
        )
        geotagger.geotag()
        length -= 1
    
    #generate virtual meged vrt file
    if vrt:
        folder_split = save_path.split('/')
        id1 = folder_split[-2]
        id2 = folder_split[-1].split('_')[0]
        geotagger.genVRT(input_path=save_path, output_path=os.path.abspath(os.path.join(save_path, os.pardir,f'{id1}_{id2}_output.vrt')))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process command line arguments")
    parser.add_argument("--start","-s", type=int, help="Start value")
    parser.add_argument("--end","-e", type=int, help="Stop value")
    parser.add_argument("--outputpath","-o", help="Save folder path")
    parser.add_argument("--inputpath","-i", help="Image path", required=True)
    parser.add_argument("--vrt","-v", help="Merges files if True", default=False)
    
    args = parser.parse_args() 

    # Check if start, stop, and savefolder are None, set them to default values
    start = args.start if args.start is not None else None
    stop = args.end if args.end is not None else None
    savefolder = args.outputpath if args.outputpath is not None else None   

    
    """
        This function is used to georeference images. It can take PNG/JPG files and georeference them to TIFF format.

        Parameters:

            inputpath (str/path)    : Path to the image folder.
            outputpath (str/path)   : Path of the folder where the georeferenced images should be saved. 
                                      If set to 'None', a new folder will be created in the imagePath with '_GEOTAGGED' appended to the path.
            vrt (bool)              : Flag to generate virtual merged file.
                                      if True, a virual merged, vrt file will be generated in root directory. 
            start (int)             : The starting number for the filenames of the images in the folder for georeferencing. 
                                      If set to 'None', the function will start from the beginning (start=0).
            stop (int)              : The ending number for the filenames of the images in the folder for georeferencing. 
                                      If set to 'None', the function will perform the action for all the items in the folder.

        The 'start' and 'stop' parameters are helpful if we want to terminate the process in the middle and restart it later.

        Examples:
            python georef.py --inputpath path/to/image_folder 
                             --outputpath path/to/save_folder 
                             --start 10 
                             --stop 20
    """
    
    main(imagePath=args.inputpath, vrt=args.vrt, saveFolder=savefolder, start=start, stop=stop)


    


# python georef.py -i /home/savvas/SUPER-NAS/USERS/Chirag/PERIOPSIS/202405-Greece/Data/Larissa/larissa/sample -v True

