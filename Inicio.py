#--------------------LIBRERÍAS--------------------#
import streamlit as st 
import seaborn as sns
sns.set()
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Webscrapping
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Los warnings
import warnings
warnings.filterwarnings('ignore')

from streamlit_extras.badges import badge


#--------------------CONFIGURACIÓN DE LA PÁGINA----------------------------#
st.set_page_config(page_title="Valencia", layout="wide", page_icon="🏘️")
st.set_option('deprecation.showPyplotGlobalUse', False)

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

st.caption('Pedro Llamas López')
badge(type="github", name="pedrollamas")

st.title("""Análisis del sector inmobiliario en la ciudad de Valencia""")
st.video("img/190815_01_UHD_19_preview.mp4")


col1, col2 = st.columns(2)
with col1:
    st.header("Objetivo del proyecto")
    st.markdown("""Este proyecto tiene como objetivo ofrecer una visión detallada  del mercado de la vivienda en la ciudad de Valencia, explorando los factores que influyen en la fluctuación de los precios.

A lo largo de esta app, podrás encontrar información sobre como afectan las distintas variables al precio, el precio medio por metro cuadrado en diferentes zonas de la ciudad, y cómo se relacionan los precios con variables como el tamaño de la vivienda, la antigüedad del edificio, y otras muchas.

Esperamos que este análisis sea de utilidad tanto para aquellos que buscan comprar o vender una propiedad en Valencia, como para aquellos interesados en conocer más sobre el mercado inmobiliario en esta ciudad.


En este proyecto, he desarrollado un predictor de precios de viviendas en la ciudad de Valencia a través del entrenamiento de un modelo de Machine Learning con diferentes variables. Este predictor permite obtener una estimación del precio de una vivienda en función de su ubicación, tamaño, características y otros factores relevantes en el mercado inmobiliario. 

Adicionalmente, también he creado un simulador de hipotecas que permite a los usuarios estimar la cuota mensual de su hipoteca en función de la cantidad prestada, la tasa de interés y otros parámetros. 

Con estos recursos, se busca facilitar la toma de decisiones a la hora de comprar o vender una propiedad en Valencia.""")

with col2:
    st.image("img/Valencia.jpg")
    

col1, col2 = st.columns(2)
with col2:
    st.markdown(""" """)
    st.markdown(""" """)
    st.markdown(""" """)
    st.markdown(""" """)
    st.markdown("""El sector inmobiliario valenciano es un área clave en la economía de la región. El mercado inmobiliario de Valencia ha experimentado un crecimiento significativo en los últimos años, con una gran cantidad de inversores nacionales e internacionales que buscan oportunidades en la zona. Por lo tanto, es importante analizar el mercado inmobiliario valenciano para entender las tendencias y oportunidades en el sector, y para ayudar a los compradores y vendedores a tomar decisiones informadas y rentables. Además, el análisis del sector inmobiliario también es fundamental para las políticas de planificación urbana y la toma de decisiones por parte de las autoridades gubernamentales en relación a la gestión de los recursos y la planificación del desarrollo urbano.""")
    st.image("img/noticia2.jpg")
    st.markdown('[La inversión inmobiliaria en el sur de Europa bate récord con 31.700 millones](https://valenciaplaza.com/inversion-inmobiliaria-sur-europa-bate-record-31700-millones.html)')
    st.markdown(""" """)
    st.markdown(""" """)
    st.image('img/noticia4.jpg')
    st.markdown('[El mercado inmobiliario de Valencia es el más atractivo entre las principales capitales españolas](https://www.abc.es/espana/comunidad-valenciana/mercado-inmobiliario-valencia-atractivo-principales-capitales-espanolas-20230413200203-nt.html?ref=https%3A%2F%2Fwww.abc.es%2Fespana%2Fcomunidad-valenciana%2Fmercado-inmobiliario-valencia-atractivo-principales-capitales-espanolas-20230413200203-nt.html)')
    st.image('img/noticia6.jpg')
    st.markdown('[Tres de cada diez viviendas vendidas en Valencia son para inversión](https://www.eleconomista.es/vivienda-inmobiliario/noticias/12020979/11/22/Tres-de-cada-diez-viviendas-vendidas-en-Valencia-son-para-inversion.html)')
    
    
with col1:
    st.header("Noticias al respecto")
    # Noticias relevantes
    url = 'https://www.levante-emv.com/economia/2022/12/28/valencia-ciudad-espanola-rentable-invertir-vivienda-76874501.html'

    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    # Busca la etiqueta de la carátula
    caratula = soup.find('meta', property='og:image')

    # Obtiene la URL de la imagen
    imagen_url = caratula['content']

    # Muestra la imagen en Streamlit
    st.image(imagen_url)

    st.markdown('[Valencia, la ciudad española más rentable para invertir en vivienda](https://www.levante-emv.com/economia/2022/12/28/valencia-ciudad-espanola-rentable-invertir-vivienda-76874501.html)')
    st.markdown(""" """)
    st.markdown(""" """)
    st.markdown(""" """)
    st.markdown(""" """)
    st.image('img/noticia3.jpg')
    st.markdown("[What Makes This Stunning City So Popular For Luxury Lovers Seeking A New Life](https://www.luxurylifestylemag.co.uk/property/viva-valencia-what-makes-this-stunning-city-so-popular-for-luxury-lovers-seeking-a-new-life/.html)")
    st.image('img/noticia5.jpg')
    st.markdown('[El precio de la vivienda sube un 7,6% en València en 2022 y la ciudad se sitúa como el "mercado más atractivo"](https://cadenaser.com/comunitat-valenciana/2023/04/13/el-precio-de-la-vivienda-sube-un-76-en-valencia-en-2022-y-la-ciudad-se-situa-como-el-mercado-mas-atractivo-radio-valencia/)')
