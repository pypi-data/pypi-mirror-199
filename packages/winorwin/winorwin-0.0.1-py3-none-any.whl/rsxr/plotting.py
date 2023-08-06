import xarray as xr
from raster_xarray import bands_vals
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def rgb_plot (stack_xr, dim = 'bands', ax = None, **kwargs):
    
    """rgb_plot returns an rgb plot with a combination of 3 bands

    Parameters
    ----------
    stack_xr : xarray.DataArray
        xarray Dataset with 3 bands
    dim (str, optional): 
        The name of the dimension corresponding to the bands. Default value is 'bands'.
    
    Returns
    -------
    rgb plot : It can be a true color composite or a false color composite
    based on https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html

    """ 
    # Input validation
    if not isinstance(stack_xr, xr.DataArray):
        raise TypeError('stack_xr must be an xarray DataArray')
    if len(stack_xr[dim].values) != 3 :
        raise ValueError("Please specify a stack_xr with only a combination of 3 bands for an rgb plot") 

    if ax:
        show = False
    else:
        show = True
        ax = plt.gca()

    fig = ax.get_figure()
    
    stack_xr.plot.imshow(robust= True, ax =ax )
    
    if show:
        plt.show()
        
def rsxr_hist (stack_xr, dim = 'bands', title = 'Histogram', overlay: bool = True, alpha = 0.5 , bins = 50, ax = None, **kwargs):
    
    """
    Plots a histogram of the values of each band/predictor in the xarray DataArray stack_xr.
    
    Based on rasterio show_hist
    reference : https://github.com/rasterio/rasterio/blob/824a8dc40dd3475c3bfdcafc42d18f1c63c02f28/rasterio/plot.py#L219    
    
    Parameters:
    stack_xr (xarray DataArray): 
        The DataArray containing the bands/bands.
    dim (str, optional): 
        The dimension in stack_xr that contains the names of the bands/bands. Default value is 'bands'.
    title (str, optional): 
        The title of the histogram. Default value is 'Histogram'.
    overlay (bool, optional):
        If True (default), the function will return a single overlayed histogram plot for each band.
        If False, the function will return multiple histogram plots for each band. 
    alpha (float, optional): 
        The alpha transparency of the histogram bars. Default value is 0.5.
    bins (int, optional): 
        The number of bins to use in the histogram. Default value is 50.
    ax (matplotlib Axes object, optional): 
        The Axes object to use for the histogram. If not specified, a new Axes object will be created.
    **kwargs: Additional keyword arguments to pass to the hist() function.
    
    Returns:
    histogram plot
    """
    
    if not isinstance(overlay, bool):
        raise TypeError("'overlay' must be a boolean value (True or False). By default overlay = True")

    bands_vals_df = bands_vals (stack_xr, dim = dim)
    
    if overlay == True:
    
        if ax:
            show = False
        else:
            show = True
            ax = plt.gca()

        fig = ax.get_figure()
    
        for col in bands_vals_df.columns:
            bands_vals_df[col].hist( bins = bins, legend = col, alpha = alpha, ax = ax, **kwargs)

        ax.legend(loc="upper right")
        ax.set_title(title, fontweight='bold')
        ax.grid(True)
        ax.set_xlabel('DN')
        ax.set_ylabel('Frequency')
        if show:
            plt.show()
            
    else:
         bands_vals_df.hist(bins = bins, alpha = alpha, stacked=False, **kwargs)

def rsxr_corr (stack_xr, dim = 'bands', ax = None, **kwargs):
    
    """
    Plots a heatmap of the Pearson correlations between the bands/bands in the xarray DataArray stack_xr.
    
    Parameters:
    stack_xr (xarray DataArray): 
        The DataArray containing the bands/bands.
    dim (str, optional): 
        The dimension in stack_xr that contains the names of the bands/bands. Default value is 'bands'.
    ax (matplotlib Axes object, optional): 
        The Axes object to use for the heatmap. If not specified, a new Axes object will be created.
    **kwargs: 
        Additional keyword arguments to pass to the heatmap() function.
    
    Returns:
    heatmap plot
    """
    
    bands_vals_df = bands_vals (stack_xr, dim = dim)
    
    if ax:
        show = False
    else:
        show = True
        ax = plt.gca()

    fig = ax.get_figure()
    
    corr = corr = bands_vals_df.corr()
    df_lt = corr.where(np.tril(np.ones(corr.shape)).astype(bool))
    
    sns.heatmap(df_lt, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot = True, ax = ax, **kwargs)

    ax.set_title('Pearson correlation', fontsize = 10, fontweight = 'bold')
    ax.tick_params(labelsize = 9)
    
    if show:
        plt.show()
            
