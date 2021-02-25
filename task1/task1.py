

'''
A class to handle geotiffs
'''

#######################################################
# import necessary packages
from lvisClass import lvisData
from processLVIS import lvisGround
from pyproj import Proj, transform # package for reprojecting data
from osgeo import gdal             # pacage for handling geotiff data
from osgeo import osr              # pacage for handling projection information
from gdal import Warp
import numpy as np
import argparse
import h5py

##########################################

def getCmdArgs():
  # function description for use within python
  '''
  Get commandline arguments
  '''
  # create an argparse object with a useful help comment
  p = argparse.ArgumentParser(description=("An illustration of a command line parser"))
  # read a string
  p.add_argument("--input",dest="inName",type=str,default='/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_049700.h5',help=("Input filename"))
  p.add_argument("--outRoot",dest="outRoot",type=str,default='chm.tif',help=("Output filename root"))
  # run the parsers and load results into an object
  cmdargs = p.parse_args()
  # return that object from this function
  return cmdargs

#######################################################

class tiffHandle(lvisGround):
  '''
  Class to handle geotiff files
  '''

  ########################################
  def writeTiffs(self,filename="chm.tif",step=1):
    for i in range(0,self.zG,step):
      self.writeTiff(o,filename=filename)

  def writeTiff(self,res=30,filename="chm.tif",epsg=27700):
    '''
    Write a geotiff from a raster layer
    '''

    # determine bounds

    minX=np.min(self.x)
    maxX=np.max(self.x)
    minY=np.min(self.y)
    maxY=np.max(self.y)

    # determine image size
    nX=int((maxX-minX)//res+1)
    nY=int((maxY-minY)//res+1)

    # pack in to array
    imageArr=np.full((nY,nX),-999.0)        # make an array of missing data flags

    # use integer division to determine which pixel each belongs to
    xInds=np.array((self.x-minX)//res,dtype=int)
    yInds=np.array((maxY-self.y)//res,dtype=int) # remember that y in a geotiff counts from the top

    # this is a simple pack which will assign a single footprint to each pixel
    imageArr[yInds,xInds]=lvis.zG
    # set geolocation information (note geotiffs count down from top edge in Y)
    geotransform = (minX, res, 0, maxY, 0, -1*res)

    # load data in to geotiff object
    dst_ds = gdal.GetDriverByName('GTiff').Create(filename, nX, nY, 1, gdal.GDT_Float32)

    dst_ds.SetGeoTransform(geotransform)    # specify coords
    srs = osr.SpatialReference()            # establish encoding
    srs.ImportFromEPSG(epsg)                # WGS84 lat/long
    dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(imageArr)  # write image to the raster
    dst_ds.GetRasterBand(1).SetNoDataValue(-999)  # set no data value
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None

    print("Image written to",filename)
    return



  ########################################

  # def readTiff(self,filename,epsg=27700):
  #   '''
  #   Read a geotiff in to RAM
  #   '''
  #
  #   # open a dataset object
  #   ds=gdal.Open(filename)
  #   # could use gdal.Warp to reproject if wanted?
  #
  #   # read data from geotiff object
  #   self.nX=ds.RasterXSize             # number of pixels in x direction
  #   self.nY=ds.RasterYSize             # number of pixels in y direction
  #   # geolocation tiepoint
  #   transform_ds = ds.GetGeoTransform()# extract geolocation information
  #   self.xOrigin=transform_ds[0]       # coordinate of x corner
  #   self.yOrigin=transform_ds[3]       # coordinate of y corner
  #   self.pixelWidth=transform_ds[1]    # resolution in x direction
  #   self.pixelHeight=transform_ds[5]   # resolution in y direction
  #   # read data. Returns as a 2D numpy array
  #   self.data=ds.GetRasterBand(1).ReadAsArray(0,0,self.nX,self.nY)



#######################################################
if __name__=="__main__":
  '''Main block'''

  # read the command line
  cmd=getCmdArgs()
  filename=cmd.inName
  outRoot=cmd.outRoot

  # create instance of class with "onlyBounds" flag
  b= tiffHandle(filename,onlyBounds=True)
  # set a steo size (note that this will be in degrees)
  step=(b.bounds[2]-b.bounds[0])/6

  # loop over spatial subsets
  for x0 in np.arange(b.bounds[0],b.bounds[2],step):  # loop over x tiles
    x1=x0+step   # the right side of the tile
    for y0 in np.arange(b.bounds[1],b.bounds[3],step):
       # loop over y tiles
      y1=y0+step  # the top of the tile

      # print the bounds to screen as a sanity check
      print("Tile between",x0,y0,"to",x1,y1)

      # read in all data within our spatial subset
      lvis=tiffHandle(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)

      # check to see whether any data is contained
      if(lvis.nWaves==0): # if there is none, skip this tile
        continue

      # set elevation, though this is not used here, but would be if you
      lvis.setElevations()    # were making a DTM
      lvis.estimateGround()
      lvis.findStats()
      lvis.setThreshold(threshScale=5)
      lvis.CofG()
      lvis.reproject(3031)
      lvis.writeTiff(filename="chm"+".x."+str(x0)+".y."+str(y0)+".tif")

      #lvis.writeTiff()
