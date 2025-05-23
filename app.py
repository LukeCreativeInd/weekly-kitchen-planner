import streamlit as st
import pandas as pd
from datetime import datetime

# Placeholder meal ingredient definitions
ingredient_db = {
    "Lasagna": {
        "Beef Mince (g)": 50,
        "Napoli Sauce (g)": 50,
        "Onions (g)": 10,
        "Mixed Herb (g)": 5
    },
    "Beef Chow Mein": {
        "Beef Mince (g)": 60,
        "Soy Sauce (ml)": 30,
        "Noodles (g)": 100,
        "Cabbage (g)": 20
    }
}

# Days of the week
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

st.title("🧑‍🍳 Weekly Ingredient Calculator")

# Tab interface for daily CSV uploads
tabs = st.tabs(week_days)
week_meals = {}

for idx, day in enumerate(week_days):
    with tabs[idx]:
        st.subheader(f"{day}")
        uploaded_file = st.file_uploader(f"Upload CSV for {day} (Meal,Quantity)", type="csv", key=f"upload_{day}")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            week_meals[day] = df
            st.success(f"Uploaded {len(df)} rows for {day}")

# Button to generate recipes
if st.button("🍲 Generate Recipes"):
    ingredient_totals = {}

    for day, df in week_meals.items():
        for _, row in df.iterrows():
            meal = row["Meal"]
            qty = row["Quantity"]
            if meal in ingredient_db:
                for ingredient, amount in ingredient_db[meal].items():
                    ingredient_totals[ingredient] = ingredient_totals.get(ingredient, 0) + amount * qty

    if ingredient_totals:
        st.subheader("📦 Total Ingredients Needed This Week")
        result_df = pd.DataFrame(ingredient_totals.items(), columns=["Ingredient", "Total Quantity"])
        st.dataframe(result_df)

        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"weekly_ingredients_{datetime.today().strftime('%Y%m%d')}.csv",
            mime='text/csv'
        )
    else:
        st.warning("No matching meals found in the recipe database yet.")
