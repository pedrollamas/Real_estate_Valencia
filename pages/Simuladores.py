#--------------------LIBRERÍAS--------------------#
import streamlit as st 
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Mapas interactivos
from streamlit_option_menu import option_menu

# Gráficos de plotly
from plotly.offline import iplot, init_notebook_mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)

# Para el predictor
from pycaret.regression import *
import pyperclip

# Los warnings
import warnings
warnings.filterwarnings('ignore')
clf = setup(data, target='target', silent=True, experiment_name='/tmp/pycaret_experiment')


#--------------------CONFIGURACIÓN DE LA PÁGINA----------------------------#
st.set_page_config(page_title="Predictor", layout="wide", page_icon="🎯")

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

selected = option_menu("Predictors", ["Estimar el precio", 'Simulador hipoteca'],icons=['currency-exchange', 'piggy-bank'], menu_icon="bullseye", default_index=1)



# Defino el dataframe para poder rellenar los valores fijos que no queremos que los usuarios pongan.
valencia = pd.read_csv('data/streamlit_coded_valencia.csv')
valencia.drop('Unnamed: 0', axis=1, inplace=True)

if selected == 'Estimar el precio':
    # Crear contenedor principal
    container = st.container()

    with container:
        st.markdown(
            """
            <div style='background-color: #2AB09C; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); margin-top: 20px; margin-left: auto; margin-right: auto; width: 60%;'>
                <div style='font-size: 30px; font-weight: 700; margin-bottom: 20px; color: #ffffff;'>Bienvenido al predictor de precios de viviendas en Valencia</div>
                <div style='font-size: 20px; margin-bottom: 20px; color: #ffffff;'>Introduzca los detalles de la vivienda que le interesa y obtenga una estimación del precio.</div>
                <div style='font-size: 20px; margin-bottom: 20px; color: #ffffff;'>Puede ajustar los siguientes parámetros:</div>
                <ul style='text-align: left; font-size: 16px; color: #ffffff;'>
                    <li>Metros cuadrados de la vivienda</li>
                    <li>Número de habitaciones y baños</li>
                    <li>Presencia de terraza, ascensor, aire acondicionado, garaje.</li>
                    <li>Puede indicar trastero, armarios, piscina, conserje, jardín, dúplex y ático</li>
                    <li>Orientación de la vivienda</li>
                    <li>Año de construcción del edificio</li>
                    <li>Altura máxima del edificio y número de viviendas en el edificio</li>
                    <li>Distancia al centro de Valencia y al metro</li>
                    <li>Barrio</li>
                </ul>
                <div style='font-size: 20px; margin-bottom: 20px; color: #ffffff;'>Haga click en el botón 'Estimar precio' de la barra lateral.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Defino el estilo de los sliders.
    st.markdown('<style>div[role="slider"] .stSlider {background-color: #2AB09C !important;}</style>', unsafe_allow_html=True)


    # Vamos a generar los selectores de variables.

    st.sidebar.markdown("<h1 style='font-family: Verdana; font-weight: bold;'>Indica las características de la vivienda</h1>", unsafe_allow_html=True)

    Metros_Construidos = st.sidebar.slider('Metros cuadrados', 50, 400)
    Habitaciones = st.sidebar.slider('Habitaciones', 1, 16)
    Baños = st.sidebar.slider('Baños', 1, 12)
    Terraza = st.sidebar.selectbox('Terraza', ['No', 'Si'])
    Garaje = st.sidebar.selectbox('Garaje', ['No', 'Si'])
    orientacion = st.sidebar.selectbox('Orientación de la vivienda', ['Norte', 'Sur', 'Este', 'Oeste'])
    Conserje = st.sidebar.selectbox('Conserje', ['No', 'Si'])
    Ático = st.sidebar.selectbox('¿Se trata de un ático?', ['No', 'Si'])
    Año_construcción = st.sidebar.slider('Año de construcción del edificio', 1890, 2021)
    Distancia_centro = st.sidebar.slider('Distancia al centro de Valencia (km)', 0.0, 6.0, format="%.3f")
    Distancia_metro = st.sidebar.slider('Distancia al metro (km)', 0.0, 3.0, format="%.3f")

    # Creo una lista de los barrios.
    barrios = ['AIORA', 'ALBORS', 'ARRANCAPINS', 'BENICALAP', 'BENIFERRI', 'BENIMACLET',
            'BENIMAMET', 'BETERO', 'CABANYAL-CANYAMELAR', 'CAMI DE VERA', 'CAMI FONDO',
            'CAMI REAL', 'CAMPANAR', 'CIUTAT DE LES ARTS I DE LES CIENCIES',
            'CIUTAT FALLERA', 'CIUTAT JARDI', 'CIUTAT UNIVERSITARIA', 'EL BOTANIC',
            'EL CALVARI', 'EL CARME', 'EL GRAU', 'EL MERCAT', 'EL PILAR',
            'EL PLA DEL REMEI', 'ELS ORRIOLS', 'EN CORTS', 'EXPOSICIO', 'FAVARA',
            'JAUME ROIG', "L'AMISTAT", "L'HORT DE SENABRE", "L'ILLA PERDUDA",
            'LA CARRASCA', 'LA CREU COBERTA', 'LA CREU DEL GRAU', 'LA FONTETA S.LLUIS',
            'LA FONTSANTA', 'LA GRAN VIA', 'LA LLUM', 'LA MALVA-ROSA', 'LA PETXINA',
            'LA PUNTA', 'LA RAIOSA', 'LA ROQUETA', 'LA SEU', 'LA VEGA BAIXA', 'LA XEREA',
            'LES TENDETES', 'MALILLA', 'MARXALENES', 'MESTALLA', 'MONT-OLIVET', 'MORVEDRE',
            'NA ROVELLA', 'NATZARET', 'NOU MOLES', 'PATRAIX', 'PENYA-ROJA', 'POBLE NOU',
            'RUSSAFA', 'SAFRANAR', 'SANT ANTONI', 'SANT FRANCESC', 'SANT ISIDRE',
            'SANT LLORENS', 'SANT MARCEL.LI', 'SANT PAU', 'SOTERNES', 'TORMOS',
            'TORREFIEL', 'TRES FORQUES', 'TRINITAT', 'VARA DE QUART']
    # Creo el selectbox desde la lista.
    Barrio = st.sidebar.selectbox('Barrio', barrios)

    # Diccionario con el valor correspondiente para cada barrio
    valores_barrios = {Barrio: valor for valor, Barrio in enumerate(barrios)}

    # Filtrar el DataFrame por el barrio seleccionado
    barrio_df = valencia[valencia['Barrio'] == Barrio]

        
    # Convertir los valores de entrada para predecir el modelo
    Terraza = 1 if Terraza == 'Si' else 0
    if orientacion == 'Norte':
        Orientación_norte = 1
        Orientación_sur = 0
        Orientación_este = 0
        Orientación_oeste = 0
    elif orientacion == 'Sur':
        Orientación_norte = 0
        Orientación_sur = 1
        Orientación_este = 0
        Orientación_oeste = 0
    elif orientacion == 'Este':
        Orientación_norte = 0
        Orientación_sur = 0
        Orientación_este = 1
        Orientación_oeste = 0
    else:
        Orientación_norte = 0
        Orientación_sur = 0
        Orientación_este = 0
        Orientación_oeste = 1

    Garaje = 1 if Garaje == 'Si' else 0
    Conserje = 1 if Conserje == 'Si' else 0
    Ático = 1 if Ático == 'Si' else 0

    # Asigno el valor correspondiente al barrio seleccionado para el modelo.
    valor_barrio = valores_barrios.get(Barrio, None)
    if valor_barrio is not None:
        Barrio = float(valor_barrio)
    else:
        Barrio = None
        
    # Cargar el modelo.
    model = load_model('data/streamlit_modelo_copia')

    # Da igual el precio que le demos porque lo sustituirá, pero le damos uno para que tenga la misma estructura que como fue entrenado.
    precio = 120000

    # Convertir los valores de entrada en un formato adecuado.
    X_new = [[precio,Metros_Construidos, Habitaciones, Baños, Terraza, Garaje, Orientación_norte, Orientación_sur, Orientación_este, Orientación_oeste,
            Conserje,Ático, Año_construcción, Distancia_centro, Distancia_metro, Barrio]]


    # Crear el diccionario de características.
    features_dict = {}
    for i, feature_name in enumerate(valencia.columns[1:]):
        features_dict[feature_name] = X_new[0][i]

    # Crear un nuevo dataframe con las características.
    X_new_df = pd.DataFrame(features_dict, index=[0])

    
    if st.sidebar.button('Estimar precio'):
            # Hacer la predicción con el modelo.
            predicted_price = model.predict(X_new_df)[0]
            # Formatear el precio predicho.
            precio_formateado = f'{round(round(predicted_price),2):,} €'
            # Mostrar el precio predicho.
            st.markdown(
                f"""
                <div style="
                    background-color: #2AB09C;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
                    margin-top: 20px;
                    margin-left: auto;
                    margin-right: auto;
                    width: 60%;
                ">
                    <div style="font-size: 30px; font-weight: 700; margin-bottom: 20px; color: #ffffff;">El precio estimado de la vivienda es:</div>
                    <div style="font-size: 80px; font-weight: 700; color: #ffffff;">{precio_formateado}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Calculadora de hipoteca.
            container_style = """
                background-color: #2AB09C;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
                margin-top: 20px;
                margin-left: auto;
                margin-right: auto;
                width: 60%;
            """

            st.markdown(
                f"""
                <div style="{container_style}">
                    <div style="font-size: 30px; font-weight: 700; margin-bottom: 20px; color: #ffffff;">Si desea calcular la cuota de hipoteca que le supondría, copie el precio y entre en el simulador de hipoteca.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    predicted_price = model.predict(X_new_df)[0]        
    # Crear un botón para que copie el precio.
    if st.button("Copiar resultado"):
        # Copiamos el valor de predicted_price al portapapeles del usuario
        pyperclip.copy(predicted_price)
        # Mostramos un mensaje de confirmación
        st.success("¡Valor copiado al portapapeles!")
            
if selected == 'Simulador hipoteca':
    container = st.container()
    # Meto el simulador de hipotecas.
    with container:
        st.markdown(
            """
            <div style='background-color: #2AB09C; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); margin-top: 20px; margin-left: auto; margin-right: auto; width: 60%;'>
                <div style='font-size: 30px; font-weight: 700; margin-bottom: 20px; color: #ffffff;'>Simulador de hipotecas</div>
                <div style='font-size: 20px; margin-bottom: 20px; color: #ffffff;'>Modifique los parámetros para obtener la cuota mensual de su hipoteca.</div>
                <div style='font-size: 20px;text-align: left; margin-bottom: 20px; color: #ffffff;'>Puede ajustar los siguientes parámetros:</div>
                <ul style='text-align: left; font-size: 16px; color: #ffffff;'>
                    <li>Número de años que quiere solicitar la hipoteca.</li>
                    <li>Ingresos mensuales netos.</li>
                    <li>Ahorro que aporta.</li>
                </ul>
                <div style='font-size: 20px; margin-bottom: 20px; color: #ffffff;'>Haga click en el botón 'Calcular hipoteca'.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns(3)
    with col2:
        
        # Agregar estilo CSS a la columna col2.
        col2.markdown(
            f"""
            <style>
                .css-1pahdxg {{
                    background-color: #2AB09C;
                    color: white;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
        # Le pedimos al usuario que introduzca el precio.      
        predicted_price = st.number_input('Precio de la vivienda', min_value=0)
        # Pedir al usuario el número de años, los ingresos mensuales y el ahorro aportado.
        n = st.slider('Número de años', 5, 30)
        i = st.number_input('Ingresos netos mensuales', min_value=0)
        a = st.number_input('Ahorro aportado', min_value=0)
        interes_anual = 0.03

        # Validar que el ahorro aportado sea al menos el 20% del precio estimado de la vivienda.
        if a < predicted_price * 0.2:
            st.warning('El ahorro aportado debe ser al menos el 20% del precio estimado de la vivienda, es decir, superior a {} €'.format(predicted_price*0.2))
        
        # Calcular el principal de la hipoteca.
        principal = predicted_price - a

        # Calcular la tasa de interés mensual.
        r = interes_anual / 12

        # Calcular el número de pagos mensuales y la cuota mensual.
        n_pagos = n * 12
        cuota_mensual = principal * r * (1 + r)**n_pagos / ((1 + r)**n_pagos - 1)

        # Verificar si la cuota mensual es mayor al 50% de los ingresos mensuales.
        if cuota_mensual > i*0.5:
            st.warning(f"Consejo: La cuota mensual no debería superar el 50% de sus ingresos mensuales, es decir, superior a {i*0.5}")
                
            
    # Mostrar el resultado.
    st.markdown(
        f"""
        <div style="
            background-color: #2AB09C;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            margin-top: 20px;
            margin-left: auto;
            margin-right: auto;
            width: 60%;
        ">
            <div style="font-size: 30px; font-weight: 700; margin-bottom: 20px; color: #ffffff;">Resultado</div>
            <div style="font-size: 18px; font-weight: 700; color: #ffffff;">Para una hipoteca de {round(predicted_price)} € a {n} años con un tipo de interés del {interes_anual*100:.2f}% y un ahorro aportado de {a} €, la cuota mensual sería:</div>
            <div style="font-size: 30px; font-weight: 700; margin-bottom: 20px; color: #ffffff;">{cuota_mensual:.2f} €.</div>
        </div>
        """,
        unsafe_allow_html=True
    )








