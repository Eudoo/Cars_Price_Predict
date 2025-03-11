import streamlit as st
import gdown
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

file_id = "1cfYTfamo1JXPMxs9kLPxw-8fusZlVXCp"
output = "model_3_rand_forest.joblib"

gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False, use_cookies=False)

# Charger le modèle
model = joblib.load(output)

# Charger le scaler
scaler = joblib.load('scaler_2.joblib')

st.image('eud.jpg', use_container_width=True)

st.write('''
# Bienvenue sur Cars Price Predict ..! 
 🔍 Trouvez votre voiture idéale et obtenez une estimation de son prix 💰
''')

st.markdown("---")

st.sidebar.header('Les caractéristiques du véhicule')


brands = ['Ssangyong', 'MG', 'BMW', 'Mercedes-Benz', 'Renault', 'Land',
              'Nissan', 'Toyota', 'Honda', 'Volkswagen', 'Ford', 'Mitsubishi',
              'Subaru', 'Hyundai', 'Jeep', 'Volvo', 'Mazda', 'Abarth', 'Holden',
              'Audi', 'Kia', 'Mini', 'Suzuki', 'Porsche', 'Peugeot', 'Isuzu',
              'Lexus', 'Jaguar', 'Rolls-Royce', 'Skoda', 'Fiat', 'Haval',
              'Citroen', 'LDV', 'HSV', 'Foton', 'Mahindra', 'Maserati', 'GWM',
              'Ram', 'Tesla', 'Alfa', 'Genesis', 'Dodge', 'Chrysler', 'Great',
              'Opel', 'Bentley', 'Ferrari', 'Cupra', 'Chevrolet', 'Lamborghini',
              'FPV', 'McLaren', 'Iveco', 'Chery', 'Infiniti', 'BYD', 'Tata',
              'Aston', 'Daewoo', 'Saab', 'Proton', 'Smart']

models_dict = {
        'BMW': ['430I', 'X3', '118D', '220I', 'X4', '118I', 'M135I', '330I', 'X1',
                'M4', 'M140I', '218I', '320D', 'X5'],
        'Mercedes-Benz': ['E500', 'E250', 'A250', 'ML320', 'CLC200', 'C200', 'A200',
                          'GLA250', 'C220', 'C250', 'C43', 'GLC43', 'GLC300', 'CLA250',
                          'ML350', 'C63', 'C300', 'GLE63'],
        'Renault': ['Arkana', 'Trafic', 'Megane', 'Koleos', 'Kangoo', 'Captur', 'Clio',
                    'Master', 'Laguna', 'Kadjar'],
        'Nissan': ['Pulsar', 'Qashqai', 'X-Trail', 'Navara', 'Patrol', 'Pathfinder',
                   'Dualis', 'Almera', 'Juke', 'Altima', 'Maxima', 'Micra', 'Leaf',
                   'Murano', 'Tiida', 'Z', 'GT-R', '370Z', '350Z', '300ZX'],
        'Toyota': ['86', 'HiAce', 'Camry', 'Corolla', 'Yaris', 'Kluger', 'C-HR',
                   'RAV4', 'Hilux', 'Landcruiser', 'Tarago', 'GR', 'Hiace', 'Aurion',
                   'Celica', 'Echo', 'FJ', 'Fortuner', 'Granvia', 'Prius', 'Avensis',
                   'Supra', 'Avalon', 'Prius-C', 'Coaster', 'GR86'],
        'Volkswagen': ['Golf', 'Amarok', 'Tiguan', 'Caddy', 'Polo', 'Passat', 'Crafter',
                       'Multivan', 'Touareg', 'Transporter', 'T-Cross'],
        'Jeep': ['Patriot', 'Cherokee', 'Renegade'],
        'Audi': ['A5', 'Q7', 'Q3', 'RS3', 'A3', 'A4', 'SQ5', 'Q2', 'S3', 'R8'],
        'Porsche': ['Cayenne', 'Cayman', 'Macan', 'Taycan', '911', 'Boxster',
                    'Panamera', '718'],
        'Peugeot': ['308', '208', '2008', '508', '3008', 'RCZ'],
        'Jaguar': ['XF', 'F-Pace', 'XE', 'Xjsc', 'E-Pace', 'F-Type', 'X', 'XKR',
                   'XJ8', 'I-Pace'],
        'Bentley': ['Mulsanne', 'Continental', 'Arnage'],
        'Ferrari': ['360', 'F430', 'GTC4', 'California', '612'],
        'Lamborghini': ['Urus', 'Aventador'],
        'McLaren': ['720S', '540C', '650S', '570S']

    }
 

def user_input():

    # Widgets pour les caractéristiques du véhicule
    Brand = st.sidebar.selectbox(' 🚗 Marque:', brands, index=2)

    Year = st.sidebar.number_input(' 📅 Année de production:', min_value=1980, max_value=2024, value=2020, step=1)

    Model = st.sidebar.selectbox(' 🚘 Modèle de la voiture:', models_dict[Brand])

    UsedOrNew = st.sidebar.selectbox(' 🔄 État d\'utilisation:', ['DEMO', 'USED', 'NEW'])

    Transmission = st.sidebar.selectbox(' ⚙️ Transmission:', ['Automatic', 'Manual', '-'])

    FuelType = st.sidebar.selectbox(' ⛽ Type de carburant:', ['Diesel', 'Premium', 'Unleaded', 'Hybrid', '-',
                                                           'Electric', 'LPG', 'Leaded'])

    FuelConsumption = st.sidebar.number_input(' 🛢️ Consommation aux 100 Km (L):', min_value=0.0, max_value=30.0, value=7.0, step=0.1)

    Kilometres = st.sidebar.slider(' 📏 Kilométrage:', min_value=1, max_value=526162, value=1, step=1)

    BodyType = st.sidebar.selectbox(' 🚙 Gamme de voiture:', ['SUV', 'Hatchback', 'Coupe', 'Commercial', 'Ute / Tray',
                                                          'Sedan', 'People Mover', 'Convertible', 'Wagon', 'Other'])

    Seats = st.sidebar.number_input(' 💺 Nombre de sièges:', min_value=2, max_value=8, value=5, step=1)


    data = {
        'Brand': Brand,
        'Year': Year,
        'Model': Model,
        'UsedOrNew': UsedOrNew,
        'Transmission': Transmission,
        'FuelType': FuelType,
        'FuelConsumption (L / 100 Km)': FuelConsumption,
        'Kilometres': Kilometres,
        'BodyType': BodyType,
        'Seats': Seats
    }

    return pd.DataFrame(data, index=[0])


# Collecte des données d'entrée de l'utilisateur
input_data = user_input()

# Affichage des données saisies
st.write('#### 📋 Les caractéristiques du véhicule:')
st.write(input_data)



# Définir les mappings

brand_mapping = {'Ssangyong': 0, 'MG': 1, 'BMW': 2, 'Mercedes-Benz': 3, 'Renault': 4, 'Land': 5, 'Nissan': 6,
                 'Toyota': 7, 'Honda': 8, 'Volkswagen': 9, 'Ford': 10, 'Mitsubishi': 11, 'Subaru': 12, 'Hyundai': 13,
                 'Jeep': 14, 'Volvo': 15, 'Mazda': 16, 'Abarth': 17, 'Holden': 18, 'Audi': 19, 'Kia': 20, 'Mini': 21,
                 'Suzuki': 22, 'Porsche': 23, 'Peugeot': 24, 'Isuzu': 25, 'Lexus': 26, 'Jaguar': 27, 'Rolls-Royce': 28,
                 'Skoda': 29, 'Fiat': 30, 'Haval': 31, 'Citroen': 32, 'LDV': 33, 'HSV': 34, 'Foton': 35, 'Mahindra': 36,
                 'Maserati': 37, 'GWM': 38, 'Ram': 39, 'Tesla': 40, 'Alfa': 41, 'Genesis': 42, 'Dodge': 43,
                 'Chrysler': 44, 'Great': 45, 'Opel': 46, 'Bentley': 47, 'Ferrari': 48, 'Cupra': 49, 'Chevrolet': 50,
                 'Lamborghini': 51, 'FPV': 52, 'McLaren': 53, 'Iveco': 54, 'Chery': 55, 'Infiniti': 56, 'BYD': 57,
                 'Tata': 58, 'Aston': 59, 'Daewoo': 60, 'Saab': 61, 'Proton': 62, 'Smart': 63}


model_mapping = {'430I': 0, 'X3': 1, '118D': 2, '220I': 3, 'X4': 4, '118I': 5, 'M135I': 6, '330I': 7, 'X1': 8, 'M4': 9, 'M140I': 10, '218I': 11, '320D': 12, 'X5': 13,
                 'E500': 0, 'E250': 1, 'A250': 2, 'ML320': 3, 'CLC200': 4, 'C200': 5, 'A200': 6, 'GLA250': 7, 'C220': 8, 'C250': 9, 'C43': 10, 'GLC43': 11, 'GLC300': 12, 'CLA250': 13, 'ML350': 14, 'C63': 15, 'C300': 16, 'GLE63': 17,
                 'Arkana': 0, 'Trafic': 1, 'Megane': 2, 'Koleos': 3, 'Kangoo': 4, 'Captur': 5, 'Clio': 6, 'Master': 7, 'Laguna': 8, 'Kadjar': 9,
                 'Pulsar': 0, 'Qashqai': 1, 'X-Trail': 2, 'Navara': 3, 'Patrol': 4, 'Pathfinder': 5, 'Dualis': 6, 'Almera': 7, 'Juke': 8, 'Altima': 9, 'Maxima': 10, 'Micra': 11, 'Leaf': 12, 'Murano': 13, 'Tiida': 14, 'Z': 15, 'GT-R': 16, '370Z': 17, '350Z': 18, '300ZX': 19,
                 '86': 0, 'HiAce': 1, 'Camry': 2, 'Corolla': 3, 'Yaris': 4, 'Kluger': 5, 'C-HR': 6, 'RAV4': 7, 'Hilux': 8, 'Landcruiser': 9, 'Tarago': 10, 'GR': 11, 'Hiace': 12, 'Aurion': 13, 'Celica': 14, 'Echo': 15, 'FJ': 16, 'Fortuner': 17, 'Granvia': 18, 'Prius': 19, 'Avensis': 20, 'Supra': 21, 'Avalon': 22, 'Prius-C': 23, 'Coaster': 24, 'GR86': 25,
                 'Golf': 0, 'Amarok': 1, 'Tiguan': 2, 'Caddy': 3, 'Polo': 4, 'Passat': 5, 'Crafter': 6, 'Multivan': 7, 'Touareg': 8, 'Transporter': 9, 'T-Cross': 10,
                 'Patriot': 0, 'Cherokee': 1, 'Renegade': 2,
                 'A5': 0, 'Q7': 1, 'Q3': 2, 'RS3': 3, 'A3': 4, 'A4': 5, 'SQ5': 6, 'Q2': 7, 'S3': 8, 'R8': 9,
                 'Cayenne': 0, 'Cayman': 1, 'Macan': 2, 'Taycan': 3, '911': 4, 'Boxster': 5, 'Panamera': 6, '718': 7,
                 '308': 0, '208': 1, '2008': 2, '508': 3, '3008': 4, 'RCZ': 5,
                 'XF': 0, 'F-Pace': 1, 'XE': 2, 'Xjsc': 3, 'E-Pace': 4, 'F-Type': 5, 'X': 6, 'XKR': 7, 'XJ8': 8, 'I-Pace': 9,
                 'Mulsanne': 0, 'Continental': 1, 'Arnage': 2,
                 '360': 0, 'F430': 1, 'GTC4': 2, 'California': 3, '612': 4,
                 'Urus': 0, 'Aventador': 1,
                 '720S': 0, '540C': 1, '650S': 2, '570S': 3}


used_mapping = {'DEMO': 0, 'USED': 1, 'NEW': 2}
transmission_mapping = {'Automatic': 0, 'Manual': 1, '-': 2}
fuel_mapping = {'Diesel': 0, 'Premium': 1, 'Unleaded': 2, 'Hybrid': 3, '-': 4,
                'Electric': 5, 'LPG': 6, 'Leaded': 7}
body_mapping = {'SUV': 0, 'Hatchback': 1, 'Coupe': 2, 'Commercial': 3, 'Ute / Tray': 4,
                'Sedan': 5, 'People Mover': 6, 'Convertible': 7, 'Wagon': 8, 'Other': 9}


# Appliquer les mappings
input_data['Brand'] = input_data['Brand'].map(brand_mapping)
input_data['Model'] = input_data['Model'].map(model_mapping)
input_data['UsedOrNew'] = input_data['UsedOrNew'].map(used_mapping)
input_data['Transmission'] = input_data['Transmission'].map(transmission_mapping)
input_data['FuelType'] = input_data['FuelType'].map(fuel_mapping)
input_data['BodyType'] = input_data['BodyType'].map(body_mapping)

input_data[['Year',
            'FuelConsumption (L / 100 Km)',
            'Kilometres',
            'Seats']] = scaler.transform(input_data[['Year', 'FuelConsumption (L / 100 Km)', 'Kilometres', 'Seats']])

x = input_data['Brand'][0]
y = input_data['Model'][0]

# st.write(f'Marque: {x} et model: {y}')

# Prédire le prix avec le modèle chargé
if st.button(' 💰 Estimer le prix'):
    with st.spinner('🔄 **Calcul du prix estimé...**'):
        prediction = model.predict(input_data) # Prédire avec les données normalisées
    st.success(f"💵 **Prix estimé : {prediction[0]:,.2f} $**")
     


