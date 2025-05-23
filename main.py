import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

def train_and_save_model():
    df = pd.read_csv('oyo_housing_sample.csv')
    categorical_cols = [
        'mainroad', 'guestroom', 'basement', 'hotwaterheating',
        'airconditioning', 'prefarea', 'furnishingstatus', 'region'
    ]
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    X = df_encoded.drop('price', axis=1)
    y = df_encoded['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump((model, list(X.columns)), 'house_value_model.joblib')
    print('Model trained and saved as house_value_model.joblib')

if __name__ == "__main__":
    train_and_save_model()
