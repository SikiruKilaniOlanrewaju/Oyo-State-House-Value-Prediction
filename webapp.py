import streamlit as st
import pandas as pd
import joblib

# Add a beautiful page title and icon
st.set_page_config(page_title="Oyo State House Value Predictor", page_icon="🏠", layout="centered")

# Custom CSS for professional look
st.markdown('''
    <style>
    .main {
        background-color: #f7f7fa;
    }
    .stApp {
        background: linear-gradient(120deg, #e0e7ff 0%, #f7f7fa 100%);
    }
    .stButton>button {
        background-color: #4f8cff;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 2em;
        border: none;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        color: #fff;
    }
    .stTextInput>div>input, .stNumberInput>div>input {
        border-radius: 6px;
        border: 1px solid #cbd5e1;
        padding: 0.5em;
    }
    .stSelectbox>div>div {
        border-radius: 6px;
        border: 1px solid #cbd5e1;
    }
    .stSuccess {
        background-color: #e0ffe0;
        color: #256029;
        border-radius: 8px;
        font-size: 1.2em;
    }
    </style>
''', unsafe_allow_html=True)

# Load model and feature columns
@st.cache_resource
def load_model():
    model, feature_columns = joblib.load('house_value_model.joblib')
    return model, feature_columns

model, feature_columns = load_model()

st.title('🏠 Oyo State House Value Predictor')
st.markdown('<h4 style="color:#4f8cff;">Enter the house features below to predict the value (₦)</h4>', unsafe_allow_html=True)

regions = [
    "Ibadan", "Oyo", "Ogbomosho", "Iseyin", "Saki", "Igboho", "Eruwa", "Igbo-Ora", "Lanlate", "Okeho",
    "Kisi (Kishi)", "Fiditi", "Ilora", "Lalupon", "Awe", "Tede", "Sepeteri", "Ago-Amodu", "Ado-Awaye",
    "Igbeti", "Otu", "Igangan", "Iroko", "Akinmoorin", "Jobele", "Ayete", "Iresa-Adu", "Iresa-Apa",
    "Alabata", "Erunmu"
]
furnishings = ["unfurnished", "semi-furnished", "furnished"]
yesno = ["yes", "no"]

with st.form("prediction_form"):
    st.markdown("<div style='background-color:#e0e7ff;padding:1.5em 2em;border-radius:10px;'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)
    submit = st.form_submit_button("Predict House Value")

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
    for col in feature_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    input_encoded = input_encoded[feature_columns]
    pred = model.predict(input_encoded)[0]
    st.success(f"Estimated House Value: ₦{pred:,.2f}")
