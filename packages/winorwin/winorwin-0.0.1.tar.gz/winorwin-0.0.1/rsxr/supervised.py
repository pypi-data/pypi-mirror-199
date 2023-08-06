import xarray as xr
from raster_xarray import bands_vals
import pandas as pd

def rsxr_predict (model, stack_xr, task, dim = 'bands' , method = 'prediction'):
    
    """Spatial model predictions with a fitted Supervised ML model to an xarray DataArray with geo attributes

    Parameters
    ----------
    model : ML model
        Fitted model object, either classifier or regressor from sklearn
    stack_xr : xarray.DataArray
        A Dataset with one or multiple bands representing the independent (predictor) variables   
    task : str 
        either regression or classification 
    method : str
        specify either 'prediction' or 'proba'. By default method is set to 'prediction'. 'praba' is only possible for classification tasks
    dim (str, optional): 
        Parameter specifies the name of the dimension along which the bands are stacked. Default value is 'bands'.
    
    Returns
    -------
    xarray.DataArray 
        predicted xarray DataArray 

    """
    # Input validation
    if not isinstance(stack_xr, xr.DataArray):
        raise TypeError('stack_xr must be an xarray DataArray')
    if not isinstance(dim, str):
        raise TypeError('dim must be a string')
    if (task != 'regression' and task != 'classification'):
        raise AttributeError(f"ERROR: Invalid task {task}. Please specify either modelression or classification.")
        
    elif (task == 'regression' and method == 'proba'):
        raise AttributeError(f"ERROR: Running a probality for a regression task is not possible, Please verify your Task.")  
    
    elif (method != 'prediction' and method != 'proba'):
        raise AttributeError(f"ERROR: Invalid method {method}. Please specify either prediction or proba.")

    elif (task == 'regression' or task == 'classification'):
        # Get the predictors names
        pred_names = list(stack_xr[dim].values.ravel())
        
        # Extract values from each predictor        
        df_values = bands_vals (stack_xr, dim = dim)
                    
        # Get a copy of the df and remove nan 
        ## NOTE : If one predictor have nan values while the rest dont, the overlapping pixels will be considered as nan
        df_values_copy = df_values.copy()
        df_values_copy = df_values_copy.dropna()
        
        if method == 'prediction':
            model_preds = model.predict(df_values_copy)
            
            # Save the prediction in the df
            df_values_copy['pred'] = model_preds  
            df_values['pred_valid'] = df_values_copy.pred
            
            # Convert to an xarray object
            xr_prediction = xr.DataArray(df_values.pred_valid.values.reshape(stack_xr.shape[1:]), 
                                           coords={'y': stack_xr.y,'x': stack_xr.x},
                                           dims=["y", "x"])
    
            xr_prediction = xr_prediction.rename("prediction")

            # Add geospatial information crs
            xr_prediction.rio.set_crs(stack_xr.rio.crs)
        
        elif (task == 'classification' and method == 'proba'):
            
            # Run the predict proba
            model_preds = model.predict_proba(df_values_copy)
    
            # Get the classes we have :
            lc_class_proba = pd.DataFrame(model_preds)
            n_classes = lc_class_proba.columns.stop
            
            df_values_valid = df_values_copy.copy()
            xr_list = []
            
            # Loop over the each class and get the predicted values 
            for i in range(n_classes):
                # save the prediction in the df
                df_values_valid['pred'] =  lc_class_proba[[i]].values.ravel()
                df_values['pred_valid'] = df_values_valid.pred
                
                # Convert to an xarray object
                xr_prob_pred = xr.DataArray(df_values.pred_valid.values.reshape(stack_xr.shape[1:]), 
                                                 coords={'y': stack_xr.y,'x': stack_xr.x},
                                                 dims=["y", "x"])
    
                xr_list.append(xr_prob_pred)

            xr_prediction = xr.concat(xr_list, "class")
            xr_prediction.coords['class'] = list(range(n_classes))
            
            xr_prediction = xr_prediction.rename("probablity")
            # Add geospatial information crs
            xr_prediction.rio.set_crs(stack_xr.rio.crs)
            
    return xr_prediction
