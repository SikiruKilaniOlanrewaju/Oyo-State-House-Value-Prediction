import pandas as pd
import numpy as np

regions = [
    "Ibadan", "Oyo", "Ogbomosho", "Iseyin", "Saki", "Igboho", "Eruwa", "Igbo-Ora", "Lanlate", "Okeho",
    "Kisi (Kishi)", "Fiditi", "Ilora", "Lalupon", "Awe", "Tede", "Sepeteri", "Ago-Amodu", "Ado-Awaye",
    "Igbeti", "Otu", "Igangan", "Iroko", "Akinmoorin", "Jobele", "Ayete", "Iresa-Adu", "Iresa-Apa",
    "Alabata", "Erunmu"
]

furnishings = ["unfurnished", "semi-furnished", "furnished"]
yesno = ["yes", "no"]

rows = []
np.random.seed(42)
for i in range(7000):
    area = np.random.randint(80, 400)
    bedrooms = np.random.randint(1, 6)
    bathrooms = np.random.randint(1, 4)
    stories = np.random.randint(1, 3)
    parking = np.random.randint(0, 4)
    mainroad = np.random.choice(yesno)
    guestroom = np.random.choice(yesno)
    basement = np.random.choice(yesno)
    hotwaterheating = np.random.choice(yesno)
    airconditioning = np.random.choice(yesno)
    prefarea = np.random.choice(yesno)
    furnishingstatus = np.random.choice(furnishings)
    region = np.random.choice(regions)
    # Price logic: more features = higher price, but always between 100,000 and 1,000,000
    base = 100_000
    price = base + area*5 + bedrooms*10000 + bathrooms*7000 + stories*5000 + parking*3000
    price += 5000 if mainroad == "yes" else 0
    price += 4000 if guestroom == "yes" else 0
    price += 3000 if basement == "yes" else 0
    price += 3000 if hotwaterheating == "yes" else 0
    price += 4000 if airconditioning == "yes" else 0
    price += 3000 if prefarea == "yes" else 0
    price += {"unfurnished": 0, "semi-furnished": 7000, "furnished": 15000}[furnishingstatus]
    price += np.random.randint(-10000, 10000)
    price = int(np.clip(price, 100_000, 1_000_000))
    rows.append([
        area, bedrooms, bathrooms, stories, parking, mainroad, guestroom, basement,
        hotwaterheating, airconditioning, prefarea, furnishingstatus, region, price
    ])

df = pd.DataFrame(rows, columns=[
    "area", "bedrooms", "bathrooms", "stories", "parking", "mainroad", "guestroom", "basement",
    "hotwaterheating", "airconditioning", "prefarea", "furnishingstatus", "region", "price"
])
df.to_csv("oyo_housing_sample.csv", index=False)
print("Generated oyo_housing_sample.csv with 7,000 rows and prices between ₦100,000 and ₦1,000,000.")
