import xarray as xr
from raster_xarray import bands_vals
import pandas as pd
from sklearn.decomposition import PCA

def rsxr_pca (model, stack_xr, dim = 'bands'):
    
    """Decompose a fitted PCA model to an xarray DataArray with geo attributes
    
    This function takes in a fitted PCA model object and an xarray DataArray and
    decomposes the DataArray using the fitted model. The resulting decomposed DataArray is returned.
    
    Parameters
    ----------
    model : sklearn.decomposition.PCA
        A fitted PCA model object
    stack_xr : xarray.DataArray
        A Dataset with one or multiple bands representing the independent (predictor) variables   
    dim : str, optional
        Parameter specifies the name of the dimension along which the bands are stacked. Default value is 'bands'.
    
    Returns
    -------
    xarray.DataArray
        The decomposed xarray DataArray
    """
    # Input validation
    if not isinstance(model, PCA):
        raise TypeError('model must be a fitted PCA object')
    if not isinstance(stack_xr, xr.DataArray):
        raise TypeError('stack_xr must be an xarray DataArray')
    if not isinstance(dim, str):
        raise TypeError('dim must be a string')

    # Get how many bands and components we have bands len
    n_preds = len(list(stack_xr[dim].values.ravel()))
    n_features = model.n_features_
    n_components = model.n_components
    # Raise an error if applicable
    if n_features != n_preds:
        raise AttributeError(f"ERROR: The number of features {n_features} provided by the model does not match the number of bands {n_preds}.")

    # Extract values from each predictor
    df_values = bands_vals (stack_xr, dim = dim)

    df_values_copy = df_values.copy()
    df_values_copy = df_values_copy.dropna()

    # Get the PCAs prediction we have :
    model_preds = model.fit_transform(df_values_copy)
    pca_preds = pd.DataFrame(model_preds)

    xr_list = []
    # Loop over the PCA prediction and get the predicted values 
    for i in range(n_components):
        # Save the prediction in the df
        df_values_copy['pred'] =  pca_preds[[i]].values
        df_values['pca_valid'] = df_values_copy['pred']

        # Convert to an xarray object
        xr_prob_pred = xr.DataArray(df_values.pca_valid.values.reshape(stack_xr.shape[1:]), 
                                    coords={'y': stack_xr.y,'x': stack_xr.x},
                                    dims=["y", "x"])
    
        xr_list.append(xr_prob_pred)

    xr_prediction = xr.concat(xr_list, "pca")
    xr_prediction.coords['pca'] = list(range(1, n_components + 1))
    
    xr_prediction = xr_prediction.rename("prediction")
    # Add geospatial information crs
    xr_prediction.rio.set_crs(stack_xr.rio.crs)
    
    return xr_prediction
