# final-assignment
this is for final assignment
This contains all the files for task.  

Task1 includes lvisClass.py, processLVIS.py, task1.py. 

Task2 includes handleTiff.py, lvisClass.py, processLVIS.py,task2.py.

Task3 includes handleTiff.py, lvisClass.py, processLVIS.py,task3.py.


## Task1.py

A python scripts to handle geotiff files. This class inherits functions from lvisGround.  The data of this task is 2009 LVIS data from h5 files .

This file includes one method`writeTiff()`, command line function `getCmdArgs()` and main block `if __name__=="__main__"`:.

In the command line function:

Set input and output data file arguments to make the code reusable

`p.add_argument("input",dest="inName",type=str,default='/geos/netdata/oosa/assignment/lvis/2009/ILVIS1B_AQ2009_1020_R1408_049700.h5',help=("Input filename"))``
p.add_argument("--outRoot",dest="outRoot",type=str,default='chm.tif',help=("Output filename root"))`

The class in this file  is `tiffHandle()`.

This class includes one method`writeTiff()`

In this method,  the variables we used shows as follow:

`minX,maxX,minY,maxY : to determine the bounds`
`nX,nY: to determine image size`
`imageArr: to pack into array`
`geotransform: to set geolocation information`

To set the bounds:

 `np.min(self.x)`

To determine the image size:

 `int((maxX-minX)//res+1)`

To assign a single ground elevation to each pixel

`imageArr[yInds,xInds]`

To set geolocation information:

`geotransform = (minX, res, 0, maxY, 0, -1*res)`

Load data to geotiff object

   dst_ds = gdal.GetDriverByName('GTiff').Create(filename, nX, nY, 1, gdal.GDT_Float32)

    dst_ds.SetGeoTransform(geotransform)    # specify coords
    srs = osr.SpatialReference()            # establish encoding
    srs.ImportFromEPSG(epsg)                # WGS84 lat/long
    dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(imageArr)  # write image to the raster
    dst_ds.GetRasterBand(1).SetNoDataValue(-999)  # set no data value
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None

The function called in this task:

      lvis.setElevations()   
      lvis.estimateGround()
      lvis.findStats()
      lvis.setThreshold()
      lvis.CofG()
      lvis.reproject()
      lvis.writeTiff()

## Task2.py

A python scripts to handle geotiff files. This class inherits functions from lvisGround.  The data of this task is all the LVIS data in 2015 from h5 files .

This file includes one method`writeTiff()`, command line function `getCmdArgs()` and main block `if __name__=="__main__"`:.

In the `getCmdArgs()`  function, input a file list

`p.add_argument("--inDir",dest="inDir",type=str,default='/geos/netdata/oosa/assignment/lvis/2015',help=("Input filelist"))`

The class in this file  is `tiffHandle()`. The function remains the same as task1.py

This class includes one method`writeTiff()`

In the main block,

read the command line and list directory

`cmd=getCmdArgs()`

`fileList=glob(cmd.inDir+'/*.h5')`

loop over files 

`for f in fileList:`

create instance of class with "onlybounds" flag

`b= tiffHandle(f,onlyBounds=True)`

loop over spatial subsets (x tiles and y tiles)

`for x0 in np.arange(b.bounds[0],b.bounds[2],step):  
        x1=x0+step  
        for y0 in np.arange(b.bounds[1],b.bounds[3],step):`

`                     y1=y0+step`  







## Task3.py

A python scripts to handle geotiff files. This class inherits functions from lvisGround.  The data of this task is 2009 LVIS data from h5 files .

This file includes one method`writeTiff()`, command line function `getCmdArgs()` and main block `if __name__=="__main__"`:.

The class in this file  is `tiffHandle()`.

This class includes one method`writeTiff()`

