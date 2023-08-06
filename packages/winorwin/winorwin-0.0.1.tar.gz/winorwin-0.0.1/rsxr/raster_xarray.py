import xarray as xr
import numpy as np
import pandas as pd
import geopandas as gpd
from helpers import check_xr_gdf

def stack_open (src_path, src_names, dim = 'bands'):
    """
    Opens and stack multiple datasets stored in raster format and returns them as an xarray.DataArray.
    
    Parameters:
    src_path (list): 
        A list of strings containing the paths to the raster datasets.
    src_names (list): 
        A list of strings representing the names of the bands.
    dim (str, optional): 
        The name of the dimension to stack the bands. Default value is 'bands'.
    
    Returns:
        xarray.DataArray: 
        The stacked bands is returned as an xarray.DataArray.
    
    Source: This function was adapted from xarray.concat
            https://docs.xarray.dev/en/stable/generated/xarray.concat.html
    """
    xr_list = []
    for i in src_path:
        xr_var = xr.open_dataset(i, engine="rasterio").squeeze()
        xr_var = xr_var.band_data
        xr_list.append(xr_var)
    
    bands_var = xr.concat(xr_list, "bands")
    
    bands_var.coords['bands'] = src_names

    return bands_var


def crop_bb (stack_xr, gdf, inverse: bool = False) :
    
    """crop_bb returns a geographic subset of an xarray with geo attributes from which an extent object (Bounding Box) can be extracted/created 

    Parameters
    ----------
    stack_xr : xarray.DataArray
        A Dataset with one or multiple bands
    gdf : GeoDataFrame 
        GeoDataFrame 
    inverse : bool, optional
        If True, the function will return an xarray with a mask applied to exclude values within the bounding box of the provided GeoDataFrame. 
        If False (default), the function will return an xarray cropped to the extent of the provided GeoDataFrame.

    Returns
    -------
    xarray.DataArray 
        xarray cropped to the extent of the provided GeoDataFrame 

    """
    if not isinstance(inverse, bool):
        raise TypeError("'inverse' must be a boolean value (True or False)")
    
    # Run helper function
    gdf = check_xr_gdf(stack_xr, gdf)
    
    # Get the bounding box of the area of interest
    bounds = gdf.bounds
    x_min, x_max = bounds.minx.values[0], bounds.maxx.values[0]
    y_max, y_min = bounds.maxy.values[0], bounds.miny.values[0]
    
    if inverse == False:
        # Select the data within the bounding box
        xr_cropped = stack_xr.sel(x=slice(x_min, x_max),
                                        y=slice(y_max, y_min))
    elif inverse == True:
        # Create a mask to exclude values within a certain y and x range
        mask = (stack_xr["y"] < y_min) | (stack_xr["y"] > y_max) | (stack_xr["x"] < x_min) | (stack_xr["x"] > x_max)

        # Apply the mask to the original DataArray using the 'where()' method
        xr_cropped = stack_xr.where(mask)
    
    return xr_cropped

def zonal_stats (stack_xr, gdf, statistic, dim = 'bands'):
    
    """Compute the zonal statistics of an xarray with geo attributes for each feature of an overlapping GeoDataFrame with a set of polygons 

    Parameters
    ----------
    stack_xr : xarray.DataArray
        A Dataset with one or multiple bands
    gdf : GeoDataFrame 
        GeoDataFrame with a polygons
    statistic : str 
        The statistic to compute ('mean', 'max', 'min', 'median', 'var', 'std', 'sum').

    Returns
    -------
    GeoDataFrame 
        GeoDataFrame with the computed statistics for each band overlapping GeoDataFrame wih polygons

    """
    # Run helper function
    gdf = check_xr_gdf(stack_xr, gdf)
    
    # Define a dictionary that maps statistic names to numpy functions
    stats_functions = {
        "mean": np.nanmean,
        "max": np.nanmax,
        "min": np.nanmin,
        "median": np.nanmedian,
        "var": np.nanvar,
        "std": np.nanstd,
        "sum": np.nansum,
        #"count": np.count_nonzero
    }
    # Look up the function in the dictionary
    stats_function = stats_functions.get(statistic)
    
    # If the statistic is not recognized, raise an error
    if stats_function is None:
        raise ValueError(f"{statistic} is not a valid statistic. Allowed statistics are {list(stats_functions.keys())}")

    # Get the bands names
    band_names = list(stack_xr[dim].values.ravel())

    vals_df = []

    # Iterate over the GeoDataFrame
    for row in (range(len(gdf))):
        gdf_row = gdf[row : row+1]
    
        # Clip the xarray within each polygon
        xr_croped = stack_xr.rio.clip(gdf_row["geometry"])

        # run the zonal stats on each band 
        vals_list = []
        for band in band_names : #{band : []}
            xr_band = xr_croped.loc[{dim : band}]
            vals_arr = xr_band.to_numpy().ravel()
            val = stats_function(vals_arr) # np.nanmean(xr_band.to_numpy().ravel()) # pd.DataFrame(xr_band.values.ravel()).mean()[0] # alt 
            vals_list.append(val)
        
        vals_df.append(vals_list)#pd.DataFrame(vals_list).reset_index()
    
    df_xr = pd.DataFrame(vals_df, columns = band_names)
    df_xr['geometry'] = gdf.geometry
    
    # Transform the GeoDataFrame to the CRS 
    xr_gdf = gpd.GeoDataFrame(df_xr, geometry= gdf.geometry )
    xr_gdf = xr_gdf.set_crs(gdf.crs)
    
    return xr_gdf

def bands_vals (stack_xr, dim = 'bands') :
    
    """
    Returns a dataframe containing the values of each band/predictor in the xarray DataArray stack_xr.
    
    Parameters:
    stack_xr (xarray.DataArray): 
        xarray.DataArray containing the bands.
    dim (str, optional): 
        Parameter specifies the name of the dimension along which the bands are stacked. Default value is 'bands'.
    
    Returns:
        pandas DataFrame: A dataframe containing the values of each band/predictor in stack_xr.
    """
    # Input validation
    if not isinstance(stack_xr, xr.DataArray):
        raise TypeError('stack_xr must be an xarray DataArray')
    
    # Get the bands names
    band_names = list(stack_xr[dim].values.ravel())
    # Create an empty list to store the values of each variable-predictor
    df_list = []
    # Iterate over the arrays in xarray DataArray
    for i, arr in enumerate(stack_xr.values):
        # Flatten the array and create a dataframe with a single column for each variable
        df_xr = pd.DataFrame(arr.ravel(), columns=[i])
        # Append the dataframe to the list
        df_list.append(df_xr)

    # Concatenate the dataframes in the list along the columns axis
    df_values = pd.concat(df_list, axis=1)
    df_values.columns = band_names
    
    return df_values

def extract_values (stack_xr, gdf, dim = 'bands'): 
 
    """
    Extract values from an xarray with geo attributes over GeoDataFrame wih a set of points 

    Parameters
    ----------
    stack_xr : xarray.DataArray
        xarray.DataArray with one or multiple bands
    gdf : GeoDataFrame 
        geodataframe with a set of points
    dim (str, optional): 
        Parameter specifies the name of the dimension along which the bands are stacked. Default value is 'bands'.

    Returns
    -------
    DataFrame 
        DataFrame with extracted values at each band over each point 

    """
    # Run helper function
    gdf = check_xr_gdf(stack_xr, gdf)
    
    # Get the x,y from each geo pts 
    coords_list = [(x,y) for x,y in zip(gdf['geometry'].x , gdf['geometry'].y)]
    coords_df = pd.DataFrame(coords_list, columns = ['longitude', 'latitude'])
    gdf['longitude'] = coords_df['longitude']
    gdf['latitude'] = coords_df['latitude']
    
    # Get the bands names
    band_names = list(stack_xr[dim].values.ravel())
    
    vals_list = []
    # Loop over each GeoDataFrame Point feature 
    for row in range(len(gdf)):
        df_row = gdf[row : row+1]
        x_long = df_row.longitude.values[0]
        y_lat = df_row.latitude.values[0] 
        
        # Extract vals for each coords
        pix_val = stack_xr.sel(x=x_long, y= y_lat,method='nearest').copy().values.tolist()
        vals_list.append(pix_val)
    
    df_training = pd.DataFrame(vals_list, columns = band_names)
    
    return df_training

def rsxr_translate (stack_xr, dx, dy) :
    
    """Translate/shift a xarray with geo attributes to a new position based on x and y
    
    Parameters
    ----------
    stack_xr : xarray.DataArray
        xarray.DataArray with one or multiple bands
    dx : int or float 
        Define the the shift in horizontal/longitude direction
    dy : int or float 
        Define the the shift in vertical/latitude direction

    Returns
    -------
    xarray.DataArray 
        Translated xarray.DataArray to new position 
    """
    # Input validation
    if not isinstance(stack_xr, xr.DataArray):
        raise TypeError('stack_xr must be an xarray DataArray')
    if (stack_xr.rio.crs == None):
        raise AttributeError('The passed xarray DataArray has no CRS')
        
    # Define the x and y offset distances in meters
    x_offset = dx
    y_offset = dy
    
    # Translate the xarray by the given offsets
    stack_xr_shift = stack_xr.copy()
    stack_xr_shift['x'] = stack_xr_shift.x + x_offset
    stack_xr_shift['y'] = stack_xr_shift.y + y_offset
    
    return stack_xr_shift

def reclassify(xr_data, bins):
    
    """Classify the values in a data array using a list of bins.
    
    Parameters
    ----------
    xr_data : xarray.DataArray
        xarray.DataArray with one band
    bins : list
        A list of bins to use for classification.
        
    Returns
    -------
    xarray.DataArray
        The classified xarray.DataArray
    """
    # Input validation
    if not isinstance(xr_data, xr.DataArray):
        raise TypeError('stack_xr must be an xarray DataArray')

    # Initialize the classified xarray with the lowest class
    xr_classified = xr.ones_like(xr_data) * (len(bins) - 1)
    
    # Classify the data using xr.where
    for i in range(len(bins) - 1):
        xr_classified = xr.where((xr_data >= bins[i]) & (xr_data < bins[i+1]), i+1, xr_classified)
    
    return xr_classified