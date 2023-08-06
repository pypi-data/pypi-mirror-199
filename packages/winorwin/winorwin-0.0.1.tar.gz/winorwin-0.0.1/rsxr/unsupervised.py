import xarray as xr
from raster_xarray import bands_vals
import pandas as pd
from sklearn.cluster import KMeans


def rsxr_kmeans (stack_xr, ncluster, dim = 'bands', random_state = None, **kwargs):
    
    """Perfom a kmeans Spatial clustering : An Unsupervised Classification using kmeans over an xarray DataArray with geo attributes.
       Unsupervised classification is performed using the k-means algorithm. By default lloyd algorithm is used
 
    Parameters
    ----------
    stack_xr : xarray.DataArray
        A Dataset with one or multiple bands representing the independent (predictor) variables   
    ncluster : int 
        The number of clusters to form 
    dim : str, optional
        Parameter specifies the name of the dimension along which the bands are stacked. Default value is 'bands'.
    random_state : int, optional
        The random seed for reproducibility. Default is None.
    kwargs : set of arguments from sklean api : https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
            eg: algorithm {“lloyd”, “elkan”, “auto”, “full”}, default=”lloyd”

    Returns
    -------
    xarray.DataArray 
         clustered classified xarray with Geo attribute 

    """
    # Input validation
    if not isinstance(stack_xr, xr.DataArray):
        raise TypeError('stack_xr must be an xarray DataArray')
    if not isinstance(ncluster, int) or ncluster <= 0:
        raise ValueError('ncluster must be a positive integer')
    if not isinstance(random_state, (int, type(None))):
        raise TypeError('random_state must be an integer or None')
    if not isinstance(dim, str):
        raise TypeError('dim must be a string')
    
    df_values = bands_vals (stack_xr, dim = dim)

    # Get a copy of the df and remove nan since kmeans cant handle nan values
    df_values_copy = df_values.copy()
    df_values_copy = df_values_copy.dropna()
    
    # Check if the number of clusters is larger than the number of samples
    if ncluster > df_values_copy.shape[0]:
        raise ValueError(f'The number of clusters ({ncluster}) must be less than or equal to the number of samples ({df_values_copy.shape[0]})')
    
    # Fit the model
    model = KMeans(n_clusters = ncluster, random_state = random_state, **kwargs )
    model_preds = model.fit(df_values_copy)
    
    # save in the df
    df_values_copy['pred'] = model_preds.labels_  
    df_values['pred_valid'] = df_values_copy.pred

    # convert to an xarray object
    kmeans_prediction = xr.DataArray(df_values.pred_valid.values.reshape(stack_xr.shape[1:]), 
                                           coords={'y': stack_xr.y,'x': stack_xr.x},
                                           dims=["y", "x"])
    
    kmeans_prediction = kmeans_prediction.rename("prediction")

    # add geospatial information crs
    kmeans_prediction.rio.set_crs(stack_xr.rio.crs)
    
    return kmeans_prediction
