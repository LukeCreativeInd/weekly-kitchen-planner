import streamlit as st
import pandas as pd
import math
from fpdf import FPDF

# ----------------------------
# BULK RECIPE DEFINITIONS
# ----------------------------
bulk_sections = [
    {
        "title": "Pasta Order",
        "batch_ingredient": "Spaghetti",
        "batch_size": 68,
        "ingredients": {
            "Spaghetti": 68,
            "Oil": 0.7
        },
        "meals": ["SPAGHETTI BOLOGNESE"]
    },
    {
        "title": "Penne Order",
        "batch_ingredient": "Penne",
        "batch_size": 59,
        "ingredients": {
            "Penne": 59,
            "Oil": 0.7
        },
        "meals": ["CHICKEN PESTO PASTA", "CHICKEN AND BROCCOLI PASTA"]
    },
    {
        "title": "Rice Recipe",
        "batch_ingredient": "Rice",
        "batch_size": 60,
        "ingredients": {
            "Rice": 60,
            "Oil": 0.7
        },
        "meals": [
            "BEEF CHOW MEIN", "BEEF BURRITO BOWL", "LEBANESE BEEF STEW",
            "MONGOLIAN BEEF", "BUTTER CHICKEN", "THAI GREEN CHICKEN CURRY",
            "BEANS NACHO", "CHICKEN FAJITA BOWL"
        ]
    },
    {
        "title": "Italian Herbs Chicken",
        "batch_ingredient": "Chicken",
        "batch_size": 80,
        "ingredients": {
            "Chicken": 180,
            "Oil": 2,
            "Lemon Juice": 6,
            "Italian Herbs Mix": 4
        },
        "meals": ["CHICKEN WITH VEGETABLES", "CHICK SWEET POTATO AND BEANS", "NAKED CHICKEN PARMA", "CHICKEN ON ITS OWN"]
    },
    {
        "title": "Moroccan Chicken",
        "batch_ingredient": "Chicken",
        "batch_size": 80,
        "ingredients": {
            "Chicken": 180,
            "Oil": 2,
            "Lemon Juice": 6,
            "Moroccan Chicken Mix": 4
        },
        "meals": ["MORROCAN CHICKEN"]
    },
    {
        "title": "Chicken Thigh",
        "batch_ingredient": "Chicken Thigh",
        "batch_size": 80,
        "ingredients": {
            "Chicken Thigh": 150,
            "Roast Chicken Mix": 4,
            "Oil": 4
        },
        "meals": ["ROASTED LEMON CHICKEN", "CHICKEN FAJITA BOWL"]
    },
    {
        "title": "Topside Steak",
        "batch_ingredient": "Steak",
        "batch_size": 80,
        "ingredients": {
            "Steak": 110,
            "Oil": 1.5,
            "Baking Soda": 3
        },
        "meals": ["STEAK WITH MUSHROOM SAUCE", "STEAK ON ITS OWN"]
    },
    {
        "title": "Lamb Shoulder Marinated",
        "batch_ingredient": "Lamb Shoulder",
        "batch_size": 80,
        "ingredients": {
            "Lamb Shoulder": 162,
            "Oil": 2,
            "Salt": 1.5,
            "Oregano": 1.2
        },
        "meals": ["LAMB SOUVLAKI"]
    },
    {
        "title": "Lamb Veg Marinated",
        "batch_ingredient": "Red Onion",
        "batch_size": 80,
        "ingredients": {
            "Red Onion": 30,
            "Parsley": 1.5,
            "Paprika": 0.5
        },
        "meals": ["LAMB SOUVLAKI"]
    },
    {
        "title": "Roasted Lemon Potato",
        "batch_ingredient": "Potatoes",
        "batch_size": 80,
        "ingredients": {
            "Potatoes": 207,
            "Oil": 1,
            "Salt": 1.2
        },
        "meals": ["ROASTED LEMON CHICKEN"]
    },
    {
        "title": "Roasted Potatoes Thai",
        "batch_ingredient": "Potato",
        "batch_size": 80,
        "ingredients": {
            "Potato": 60,
            "Salt": 1
        },
        "meals": ["THAI GREEN CHICKEN CURRY"]
    },
    {
        "title": "Potato Mash",
        "batch_ingredient": "Potato",
        "batch_size": 80,
        "ingredients": {
            "Potato": 150,
            "Cooking Cream": 20,
            "Butter": 7,
            "Salt": 1.5,
            "White Pepper": 0.5
        },
        "meals": ["BEEF MEATBALLS", "STEAK WITH MUSHROOM SAUCE"]
    },
    {
        "title": "Sweet Potato Mash",
        "batch_ingredient": "Sweet Potato",
        "batch_size": 80,
        "ingredients": {
            "Sweet Potato": 185,
            "Salt": 1,
            "White Pepper": 0.5
        },
        "meals": ["SHEPHERD'S PIE", "CHICK SWEET POTATO AND BEANS"]
    },
    {
        "title": "Green Beans",
        "batch_ingredient": "Green Beans",
        "batch_size": 80,
        "ingredients": {
            "Green Beans": 60
        },
        "meals": ["CHICKEN WITH VEGETABLES", "CHICK SWEET POTATO AND BEANS", "STEAK WITH MUSHROOM SAUCE"]
    }
]

# ----------------------------
# Streamlit App
# ----------------------------
st.title("📦 Bulk Ingredient Summary Report")
uploaded_file = st.file_uploader("Upload Production CSV (Product name, Quantity)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()
    if not {"product name", "quantity"}.issubset(df.columns):
        st.error("CSV must contain 'Product name' and 'Quantity' columns.")
        st.stop()

    st.success("CSV uploaded successfully!")
    st.dataframe(df)

    meal_totals = dict(zip(df["product name"].str.upper(), df["quantity"]))

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Weekly Ingredient Report - Bulk Order", ln=True, align="C")
    pdf.ln(5)

    # Two-column layout setup
    col_width = 95
    cell_height = 8
    section_count = 0

    for section in bulk_sections:
        if section_count % 2 == 0 and section_count > 0:
            pdf.ln(3)
        if section_count % 2 == 0:
            start_y = pdf.get_y()
            start_x = pdf.get_x()
        else:
            pdf.set_y(start_y)
            pdf.set_x(start_x + col_width + 5)

        section_title = section["title"]
        batch_ingredient = section["batch_ingredient"]
        batch_size = section["batch_size"]
        ingredients = section["ingredients"]
        source_meals = section["meals"]
        total_meals = sum(meal_totals.get(meal.upper(), 0) for meal in source_meals)

        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(col_width, cell_height, section_title, ln=True, fill=True)

        pdf.set_font("Arial", "B", 8)
        pdf.cell(col_width / 2, cell_height, "Ingredient", 1)
        pdf.cell(col_width / 2, cell_height, "Batch/Grams", 1)
        pdf.ln()

        pdf.set_font("Arial", "", 8)
        for idx, (ingredient, per_meal) in enumerate(ingredients.items()):
            is_batch_driver = (ingredient == batch_ingredient)
            amount_label = f"{batch_size}" if is_batch_driver else f"{per_meal}g"
            pdf.cell(col_width / 2, cell_height, ingredient, 1)
            pdf.cell(col_width / 2, cell_height, amount_label, 1)
            pdf.ln()

        batches = math.ceil(total_meals / batch_size) if batch_size > 0 else 0
        pdf.set_font("Arial", "I", 7)
        pdf.cell(col_width, cell_height, f"Total Meals: {total_meals} | Batches: {batches}", 0, ln=True)

        if section_count % 2 == 1:
            pdf.ln(3)

        section_count += 1

    pdf_path = "bulk_ingredient_report.pdf"
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download Bulk Order PDF", f, file_name=pdf_path, mime="application/pdf")
