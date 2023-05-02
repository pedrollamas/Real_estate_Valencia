#--------------------LIBRERÍAS--------------------#
import streamlit as st 
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots

import os
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Mapas interactivos
import json
import folium
from streamlit_folium import st_folium, folium_static
from streamlit_option_menu import option_menu
from folium.plugins import FastMarkerCluster
import geopandas as gpd
from branca.colormap import LinearColormap

# Gráficos de plotly
import plotly.graph_objs as go
import chart_studio.plotly as py
from plotly.offline import iplot, init_notebook_mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)

# Los warnings
import warnings
warnings.filterwarnings('ignore')

from streamlit_extras.badges import badge
from streamlit_extras.let_it_rain import rain

#--------------------CONFIGURACIÓN DE LA PÁGINA----------------------------#
st.set_page_config(page_title="EDA", layout="wide", page_icon="📊")

st.title("Análisis exploratorio de los datos")

badge(type="github", name="pedrollamas")



hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.write("""
<style>
h1, h2, h3, h4, h5, h6 {
    font-family: 'Verdana';
}
</style>
""", unsafe_allow_html=True)

# Creamos el Menú.

selected = option_menu(None, ["Dataframe", 'Visualización de los datos'],icons=['rulers', 'bar-chart-line'],styles={"container": {"background-color": "#2AB09C"}}, default_index=1)


if selected == 'Dataframe':
    # Cargamos el dataset.
    valencia = pd.read_csv("data/valencia_barrio_municipio.csv")
    valencia.drop('Unnamed: 0', axis =1, inplace=True)
    valencia.drop('Precio_garaje', axis=1, inplace=True)
    valencia.drop('Municipio', axis=1, inplace=True)
    valencia.drop('ID', axis =1, inplace=True)
    valencia = valencia[valencia['Año_construcción'] >= 1500]

    # Mostramos el dataframe
    valencia

    if st.button('Descargar csv'):
        valencia.to_csv("real_state_valencia.csv")
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("Explicación columnas y valores")
        st.markdown("""- **Periodo**: 2018 (03/06/09/12): nos indica el año y mes. Va por trimestres.
- **Precio**: Está en formato decimal, lo normal sería tenerlo en enteros.
- **Preciom2**: Con decimales, podríamos pasarlo a dos decimales.
- **Metros_construidos**: Está en formato decimal, lo normal sería tenerlo en enteros.
- **Habitaciones**: Indica el nº de habitaciones, comprobar valores muy altos (hay un 81).
- **Baños**: Indica el nº de baños, comprobar valores muy altos (hay un 10 y 12).
- **Terraza**: 0 no tiene, 1 tiene.
- **Ascensor**: 0 no tiene, 1 tiene.
- **Aire_Acondicionado**: 0 no tiene, 1 tiene.
- **Servicios**: Tenemos 1, 2 y 3, en función del nº de servicios que presta el edificio.
- **Garaje**: 0 no tiene, 1 tiene.
- **Garaje_en_Precio**: 0 no está en el precio, 1 si está en el precio.
- **Orientación_norte**: 0 no tiene, 1 si tiene orientación norte.
- **Orientación_sur**: 0 no tiene, 1 si tiene orientación sur.
- **Orientación_este**: 0 no tiene, 1 si tiene orientación este.
- **Orientación_oeste**: 0 no tiene, 1 si tiene orientación oeste.
- **Trastero**: 0 no tiene, 1 si tiene trastero.
- **Armarios**: 0 no tiene, 1 si tiene armarios.
- **Piscina**: 0 no tiene, 1 tiene piscina.
- **Conserje**: 0 no tiene, 1 si tiene.
- **Calidad_suelo**: Del -1 al 11, indica la calidad de menos a más.
- **Año_diseñado**: Indica el año del diseño.
- **Plantas_máximas**: Indica las plantas máximas que tiene el edificio.
- **Número_viviendas**: Indica el número de viviendas que hay en el edificio.
- **Calidad_catastral**: Del 0 al 9 indica la calidad catastral, de menos a más.
- **Distancia_centro**: Por KM indica la distancia al centro de la ciudad.
- **Distancia_metro**: Indica por KM la distancia al metro más cercano.
- **Distancia_Blasco**: Nos indica la distancia a la calle principal de Valenccia. Avenida de Blasco Ibáñez.
- **Latitud y longitud**: Para localizar la vivienda.""")
    
    with col2:
        st.header("Determinación de los barrios")
        st.markdown("""Para poder determinar los barrios, que no se encontraban en el dataframe original he generado un código que calcula la distancia en kilómetros entre dos puntos en la superficie de la Tierra, dados sus valores de latitud y longitud. Primero, se define una función llamada "calculateDistance" que toma los valores de latitud y longitud de los dos puntos como argumentos y devuelve la distancia entre ellos utilizando la fórmula del círculo máximo. La función utiliza las funciones trigonométricas coseno y seno, que se importan del módulo math.

Luego, se define un bucle para recorrer cada fila de un DataFrame llamado "ventas_valencia", que contiene información de ventas de propiedades en la ciudad de Valencia, España. Dentro del bucle, se inicializa una lista vacía llamada "neighbourhood". Para cada punto en el DataFrame, se calcula la distancia entre ese punto y cada uno de los puntos en otro DataFrame llamado "listado", sacado de http://insideairbnb.com que contiene información de Airbnb sobre los barrios de Valencia. Defino una función "calculateDistance" para calcular la distancia entre los dos puntos y se guarda el valor mínimo de la distancia y el nombre del barrio correspondiente. Luego, se agrega el nombre del barrio a la lista "Barrio" que finalmente se agrega a nuestro dataframe de trabajo.

En resumen, este código calcula la distancia entre dos puntos en la superficie de la Tierra y utiliza esta información para asignar un barrio correspondiente a cada venta de propiedad en Valencia.""")
        st.code("""Cálculo de distancias entre puntos
        From math import acos, sin, cos 
        # Primero, creamos una función que calcule la distancia entre dos puntos.
        
            def calculateDistance(lat1, lon1, lat2, lon2):
            
        # La fórmula para calcular la distancia entre dos puntos en una esfera usando latitud y longitud es:
            # d = acos(sin(lat1) * sin(lat2) +
            # cos(lat1) * cos(lat2) *
            # cos(lon1 - lon2)) * R
            
        # d: distancia entre los puntos.
        # R: radio de la esfera (radio de la tierra = 6371 km)
        # lat1, lon1: latitud y longitud del primer punto.
        # lat2, lon2: latitud y longitud del segundo punto.
        
            R = 6371 # Radio de la tierra en km.
            d = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)) * R
            return d
        
        # Usamos un bucle para recorrer cada fila de 'ventas_valencia' y calcular la distancia entre los puntos.
        
        # Para cada punto, guardamos la distancia minima y el valor de 'neighbourhood', el barrio que le corresponde.
        neighbourhood = []
        for i in range(len(ventas_valencia)):
            lat1 = ventas_valencia['Latitud'][i]
            lon1 = ventas_valencia['Longitud'][i]
            min_dist = float('inf') # Distancia minima inicializada a infinito*(ver explicación abajo).
            min_neighbourhood = '' # Nombre del barrio inicializado a vacio*(ver explicación abajo).
                
        # Recorremos 'listado' y calculamos la distancia entre los puntos
        for j in range(len(listado)):
            lat2 = listado['latitude'][j]
            lon2 = listado['longitude'][j]
            dist = calculateDistance(lat1, lon1, lat2, lon2)
                
        # Guardamos el nombre del barrio cuando la distancia sea menor que la distancia minima.
        if dist < min_dist:
            min_dist = dist
            min_neighbourhood = listado['neighbourhood'][j]
                
        # Guardamos el nombre del barrio en la lista 'neighbourhood'.
        
        neighbourhood.append(min_neighbourhood)
        
        # Agregamos la lista 'neighbourhood' al dataframe 'ventas_valencia'.
        
        ventas_valencia['neighbourhood'] = neighbourhood
            
        # La distancia mínima inicializada al infinito significa que la distancia inicial entre los dos puntos se define como infinita. Esto significa que, al comenzar el bucle, se supone que la distancia entre los puntos es la máxima posible. Cada vez que se calcula una nueva distancia entre los puntos, se compara con la distancia mínima y se actualiza si la nueva distancia es menor que la distancia mínima.
        # El nombre del barrio inicializado a vacío significa que el nombre del barrio se establece como una cadena vacía al comenzar el bucle. Cada vez que se calcula una nueva distancia entre los puntos, se compara con la distancia mínima y, si la nueva distancia es menor que la distancia mínima, se actualiza el nombre del barrio.""")

if selected == 'Visualización de los datos':
    tab1, tab2 = st.tabs(["Características de las viviendas", "Barrios"])
    with tab1:
        
        st.markdown("""
        ### La orientación de la vivienda.

        A simple vista, la mejor orientación para un hogar es aquella que recibe la mayor intensidad de luz natural durante más horas. La mejor vivienda es la que aprovecha al máximo la trayectoria del sol para crear el mejor ambiente interior sin necesidad de consumir demasiada energía artificial. Hay estudios que calculan que una correcta orientación puede ayudarte a reducir hasta en un 70% el consumo energético.

        La orientación es un tema muy personal, en muchas ocasiones y de manera general en nuestro país se apuesta por la orientación sur, ya que se considera la más apropiada para ahorrar energía. Pero, intentado ahondar más en este asunto, vamos a ver las ventajas e inconvenientes de cada una de las orientaciones:

        * **Orientación sur**: En nuestro país se apuesta por esta orientación, ya que se considera la más apropiada para ahorrar energía. Esto es una gran ventaja para viviendas ubicadas en lugares fríos, sin embargo, en las zonas más cálidas será necesaria la instalación de toldos para evitar la sobreexposición. 

        * **Orientación este**: En esta orientación tendremos luz y sol desde el amanecer hasta el mediodía. Es la alternativa a la orientación sur en zonas muy calurosas. El calor se acumula hasta el mediodía y se libera durante la tarde-noche, por lo cual genera un consumo equilibrado de aire acondicionado y calefacción.

        * **Orientación oeste**: El sol incide en la vivienda durante todo el año del mediodía hasta al atardecer. En invierno la casa recibe pocas horas de luz natural pero son las que el sol irradia más calor. En verano, recibe el sol en las horas de más calor, lo que supone un coste energético en aire acondicionado.

        * **Orientación norte**: El sol no incide de forma directa, de manera que sólo recibe algo de radiación solar a primera y última hora durante los meses de verano. El gasto en calefacción durante el invierno es el más acentuado en la orientación norte.""")

        
        # Cargamos el dataset.
        desencodeado_valencia = pd.read_csv("data/desencodeado.csv")
        desencodeado_valencia.drop('Unnamed: 0', axis =1, inplace=True)
        # Agrupar datos por Orientación
        orientaciones = desencodeado_valencia[desencodeado_valencia['Orientación'] != 'Desconocida'].groupby('Orientación')['Orientación'].count().sort_values(ascending=False).reset_index(name='Cantidad')

        # Gráfico de barras de Orientación vs. Cantidad
        fig = px.bar(orientaciones, x="Orientación", y="Cantidad", color="Orientación",
                    color_discrete_map = {
                        'Orientación_norte': '#4285F4',
                        'Orientación_sur': '#0F9D58',
                        'Orientación_este': '#DB4437',
                        'Orientación_oeste': '#F4B400'})
        
        fig.update_layout(title_text='Cantidad de anuncios publicados por orientación')
        
        # Mostrar el gráfico usando Streamlit Plotly
        st.plotly_chart(fig, use_container_width=True)
    
        col1, col2 = st.columns(2)
        
        with col1:
            # Calcular los precios medios para cada orientación
            medias_orientacion = pd.DataFrame({
                'Orientación': ['Sur', 'Norte', 'Este', 'Oeste'],
                'Precio medio': [
                    desencodeado_valencia[desencodeado_valencia['Orientación'] == 'Sur']['Precio'].mean(),
                    desencodeado_valencia[desencodeado_valencia['Orientación'] == 'Norte']['Precio'].mean(),
                    desencodeado_valencia[desencodeado_valencia['Orientación'] == 'Este']['Precio'].mean(),
                    desencodeado_valencia[desencodeado_valencia['Orientación'] == 'Oeste']['Precio'].mean()]})
            fig = px.bar(medias_orientacion, x='Orientación', y='Precio medio',color='Orientación', color_discrete_map = {
                        'Orientación_norte': '#4285F4',
                        'Orientación_sur': '#0F9D58',
                        'Orientación_este': '#DB4437',
                        'Orientación_oeste': '#F4B400'})
            fig.update_layout(title_text='Precios medios para cada orientación.')
            st.plotly_chart(fig)
        with col2:
            st.write("""    """)
            st.write("""    """)
            st.write("""    """)
            st.write('El precio medio para los pisos con orientación sur es de {} euros.'.format(desencodeado_valencia[desencodeado_valencia['Orientación'] == 'Sur']['Precio'].mean().astype(int)))
            st.write('El precio medio para los pisos con orientación norte es de {} euros.'.format(desencodeado_valencia[desencodeado_valencia['Orientación'] == 'Norte']['Precio'].mean().astype(int)))
            st.write('El precio medio para los pisos con orientación este es de {} euros.'.format(desencodeado_valencia[desencodeado_valencia['Orientación'] == 'Este']['Precio'].mean().astype(int)))
            st.write('El precio medio para los pisos con orientación oeste es de {} euros.'.format(desencodeado_valencia[desencodeado_valencia['Orientación'] == 'Oeste']['Precio'].mean().astype(int)))    
        
        st.markdown("""**Conclusión**: Como se puede ver los pisos orientados al Oeste tienen una presencia mucho menor en los pisos anunciados a la venta en Idealista. Hay que tener en cuenta factores como que la orientación al oeste en la ciudad de Valencia implica en dirección opuesta al mar. Al ser una ciudad húmedad y con una temperatura media anual de 17,6 grados las viviendas con orientación oeste tienen una mayor temperatura, por lo tanto, mayor gasto en aire acondicionado o elementos para cubrir el sol.""")

        st.markdown("""
                    ### Presencia de garaje en las ofertas.
                    
                    Aparcar en la ciudad de Valencia puede resultar una tarea complicada debido a varios factores. En primer lugar, la ciudad cuenta con una gran cantidad de vehículos en circulación y una densidad de población relativamente alta, lo que se traduce en una gran demanda de espacios de estacionamiento. Además, el crecimiento urbano desordenado y la falta de planificación en la construcción de aparcamientos y la limitación de espacio en algunas zonas dificultan aún más la tarea. 
                    Por otro lado, existen varias zonas de estacionamiento regulado, lo que implica que es necesario pagar por aparcar en algunas calles y plazas de la ciudad. Todo esto hace que aparcar en la ciudad de Valencia sea una tarea que requiere paciencia, tiempo y en muchas ocasiones, un poco de suerte. 
                    
                    En consecuencia vamos a proceder a estudiar la presencia de viviendas anunciadas a la venta cuyos edificios tienen garaje.""")
        
        
        col1, col2 = st.columns(2)
        with col1:
            # Agrupamos los datos.
            garajes = desencodeado_valencia.groupby('Garaje')['Garaje'].count().reset_index(name='Cantidad')

            # Gráficamos.
            fig = px.bar(garajes, x="Garaje", y="Cantidad", color="Garaje",
                        color_discrete_map = {
                            'Si': 'blue',
                            'No': '#FF0000'
                        })
            fig.update_layout(title_text='Cantidad de anuncios publicados con y sin garaje.')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.write("""    """)
            st.write("""    """)
            st.write("""    """)
            st.markdown("""###### Porcentajes de inmuebles con garaje.""")
            st.write("""    """)
            
            # Agrupamos.
            garajes = desencodeado_valencia.groupby('Garaje')['Garaje'].count()
            total = desencodeado_valencia['Garaje'].count()

            # Calcular el porcentaje
            porcentajes_garaje = garajes.apply(lambda x: (x/total)*100).reset_index(name='Porcentaje')

            # Mostramos.
            st.write('El porcentaje de pisos a la venta en la ciudad de Valencia sin garaje es de {}%.'.format(round(porcentajes_garaje[porcentajes_garaje['Garaje'] == 'No']['Porcentaje'].values[0],2)))
            st.write("""    """)
            st.write('El porcentaje de pisos a la venta en la ciudad de Valencia con garaje es de {}%.'.format(round(porcentajes_garaje[porcentajes_garaje['Garaje'] == 'Si']['Porcentaje'].values[0],2)))
            st.write("""    """)
            st.markdown("""###### Precio medio de las plazas de garaje anunciadas.""")
            st.write("""    """)
            # Calcular el valor medio de la columna 'Precio_garaje'
            precio_garaje_medio = desencodeado_valencia[desencodeado_valencia['Precio_garaje'] > 1000]['Precio_garaje'].mean()

            # Imprimir el valor medio
            st.write('El precio medio para de las plazas de garaje en Valencia es de {} €'.format(precio_garaje_medio.astype(int)))
        
        st.markdown("""
                    ### Aire acondicionado en los inmuebles publicados.
                    
                    El clima en Valencia se caracteriza por veranos calurosos y secos, con temperaturas que pueden superar los 30 grados Celsius durante varios meses al año y una temperatura media anual de 17,6 grados como hemos comentado previamente. 
                    Esto hace que el aire acondicionado sea una necesidad en muchas viviendas, ya que permite mantener un ambiente fresco y confortable durante los meses más cálidos. 
                    Además, el uso del aire acondicionado puede ayudar a reducir el consumo de energía al evitar el uso de ventiladores eléctricos, que a menudo son menos eficientes y menos efectivos para mantener el hogar fresco. 
                    Por lo tanto, el aire acondicionado es considerado una característica importante en muchas viviendas en Valencia, y su presencia puede ser un factor determinante a la hora de decidir sobre la compra de una vivienda en la ciudad.""")
        
        col1, col2 = st.columns(2)
        with col1:
            # Agrupamos los datos.
            garajes = desencodeado_valencia.groupby('Aire_Acondicionado')['Aire_Acondicionado'].count().reset_index(name='Cantidad')

            # Gráficamos.
            fig = px.bar(garajes, x="Aire_Acondicionado", y="Cantidad", color="Aire_Acondicionado",
                        color_discrete_map = {
                            'Si': 'blue',
                            'No': '#FF0000'
                        })
            fig.update_layout(title_text='Cantidad de anuncios publicados con y sin aire acondicionado.')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Agrupamos.
            aires = desencodeado_valencia.groupby('Aire_Acondicionado')['Aire_Acondicionado'].count()
            total = desencodeado_valencia['Aire_Acondicionado'].count()

            # Calcular el porcentaje
            porcentajes_aire = aires.apply(lambda x: (x/total)*100).reset_index(name='Porcentaje')

            # Mostramos.
            st.write("""    """)
            st.write("""    """)
            st.write("""    """)
            st.write("""    """)
            st.write('El porcentaje de pisos a la venta en la ciudad de Valencia sin aire acondicionado es de {}%.'.format(round(porcentajes_aire[porcentajes_aire['Aire_Acondicionado'] == 'No']['Porcentaje'].values[0],2)))
            st.write("""    """)
            st.write('El porcentaje de pisos a la venta en la ciudad de Valencia con aire acondicionado es de {}%.'.format(round(porcentajes_aire[porcentajes_aire['Aire_Acondicionado'] == 'Si']['Porcentaje'].values[0],2)))
        
        st.markdown("""
                    ### Presencia de conserje en los inmuebles publicados.
                    
                    El papel del conserje en los edificios ha evolucionado con el tiempo y en la actualidad su presencia se justifica principalmente por cuestiones de seguridad y comodidad para los residentes. 
                    El conserje es una figura clave en el control de acceso al edificio, verificando la identidad de las personas que entran y salen, supervisando la seguridad del edificio y respondiendo a emergencias. 
                    Además, el conserje puede encargarse de tareas como la limpieza y el mantenimiento del edificio, lo que contribuye a mejorar la calidad de vida de los residentes y a mantener el buen estado del inmueble. 
                    En resumen, la figura del conserje sigue siendo importante en los edificios actuales, proporcionando un valor añadido a la comunidad de residentes.""")
        col1, col2 = st.columns(2)
        with col2:
            # Agrupamos.
            conserjes = desencodeado_valencia.groupby('Conserje')['Conserje'].count()
            total = desencodeado_valencia['Conserje'].count()

            # Calcular el porcentaje
            porcentajes_conserje = conserjes.apply(lambda x: (x/total)*100).reset_index(name='Porcentaje')

            # Mostramos.
            st.write("""    """)
            st.write("""    """)
            st.write("""    """)
            st.write("""    """)
            st.write("""    """)
            st.write('El porcentaje de pisos a la venta en la ciudad de Valencia sin conserje en el edificio es de {}%.'.format(round(porcentajes_conserje[porcentajes_conserje['Conserje'] == 'No']['Porcentaje'].values[0],2)))
            st.write("""    """)
            st.write('El porcentaje de pisos a la venta en la ciudad de Valencia con conserje en el edificio es de {}%.'.format(round(porcentajes_conserje[porcentajes_conserje['Conserje'] == 'Si']['Porcentaje'].values[0],2)))

        with col1:
            # Agrupamos los datos.
            conserje = desencodeado_valencia.groupby('Conserje')['Conserje'].count().reset_index(name='Cantidad')

            # Gráficamos.
            fig = px.bar(conserje, x="Conserje", y="Cantidad", color="Conserje",
                        color_discrete_map = {
                            'Si': 'blue',
                            'No': '#FF0000'
                        })
            fig.update_layout(title_text='Cantidad de anuncios publicados con y sin conserje.')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
                    ### Años de construcción de los inmuebles publicados en Valencia.
                    
                    A partir de la década de 1950, la construcción de inmuebles en la ciudad de Valencia experimentó un gran auge debido al crecimiento económico y demográfico que experimentó la ciudad en ese periodo. La ciudad comenzó a expandirse más allá de las murallas que la rodeaban, dando lugar a nuevos barrios y urbanizaciones. Se construyeron viviendas de diferentes tipos y tamaños para adaptarse a las necesidades de la población, desde bloques de pisos hasta chalets individuales. 
                    Además, se introdujeron nuevas técnicas y materiales de construcción que permitieron la edificación de edificios más altos y resistentes, lo que transformó el perfil urbano de la ciudad. 
                    Con el paso de los años, la construcción de inmuebles en Valencia ha seguido evolucionando para adaptarse a las necesidades cambiantes de la sociedad y para hacer frente a los desafíos medioambientales y de sostenibilidad que plantea la construcción en la actualidad.""")
        

        # Crear el histograma con la gama de colores personalizada
        fig = px.histogram(desencodeado_valencia[(desencodeado_valencia['Año_construcción']>1899) & (desencodeado_valencia['Año_construcción']<2019)], x = 'Año_construcción', title = 'Número de registros por año desde 1900 hasta 2018')
        fig.update_xaxes(title_text='Año de construcción')
        fig.update_yaxes(title_text='Cantidad')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            # Imprimir el resultado
            st.write('El número de viviendas construidas antes de 1900 fue de {} viviendas'.format(desencodeado_valencia[(desencodeado_valencia['Año_construcción'] < 1900)].shape[0]))
            st.write('El número de viviendas construidas entre 1900-1940 fue de {} viviendas'.format(desencodeado_valencia[(desencodeado_valencia['Año_construcción'] >= 1900) & (desencodeado_valencia['Año_construcción'] <= 1940)].shape[0]))
            st.write('El número de viviendas construidas entre 1941-1960 fue de {} viviendas'.format(desencodeado_valencia[(desencodeado_valencia['Año_construcción'] >= 1941) & (desencodeado_valencia['Año_construcción'] <= 1960)].shape[0]))
            
        with col2:
            st.write('El número de viviendas construidas entre 1961-1980 fue de {} viviendas'.format(desencodeado_valencia[(desencodeado_valencia['Año_construcción'] >= 1961) & (desencodeado_valencia['Año_construcción'] <= 1980)].shape[0]))
            st.write('El número de viviendas construidas entre 1981-2000 fue de {} viviendas'.format(desencodeado_valencia[(desencodeado_valencia['Año_construcción'] >= 1981) & (desencodeado_valencia['Año_construcción'] <= 2000)].shape[0]))
            st.write('El número de viviendas construidas entre 2001-2018 fue de {} viviendas'.format(desencodeado_valencia[(desencodeado_valencia['Año_construcción'] >= 2001) & (desencodeado_valencia['Año_construcción'] <= 2018)].shape[0]))
        
        st.markdown("""**¿Qué nos indica esto?**""") 
                    
        st.markdown("""Nos indica que es una ciudad envejecida en cuanto a la antigüedad de los edificios y es que entorno al 47% de las viviendas en la ciudad de Valencia fueron construidas entre los años 1961-1980. Esto es importante tenerlo en cuenta puesto que aquellas de mayor antigüedad que no han tenido una reforma integral, necesitarán de arreglos que pueden aumentar el coste de nuestra vivienda.
Adicionalmente y como factor a tener en cuenta de cara a adquirir una vivienda en Valencia, las Inspecciones Técnicas de los Edificios (ITE), tienen como obligatoriedad pasarse a los 50 años de su construcción. A partir de los 50 años se deberá pasar cada 10 años. """)
        
        st.markdown("""
                    ### ¿Cómo influye la distancia al centro en los inmuebles publicados en Valencia?
                    La relación entre la distancia al centro de la ciudad y el precio de un inmueble es un tema que ha sido ampliamente estudiado en el mercado inmobiliario. En el caso de Valencia, esta relación también ha sido objeto de análisis, y es un factor que los compradores y vendedores de propiedades en la ciudad deben tener en cuenta al tomar decisiones importantes. La ubicación de una propiedad es un factor clave en la determinación de su precio, y la distancia al centro de la ciudad es uno de los principales determinantes de la accesibilidad y conveniencia de una propiedad en Valencia. 
                    En este contexto, explorar la relación entre la distancia al centro y el precio de las propiedades en Valencia puede proporcionar una visión valiosa para aquellos que buscan comprar o vender una propiedad en la ciudad.""")
        
        fig = px.scatter(desencodeado_valencia, x = 'Distancia_centro', y = 'Precio', title = 'Relación entre distancia al centro y precio')
        fig.update_xaxes(title_text='Distancia al centro (km)')
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.markdown("""
                    ### ¿Cómo varia el precio de la vivienda según el barrio donde se encuentre?
                    El precio de la vivienda es uno de los indicadores más importantes de la economía y calidad de vida de una ciudad. En el caso de Valencia, conocer el precio medio de las viviendas por barrio puede ser de gran utilidad para los compradores y vendedores de propiedades, así como para los inversores y los planificadores urbanos. 
                    El análisis de los precios de la vivienda por barrio puede proporcionar información valiosa sobre la demanda y la oferta de viviendas, así como sobre las tendencias de los precios a lo largo del tiempo. Además, esta información puede ser útil para identificar las áreas más atractivas para la inversión en bienes raíces y para planificar el desarrollo urbano y la política de vivienda.""")
        
        # Cargamos el dataset.
        valencia = pd.read_csv("data/valencia_barrio_municipio.csv")
        valencia.drop('Unnamed: 0', axis =1, inplace=True)
        valencia.drop('ID', axis =1, inplace=True)
        valencia.drop('Municipio', axis=1, inplace=True)
        
        
        # Contar el número de viviendas por barrio
        num_viviendas = valencia.groupby('Barrio')['Precio'].count()

        # Seleccionar los barrios que tienen al menos 10 viviendas
        barrios = num_viviendas[num_viviendas >= 50].index

        # Filtrar el DataFrame por los barrios seleccionados
        valencia_filtrado = valencia[valencia['Barrio'].isin(barrios)]

        # Agrupar los datos por barrio y calcular la media del precio
        precio_medio = valencia_filtrado.groupby('Barrio')['Precio'].mean().sort_values(ascending=False).reset_index()

        # Graficar los datos con Plotly Express
        fig = px.bar(precio_medio, x='Barrio', y='Precio', title='Precio medio por barrio con al menos 50 viviendas anunciadas', 
                    labels={'Barrio': 'Barrio', 'Precio': 'Precio medio'}, 
                    color='Barrio', color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(xaxis_tickangle=-90)

        # Mostrar el gráfico usando Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        
        st.markdown("""
                    #### Potenciales transacciones de la plataforma""")
        
        col1, col2 = st.columns(2)
        
        with col1:    
            top_3 = valencia.groupby('Barrio')['Precio'].sum().sort_values(ascending=False)[:3]
            top_3_names = list(top_3.index)

            top_3_counts = valencia['Barrio'].value_counts()[top_3_names]

            st.write("Los barrios que más ingresos supondrían son:")
            with st.container():
                st.write('1. ' + top_3_names[0] + ' con unos posibles ingresos respectivos de ' + str(int(top_3[0])) + ' € teniendo ' + str(top_3_counts[0]) + ' anuncios publicados.')
                st.write('2. ' + top_3_names[1] + ' con unos posibles ingresos respectivos de ' + str(int(top_3[1])) + ' € teniendo ' + str(top_3_counts[1]) + ' anuncios publicados.')
                st.write('3. ' + top_3_names[2] + ' con unos posibles ingresos respectivos de ' + str(int(top_3[2])) + ' € teniendo ' + str(top_3_counts[2]) + ' anuncios publicados.')

        with col2:
            last_3 = valencia.groupby('Barrio')['Precio'].sum().sort_values(ascending=True)[:3]
            last_3_names = list(last_3.index)

            last_3_counts = valencia['Barrio'].value_counts()[last_3_names]

            st.write("Los barrios que menos ingresos supondrían son:")
            with st.container():
                st.write('1. ' + last_3_names[0] + ' con unos posibles ingresos respectivos de ' + str(int(last_3[0])) + ' € teniendo ' + str(last_3_counts[0]) + ' anuncios publicados.')
                st.write('2. ' + last_3_names[1] + ' con unos posibles ingresos respectivos de ' + str(int(last_3[1])) + ' € teniendo ' + str(last_3_counts[1]) + ' anuncios publicados.')
                st.write('3. ' + last_3_names[2] + ' con unos posibles ingresos respectivos de ' + str(int(last_3[2])) + ' € teniendo ' + str(last_3_counts[2]) + ' anuncios publicados.')
        
        st.markdown("""
                    #### Diferenciación por metros construidos
                     
                    El estudio de los metros construidos de las viviendas por barrios es relevante ya que permite tener una visión más completa del mercado inmobiliario de una determinada zona. 
                    Saber cuántos metros construidos tienen las viviendas en un barrio determinado puede ayudar a determinar su nivel socioeconómico, la calidad de vida de sus habitantes y el tipo de inmuebles que predominan en la zona. 
                    Además, esta información es importante para compradores y vendedores de viviendas, ya que el tamaño de la propiedad es uno de los factores clave que influyen en su valor. 
                    Conocer los metros construidos promedio por barrio puede ser muy útil para determinar el precio adecuado de una propiedad en venta o para valorar si un inmueble en particular tiene un precio justo.""")
        
        # Agrupar los datos por barrio y calcular la media de los metros construidos
        metros_medios = valencia.groupby('Barrio')['Metros_Construidos'].mean().sort_values(ascending=False).reset_index()

        # Graficar los datos con Plotly Express
        fig = px.bar(metros_medios, x='Barrio', y='Metros_Construidos', title='Metros construidos medios por barrio', 
                    labels={'Barrio': 'Barrio', 'Metros_Construidos': 'Metros construidos medios'}, 
                    color='Barrio', color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(xaxis_tickangle=-90)

        # Mostrar el gráfico usando Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""###### Medias de metros cuadrados construidos de los barrios que más ingresos potenciales representan""")
        
        col1, col2 = st.columns(2)
        with col1:
            # Obtener los datos de los top 3 barrios
            top_3_barrios = list(valencia.groupby('Barrio')['Precio'].sum().sort_values(ascending=False)[:3].index)

            # Filtrar el DataFrame para incluir solo los datos de los top 3 barrios
            valencia_top_3 = valencia[valencia['Barrio'].isin(top_3_barrios)]

            # Calcular la media de los metros construidos para los top 3 barrios
            metros_construidos_top_3 = valencia_top_3.groupby('Barrio')['Metros_Construidos'].mean()

            # Imprimir los resultados
            st.write("**Metros construidos medios para los tres barrios que más ingresos supondrían:**")
            for barrio, metros in metros_construidos_top_3.items():
                st.write(f"{barrio}: {round(metros, 2)} metros cuadrados")
                
        with col2:
            # Obtener los datos de los últimos 3 barrios
            ultimos_3_barrios = list(valencia.groupby('Barrio')['Precio'].sum().sort_values(ascending=True)[:3].index)

            # Filtrar el DataFrame para incluir solo los datos de los últimos 3 barrios
            valencia_ultimos_3 = valencia[valencia['Barrio'].isin(ultimos_3_barrios)]

            # Calcular la media de los metros construidos para los últimos 3 barrios
            metros_construidos_ultimos_3 = valencia_ultimos_3.groupby('Barrio')['Metros_Construidos'].mean()

            # Imprimir los resultados
            st.write("**Metros construidos medios para los tres barrios que menos ingresos potenciales representan**:")
            for barrio, metros in metros_construidos_ultimos_3.items():
                st.write(f"{barrio}: {round(metros, 2)} metros cuadrados")
       
        # Filtrar los datos para incluir solo los valores posteriores a 1899
        valencia_filtered = valencia[valencia['Año_construcción'] > 1899]

        # Crear el gráfico de dispersión
        fig = px.scatter(valencia_filtered, x='Año_construcción', y='Metros_Construidos', color='Barrio', hover_name='Barrio', 
                        title='Relación entre año de construcción y superficie de las viviendas en Valencia')
        fig.update_layout(xaxis_title='Año de construcción',
                        yaxis_title='Metros construidos')
        st.plotly_chart(fig, use_container_width=True)

        
        # Filtrar los datos para incluir solo los años superiores a 1900
        valencia_filtered = valencia[valencia['Año_construcción'] > 1890]

        # Agrupar los datos por año de construcción y calcular la media de metros construidos
        metros_construidos_por_año = valencia_filtered.groupby('Año_construcción')['Metros_Construidos'].mean().reset_index()

        # Crear la gráfica lineal
        fig = px.line(metros_construidos_por_año, x='Año_construcción', y='Metros_Construidos')

        # Añadir etiquetas y título
        fig.update_layout(title='Media de metros construidos por año de construcción (superior a 1900)',
                        xaxis_title='Año de construcción',
                        yaxis_title='Metros construidos medios')

        # Mostrar la gráfica
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            # Calcular el año de construcción medio para los 3 barrios con mayor suma de precios
            top_3_año = valencia[valencia['Barrio'].isin(top_3_names)].groupby('Barrio')['Año_construcción'].mean()
            st.write("**El año de construcción medio para los 3 barrios con mayor suma de precios son:**")
            
            for i in range(len(top_3_names)):
                st.write(f"{top_3_names[i]} con un año de construcción medio de {int(top_3_año[top_3_names[i]])}.")
        with col2:
            # Obtener los nombres de los 3 barrios con menor suma de precios
            bottom_3_names = list(valencia.groupby('Barrio')['Precio'].sum().sort_values()[:3].index)

            # Calcular el año de construcción medio para los 3 barrios con menor suma de precios
            bottom_3_año = valencia[valencia['Barrio'].isin(bottom_3_names)].groupby('Barrio')['Año_construcción'].mean()

            # Imprimir el resultado subrayado
            st.markdown("**El año de construcción medio para los 3 barrios con menor suma de precios son:**")
            for i in range(len(bottom_3_names)):
                st.write(f"{bottom_3_names[i]} con un año de construcción medio de {int(bottom_3_año[bottom_3_names[i]])}.")

        st.markdown("""
                    #### Diferenciación por altura de los edificios.
                    
                    
                    La altura de los edificios es un factor importante a considerar al decidir comprar una vivienda en la ciudad de Valencia. 
                    Por un lado, los edificios más altos suelen tener vistas panorámicas de la ciudad y, por lo tanto, ofrecen un atractivo valor añadido a la propiedad. 
                    Además, la altura del edificio puede influir en la cantidad de luz natural que recibe la vivienda, ya que los pisos más altos tienen más probabilidades de recibir más luz solar. 
                    Por otro lado, hay que tener en cuenta que los edificios altos también pueden ser más susceptibles a problemas de ruido, viento y vibración debido a la exposición a factores externos como el clima y la ubicación de la propiedad. 
                    En resumen, la altura de los edificios es un factor importante a considerar en la compra de una vivienda, ya que puede afectar tanto a la calidad de vida como al valor de la propiedad.""")

        # Obtener la media de Plantas_máximas por barrio
        plantas_maximas = valencia.groupby('Barrio')['Plantas_máximas'].mean()

        # Resetear el índice del dataframe
        plantas_maximas = plantas_maximas.reset_index()

        # Ordenar los datos de manera descendente
        plantas_maximas = plantas_maximas.sort_values(by='Plantas_máximas', ascending=False)

        # Crear la gráfica con Plotly Express
        fig = px.bar(plantas_maximas, x='Barrio', y='Plantas_máximas', color='Barrio',
                    title='Media de plantas máximas por barrio')
        fig.update_layout(xaxis_title='Barrio', yaxis_title='Media de plantas máximas')
        
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""La altura máxima de un edificio puede tener un impacto significativo en la calidad de vida y en la percepción de valor de una propiedad. 
                    Por un lado, los edificios más altos pueden proporcionar vistas panorámicas impresionantes y una sensación de amplitud. 
                    Además, pueden ofrecer un mayor aislamiento acústico y térmico, ya que se encuentran más alejados del nivel de la calle. 
                    Sin embargo, también pueden generar sombras que afectan la cantidad de luz natural que llega a las propiedades circundantes y pueden incrementar la densidad poblacional de un barrio, generando problemas de tráfico y accesibilidad. 
                    Por lo tanto, es importante evaluar cuidadosamente los pros y los contras de la altura máxima de un edificio al tomar una decisión de compra de una propiedad.""")
        
        
        st.markdown("""
                    #### Relevancia de la distancia al centro de la ciudad de las viviendas.
                    
                    
                    La distancia al centro de la ciudad es una variable clave a tener en cuenta al comprar una vivienda en Valencia. Los precios de las viviendas varían significativamente en función de la distancia al centro de la ciudad, siendo más elevados los precios de las viviendas ubicadas en el corazón de la ciudad y disminuyendo a medida que nos alejamos del centro. 
                    Además, la distancia al centro también influye en la calidad de vida, ya que los residentes más cercanos al centro tienen un mayor acceso a la oferta cultural, gastronómica y de ocio de la ciudad. 
                    Por otro lado, también es importante tener en cuenta la accesibilidad al transporte público, ya que la distancia al centro puede ser menos relevante si se dispone de buenas conexiones de transporte. 
                    En resumen, la distancia al centro de la ciudad es una variable importante a considerar al comprar una vivienda en Valencia, tanto por su impacto en el precio como por su influencia en la calidad de vida de los residentes.""")
        
        fig = px.scatter(valencia, x="Distancia_centro", y="Preciom2", size="Metros_Construidos", 
                 hover_name="Barrio", color="Barrio")

        fig.update_layout(title="Relación del precio del metro cuadrado respecto a la distancia al centro",
                        xaxis_title="Distancia al centro (km)",
                        yaxis_title="Precio por metro cuadrado (€/m²)")

        st.plotly_chart(fig, use_container_width=True)
        
        # Mapa de densidad precio m2 y distancia centro.
        fig = px.density_contour(valencia, x="Distancia_centro", y="Precio", 
                nbinsx=40, nbinsy=40)
        fig.update_layout(title="Densidad de puntos del precio y la distancia al centro", xaxis_title="Distancia al centro (km)", yaxis_title="Precio")
        
        st.plotly_chart(fig, use_container_width=True)
                
        st.markdown("""Como podemos observar existe una relación determinante entre el precio del metro cuadrado en la ciudad de Valencia y la distancia de la vivienda al centro de la ciudad.
                    Esto es algo bastante común en la mayoría de grandes ciudades y es algo que tanto como compradores o vendedores debemos tener en cuenta.
                    Para poder visualizarlo mejor vamos a ver a continuación el precio medio de las viviendas anunciadas respecto a la distancia del centro de la ciudad.""")

        # Scatter precio medio y distancia al centro.
        # Agrupar los datos por barrio y calcular la media del precio y la distancia al centro
        precio_medio = valencia.groupby('Barrio')['Precio'].mean()
        distancia_centro_medio = valencia.groupby('Barrio')['Distancia_centro'].mean()

        # Crear un DataFrame con los datos de interés
        df = pd.DataFrame({'Barrio': precio_medio.index,
                        'Precio medio': precio_medio.values,
                        'Distancia al centro media': distancia_centro_medio.values})

        # Crear el gráfico
        fig = px.scatter(df, x='Distancia al centro media', y='Precio medio', color='Barrio',
                        title='Relación entre el precio medio y la distancia al centro por barrio',
                        labels={'Distancia al centro media': 'Distancia al centro media (km)',
                                'Precio medio': 'Precio medio (€)'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""#### Visualización a través de mapas.""")
        
        st.markdown("""En el siguien mapa interactivo de la ciudad de Valencia con marcadores de puntos en función de las coordenadas, 
                    cada punto representa una vivienda y su tamaño está en relación con la cantidad de metros construidos. 
                    El color de los puntos está determinado por el precio de la vivienda en euros por metro cuadrado, siendo los colores más oscuros indicativos de precios más altos y los colores más claros indicativos de precios más bajos.""")
        
        col1, col2 = st.columns(2)
        with col1:
            # Mapa de calor
            mapa = px.scatter_mapbox(valencia, lat="Latitud", lon="Longitud", color="Precio",
                            size="Metros_Construidos", zoom=11,
                            mapbox_style="carto-positron", color_continuous_scale="YlOrRd")
            mapa.update_layout(title="Mapa de calor de los precios de las viviendas en Valencia.")
            st.plotly_chart(mapa, use_container_width=True)
        
        with col2:
            # Mapa de calor, barrios delimitados.
            # Cargar archivo geojson como una cadena de texto en formato JSON
            with open('data/neighbourhoods.geojson') as f:
                geojson_str = json.load(f)

            # Crear mapa de cloropletas
            mapa_barrios = px.choropleth_mapbox(valencia, 
                                    geojson=geojson_str, # Usar cadena de texto como geojson
                                    color="Precio",
                                    locations="Barrio",
                                    featureidkey="properties.neighbourhood",
                                    center={"lat": 39.46975, "lon": -0.37739},
                                    mapbox_style="carto-positron",
                                    zoom=11, color_continuous_scale="YlOrRd")
            mapa_barrios.update_layout(title="Mapa de calor de los precios medios por barrios.")
            
            # Mostrar mapa
            st.plotly_chart(mapa_barrios, use_container_width=True)
        
        
        # Mapa años de construcción.

        # Cargar archivo geojson como una cadena de texto en formato JSON
        with open('data/neighbourhoods.geojson') as f:
            geojson_str = json.load(f)

        # Filtrar datos de Valencia para incluir solo los registros con Año_construcción superior a 1899
        valencia_filtered = valencia[valencia['Año_construcción'] > 1899]

        # Crear mapa de cloropletas
        mapa_barrios = px.choropleth_mapbox(valencia_filtered, 
                                geojson=geojson_str, # Usar cadena de texto como geojson
                                color="Año_construcción",
                                locations="Barrio",
                                featureidkey="properties.neighbourhood",
                                center={"lat": 39.46975, "lon": -0.37739},
                                mapbox_style="carto-positron",
                                zoom=10, color_continuous_scale="YlOrRd")

        
        mapa_barrios.update_layout(title="Mapa de calor de los precios medios por barrios.")

        # Mostrar mapa
        st.plotly_chart(mapa_barrios, use_container_width=True)
        
        
        