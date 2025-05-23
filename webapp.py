import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(page_title="Oyo State House Value Predictor", page_icon="🏠", layout="centered")

# Elegant custom CSS styling
st.markdown('''
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background: linear-gradient(to right, #e0f7fa, #f7f7fa);
        padding: 2rem;
    }
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #4f8cff, #2563eb);
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        font-size: 2.8rem;
        margin: 0;
    }
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        color: #dbeafe;
    }
    .form-container {
        background-color: #ffffffcc;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .stTextInput>div>input, .stNumberInput>div>input, .stSelectbox>div>div {
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 0.6em;
        font-size: 1rem;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6em 2em;
        border: none;
        font-size: 1rem;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1e40af;
    }
    .stSuccess {
        background-color: #e0ffe0 !important;
        color: #256029 !important;
        border-radius: 10px;
        font-size: 1.2em !important;
        padding: 1rem;
    }
    </style>
''', unsafe_allow_html=True)

# Add elegant header
st.markdown('''
    <div class="main-header">
        <h1>🏠 Oyo State House Value Predictor</h1>
        <p>Estimate property value based on detailed housing features</p>
    </div>
''', unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    model, feature_columns = joblib.load('house_value_model.joblib')
    return model, feature_columns

model, feature_columns = load_model()

# Input Form
regions = [
    "Ibadan", "Oyo", "Ogbomosho", "Iseyin", "Saki", "Igboho", "Eruwa", "Igbo-Ora", "Lanlate", "Okeho",
    "Kisi (Kishi)", "Fiditi", "Ilora", "Lalupon", "Awe", "Tede", "Sepeteri", "Ago-Amodu", "Ado-Awaye",
    "Igbeti", "Otu", "Igangan", "Iroko", "Akinmoorin", "Jobele", "Ayete", "Iresa-Adu", "Iresa-Apa",
    "Alabata", "Erunmu"
]
furnishings = ["unfurnished", "semi-furnished", "furnished"]
yesno = ["yes", "no"]

with st.form("prediction_form"):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)
    submit = st.form_submit_button("Predict House Value")

# Prediction logic
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
    input_encoded = pd.get_dummies(input_df, columns=[
        'mainroad', 'guestroom', 'basement', 'hotwaterheating',
        'airconditioning', 'prefarea', 'furnishingstatus', 'region'
    ], drop_first=True)

    # Add missing columns
    for col in feature_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    input_encoded = input_encoded[feature_columns]

    # Predict
    pred = model.predict(input_encoded)[0]
    st.success(f"Estimated House Value: ₦{pred:,.2f}")
