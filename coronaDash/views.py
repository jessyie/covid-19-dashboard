from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
import folium
import pandas as pd # type: ignore
import os # type: ignore
import geopandas as gpd
import numpy as np
import fiona
import matplotlib
import locale
import json
from folium import plugins
from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings

# Convert WindowsPath object to string
data_loc_str = str(settings.DATA_LOC)


def initialise_chart(case = 'Total_Confirmed', continent = 'Africa'):
 
    #____________

    #// CHARTS //

    #____________

    filename2 = case + '.csv' 
    path2 = os.path.join(data_loc_str, 'CDATA', filename2)
    df = gpd.read_file(path2)
    
    grouped = df.groupby(['Continent'])
    dfGroup = grouped.get_group(continent)
    
    
    #______________________
    
    # // PROCESSING //
    
    #______________________
    
    # // Finding the Total confirmed cases and its relation to the continents(A)
    dfGroupA = df[["Continent", "Total"]] # Selecting specific columns and getting rid of the commas in the string
    dfGroupA["Total"] = dfGroupA["Total"].astype('int') # Converting all the string in the columns to integers
    tSum = dfGroupA["Total"].values.sum() # Sum operation on a specific column
    dfContinentSum = dfGroupA.groupby(by=["Continent"])["Total"].sum().reset_index()
    graph1AX = dfContinentSum['Continent'].values.tolist()
    graph1AY = dfContinentSum['Total']
    #print(dfContinentSum)
    
    # // Finding the countries and its maximum comfirmed cases(A)
    dfGroupB = dfGroup[["Country", "Total"]] # Selecting specific columns and getting rid of the commas in the string
    dfGroupB["Total"] = dfGroupB["Total"].astype('int') # Converting all the string in the columns to integers
    tSumB = dfGroupB["Total"].values.sum() # Sum operation on a specific column
    dfContinentSumB = dfGroupB.groupby(by=["Country"])["Total"].sum().reset_index()
    graph1BX = dfContinentSumB['Country'].values.tolist()
    graph1BY = dfContinentSumB['Total']
    #print(dfContinentSumB)

    dfGroupBA = df[["Country", "Total"]] # Selecting specific columns and getting rid of the commas in the string
    dfGroupBA["Total"] = dfGroupBA["Total"].astype('int') # Converting all the string in the columns to integers
    tSumBA = dfGroupBA["Total"].values.sum() # Sum operation on a specific column
    dfContinentSumBA = dfGroupBA.groupby(by=["Country"])["Total"].sum().reset_index()
    graph1BXA = dfContinentSumBA['Country'].values.tolist()
    graph1BYA = dfContinentSumBA['Total']
    #print(dfContinentSumBA)
    

    #________________

    #// Packaging //

    #________________

    tSum = dfGroupA["Total"].values.sum().astype(int).tolist()
    graph1AX = dfContinentSum['Continent'].values.tolist() 
    graph1AY = dfContinentSum['Total'].values.astype(int).tolist()

    tSumB = dfGroupB["Total"].values.sum().astype(int).tolist()
    graph1BX = dfContinentSumB['Country'].values.tolist()
    graph1BY = dfContinentSumB['Total'].values.astype(int).tolist()


    #________________

    #// MAP CANVAS (1) //
    
    #________________
    world_geo = os.path.join(data_loc_str, 'CDATA', 'world_countries.json')

    world_map = folium.Map(location=[0, 0], zoom_start=2)

    #// The following is done to let Folium determine the scale.
   # threshold_scale = np.linspace(dfContinentSumBA["Total"].min(),
    #                                dfContinentSumBA["Total"].max(),
    #                                9, dtype=int) 
    #threshold_scale = threshold_scale.tolist() # change the numpy array to list
    #threshold_scale[-1] = threshold_scale[-1] + 1 # last value of the list must be greater than the maximum total

    folium.Choropleth(
        geo_data=world_geo,
        data=dfContinentSumBA,
        columns=['Country', 'Total'],
        key_on='feature.properties.name',
        #threshold_scale=threshold_scale,
        fill_color='YlOrRd',
        name='Totals',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total cases based on each country',
        tooltip=folium.GeoJsonTooltip(fields=["Country", "Total"]),
        reset=True).add_to(world_map)

    folium.features.GeoJson(world_geo,
                            name="Countries", tooltip=folium.GeoJsonTooltip(fields=["name"]),).add_to(world_map)

    folium.raster_layers.TileLayer('Stamen Terrain').add_to(world_map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(world_map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(world_map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(world_map)
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(world_map)

    fullscreen_control = folium.plugins.Fullscreen()
    world_map.add_child(fullscreen_control)

    folium.LayerControl().add_to(world_map)

    world_map = world_map._repr_html_()


    #________________

    #// MAP CANVAS (2) //
    
    #________________
    world_geo2 = os.path.join(data_loc_str, 'CDATA', 'world_countries.json')

    world_map2 = folium.Map(location=[0, 0], zoom_start=2)

    #// The following is done to let Folium determine the scale.
   # threshold_scale = np.linspace(dfContinentSumBA["Total"].min(),
    #                                dfContinentSumBA["Total"].max(),
    #                                9, dtype=int) 
    #threshold_scale = threshold_scale.tolist() # change the numpy array to list
    #threshold_scale[-1] = threshold_scale[-1] + 1 # last value of the list must be greater than the maximum total

    folium.Choropleth(
        geo_data=world_geo2,
        data=dfContinentSumB,
        columns=['Country', 'Total'],
        key_on='feature.properties.name',
        #threshold_scale=threshold_scale,
        fill_color='YlOrRd',
        name='Totals',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total cases based on each country',
        tooltip=folium.GeoJsonTooltip(fields=["Country", "Total"]),
        reset=True).add_to(world_map2)

    folium.features.GeoJson(world_geo2,
                            name="Countries", tooltip=folium.GeoJsonTooltip(fields=["name"]),).add_to(world_map2)

    folium.raster_layers.TileLayer('Stamen Terrain').add_to(world_map2)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(world_map2)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(world_map2)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(world_map2)
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(world_map2)

    fullscreen_control = folium.plugins.Fullscreen()
    world_map2.add_child(fullscreen_control)

    folium.LayerControl().add_to(world_map2)

    world_map2 = world_map2._repr_html_()



    context = {
        'tSum' : tSum,
        'tSumB' : tSumB,
        'graph1AX' : graph1AX,
        'graph1AY' : graph1AY,
        'graph1BX' : graph1BX,
        'graph1BY' : graph1BY,
        'world_map' : world_map,
        'world_map2' : world_map2
        
    }
    return context

def map(request):
    data = initialise_chart()
    # data['m'] = m
    return render(request, 'map.html', data)


def update_charts(request):
    
    selected_case = request.GET.get("case")
    selected_continent = request.GET.get("continent")
    
    if selected_case == "Total_Confirmed":
        csv_path = os.path.join(data_loc_str, 'CDATA', 'Total_Confirmed.csv')
    elif selected_case == "Total_Deaths":
        csv_path = os.path.join(data_loc_str, 'CDATA', 'Total_Deaths.csv')
    elif selected_case == "Total_Recovered":
        csv_path = os.path.join(data_loc_str, 'CDATA', 'Total_Recovered.csv')
    else:
        return JsonResponse({"error": "Invalid selection."})

    
    if selected_continent == '':
        data = initialise_chart(selected_case)
    else:
        data = initialise_chart(selected_case, selected_continent)
        
    return JsonResponse(data)