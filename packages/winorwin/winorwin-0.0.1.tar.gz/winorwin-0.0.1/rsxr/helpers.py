import xarray as xr
import geopandas as gpd
import warnings

def check_xr_gdf (stack_xr, gdf): 

    """Helper function based for the prodived xarray and GeoDataFrame

    Parameters
    ----------
    stack_xr : xarray.DataArray
        A Dataset with one or multiple bands representing the independent (predictor) variables.
    gdf : geopandas.GeoDataFrame
        A GeoDataFrame containing geometries to extract values from stack_xr.
    warn : bool, optional
        Whether to display a warning if the CRS of gdf is different from that of stack_xr, by default True.

    Returns
    -------
    tuple
        A tuple containing:
        - A boolean value indicating whether the input `stack_xr` is a valid xarray DataArray.
        - A boolean value indicating whether the input `gdf` is a valid GeoDataFrame.
        - A boolean value indicating whether the CRS of the `stack_xr` and `gdf` are valid.
    GeoDataFrame 
        - The transformed GeoDataFrame, if necessary.
    """
    # Input validation
    if not isinstance(stack_xr, xr.DataArray):
        raise TypeError('stack_xr must be an xarray DataArray')
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError('gdf must be a geopandas GeoDataFrame')
    if stack_xr.rio.crs is None or gdf.crs is None:
        raise AttributeError('stack_xr and gdf must have a valid CRS')
        
    # Transform the GeoDataFrame to the CRS of the raster image, if necessary
    if gdf.crs != stack_xr.rio.crs:
        gdf = gdf.to_crs(stack_xr.rio.crs)
        warnings.warn('The passed GeoDataFrame has a different CRS from the DataArray. Please check the CRS of the passed GeoDataFrame.')
    
    return gdf     
