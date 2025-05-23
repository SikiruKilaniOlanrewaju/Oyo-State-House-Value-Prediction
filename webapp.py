import streamlit as st
import pandas as pd
import joblib

# Load model and feature columns
@st.cache_resource
def load_model():
    model, feature_columns = joblib.load('house_value_model.joblib')
    return model, feature_columns

model, feature_columns = load_model()

st.title('🏠 Oyo State House Value Predictor')
st.write('Enter the house features below to predict the value (₦)')

# Define categorical options
regions = [
    "Ibadan", "Oyo", "Ogbomosho", "Iseyin", "Saki", "Igboho", "Eruwa", "Igbo-Ora", "Lanlate", "Okeho",
    "Kisi (Kishi)", "Fiditi", "Ilora", "Lalupon", "Awe", "Tede", "Sepeteri", "Ago-Amodu", "Ado-Awaye",
    "Igbeti", "Otu", "Igangan", "Iroko", "Akinmoorin", "Jobele", "Ayete", "Iresa-Adu", "Iresa-Apa",
    "Alabata", "Erunmu"
]
furnishings = ["unfurnished", "semi-furnished", "furnished"]
yesno = ["yes", "no"]

# User input form
with st.form("prediction_form"):
    area = st.number_input("Area (sq.m)", min_value=50, max_value=500, value=150)
    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=6, value=3)
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=4, value=2)
    stories = st.number_input("Stories", min_value=1, max_value=3, value=1)
    parking = st.number_input("Parking", min_value=0, max_value=4, value=1)
    mainroad = st.selectbox("Mainroad", yesno)
    guestroom = st.selectbox("Guestroom", yesno)
    basement = st.selectbox("Basement", yesno)
    hotwaterheating = st.selectbox("Hotwater Heating", yesno)
    airconditioning = st.selectbox("Air Conditioning", yesno)
    prefarea = st.selectbox("Preferred Area", yesno)
    furnishingstatus = st.selectbox("Furnishing Status", furnishings)
    region = st.selectbox("Region", regions)
    submit = st.form_submit_button("Predict House Value")

# Prepare input for model
if submit:
    input_dict = {
        'area': area,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'stories': stories,
        'parking': parking,
        'mainroad': mainroad,
        'guestroom': guestroom,
        'basement': basement,
        'hotwaterheating': hotwaterheating,
        'airconditioning': airconditioning,
        'prefarea': prefarea,
        'furnishingstatus': furnishingstatus,
        'region': region
    }
    input_df = pd.DataFrame([input_dict])
    # One-hot encode to match training
    input_encoded = pd.get_dummies(input_df, columns=[
        'mainroad', 'guestroom', 'basement', 'hotwaterheating',
        'airconditioning', 'prefarea', 'furnishingstatus', 'region'
    ], drop_first=True)
    # Add missing columns
    for col in feature_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    input_encoded = input_encoded[feature_columns]
    pred = model.predict(input_encoded)[0]
    st.success(f"Estimated House Value: ₦{pred:,.2f}")
