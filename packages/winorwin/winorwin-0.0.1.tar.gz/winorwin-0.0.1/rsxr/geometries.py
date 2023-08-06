import geopandas as gpd
from shapely.geometry import Point
import numpy as np

def Random_Points_in_Polygon(geo_polygon, number, random_state = None):
    
    """
    Generates a specified number of random points within a given polygon.
    
    Parameters:
    geo_polygon (shapely Polygon object) 
        The polygon in which to generate the points.
    number (int): 
        The number of points to generate.
    random_state (int, optional): 
    The seed for the random number generator. Default value is None.
    
    Returns:
        points (list): A list of shapely Point objects representing the generated points.
    
    Source: This function was adapted from the solution provided by Martin D. Maas, Ph.D in the following https://www.matecdev.com/ site:
    https://www.matecdev.com/posts/random-points-in-polygon.html
    """
    
    np_rs = np.random.RandomState(random_state)
    points = []
    minx, miny, maxx, maxy = geo_polygon.bounds
    while len(points) < number:
        pnt = Point(np_rs.uniform(minx, maxx), np_rs.uniform(miny, maxy))
        if geo_polygon.contains(pnt):
            points.append(pnt)
    return points

def points_geodata(geo_polygon, classes, number, random_state = None) :
    
    """
    Generates a specified number of random points within a given polygon and returns them as a GeoDataFrame with assigned classes.
    
    Parameters:
    geo_polygon (shapely Polygon object): 
        The polygon in which to generate the points.
    classes (list): 
        A list of strings representing the names of the columns to include in the GeoDataFrame.
        for example ['id', 'class_name'] --> a list containing the id and the class for each polygon
    number (int): 
        The number of points to generate.
    random_state (int, optional): 
        The seed for the random number generator. Default value is None.
    
    Returns:
    geo_points (GeoDataFrame): A GeoDataFrame containing the generated points and the specified columns.
    """
    
    points = Random_Points_in_Polygon(geo_polygon.unary_union, number, random_state)

    # Plot the list of points
    xs = [point.x for point in points]
    ys = [point.y for point in points]

    gdf_points = gpd.GeoSeries(gpd.points_from_xy(xs, ys))
    geo_points = gpd.GeoDataFrame(gdf_points)
    geo_points = geo_points.rename(columns={0:'geometry'}).set_geometry('geometry')
    
    for i in classes:
        geo_points[i] = np.repeat(geo_polygon[[i]].values, number)
        #geo_points['class_name'] = np.repeat(geo_polygon.class_name.values, number)
    
    return geo_points
    
def points_gdf (gdf, classes, number, random_state = None):
    
    """
    Generates a specified number of random points within each polygon in a given GeoDataFrame and returns them as a new GeoDataFrame with the
    corresponding classes.
    
    Parameters:
    geo_df : GeoDataFrame
        The GeoDataFrame containing the polygons in which to generate the points.
    classes : list 
        A list of strings representing the names of the columns to include in the output GeoDataFrame.
    number : int
        The number of points to generate for each polygon.
    random_state : (int, optional)
        The seed for the random number generator. Default value is None.
    
    Returns:
    gdf_df : GeoDataFrame 
        A GeoDataFrame containing the generated points and the specified columns/classes.
    """
    # Check that the input is a GeoDataFrame
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError('Input must be a GeoDataFrame')
    
    list_gdf = []
    for row in range(len(gdf)):
        df_row = gdf[row : row+1]
        geo_points = points_geodata(df_row, classes, number, random_state)
        list_gdf.append(geo_points)
        
    gdf_df = gpd.GeoDataFrame(np.vstack(list_gdf), columns = ['geometry'] + classes)
    gdf_df = gdf_df.set_crs(gdf.crs)
    return gdf_df
