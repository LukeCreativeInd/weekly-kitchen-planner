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
        "batch_size": 85,
        "ingredients": {
            "Spaghetti": 68,
            "Oil": 0.7
        },
        "meals": ["SPAGHETTI BOLOGNESE"]
    },
    {
        "title": "Penne Order",
        "batch_ingredient": "Penne",
        "batch_size": 157,
        "ingredients": {
            "Penne": 59,
            "Oil": 0.7
        },
        "meals": ["CHICKEN PESTO PASTA", "CHICKEN AND BROCCOLI PASTA"]
    },
    {
        "title": "Rice Recipe",
        "batch_ingredient": "Rice",
        "batch_size": 180,
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
        "title": "Moroccan Chicken",
        "batch_ingredient": "Chicken",
        "batch_size": 0,
        "ingredients": {
            "Chicken": 180,
            "Oil": 2,
            "Lemon Juice": 6,
            "Moroccan Chicken Mix": 4
        },
        "meals": ["MORROCAN CHICKEN"]
    },
    {
        "title": "Topside Steak",
        "batch_ingredient": "Steak",
        "batch_size": 0,
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
        "batch_size": 0,
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
        "batch_size": 0,
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
        "batch_size": 60,
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
        "batch_size": 0,
        "ingredients": {
            "Potato": 60,
            "Salt": 1
        },
        "meals": ["THAI GREEN CHICKEN CURRY"]
    },
    {
        "title": "Roasted Potatoes",
        "batch_ingredient": "Roasted Potatoes",
        "batch_size": 60,
        "ingredients": {
            "Roasted Potatoes": 190,
            "Oil": 1,
            "Spices Mix": 2.5
        },
        "meals": ["NAKED CHICKEN PARMA", "LAMB SOUVLAKI"]
    },
    {
        "title": "Potato Mash",
        "batch_ingredient": "Potato",
        "batch_size": 0,
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
        "batch_size": 0,
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
        "batch_size": 0,
        "ingredients": {
            "Green Beans": 60
        },
        "meals": [
            "CHICKEN WITH VEGETABLES",
            "CHICK SWEET POTATO AND BEANS",
            "STEAK WITH MUSHROOM SAUCE"
        ]
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

    left_margin = 10
    page_width = 210 - 2 * left_margin
    col_width = page_width / 2 - 5
    cell_height = 6

    x_left = left_margin
    x_right = left_margin + col_width + 10
    y_left = pdf.get_y()
    y_right = y_left

    def draw_section(x, y, section):
        pdf.set_xy(x, y)
        section_title = section["title"]
        batch_ingredient = section["batch_ingredient"]
        batch_size = section["batch_size"]
        ingredients = section["ingredients"]
        source_meals = section["meals"]
        amount = sum(meal_totals.get(meal.upper(), 0) for meal in source_meals)

        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(col_width, cell_height, section_title, ln=1, fill=True)

        pdf.set_x(x)
        pdf.set_font("Arial", "B", 8)
        pdf.cell(col_width * 0.4, cell_height, "Ingredient", 1)
        pdf.cell(col_width * 0.15, cell_height, "Qty", 1)
        pdf.cell(col_width * 0.15, cell_height, "Amt", 1)
        pdf.cell(col_width * 0.15, cell_height, "Total", 1)
        pdf.cell(col_width * 0.15, cell_height, "Batches", 1)
        pdf.ln(cell_height)

        pdf.set_font("Arial", "", 8)
        start_y = pdf.get_y()

        batches_required = math.ceil(amount / batch_size) if batch_size > 0 else 0

        for ingredient, qty_per_meal in ingredients.items():
            total = qty_per_meal * amount
            if batch_size > 0 and batches_required > 0:
                adjusted_total = round(total / batches_required)
            else:
                adjusted_total = round(total, 2)
            batches = batches_required if batch_size > 0 and ingredient == batch_ingredient else ""

            pdf.set_x(x)
            pdf.cell(col_width * 0.4, cell_height, ingredient[:20], 1)
            pdf.cell(col_width * 0.15, cell_height, str(qty_per_meal), 1)
            pdf.cell(col_width * 0.15, cell_height, str(amount), 1)
            pdf.cell(col_width * 0.15, cell_height, str(adjusted_total), 1)
            pdf.cell(col_width * 0.15, cell_height, str(batches), 1)
            pdf.ln(cell_height)

        return pdf.get_y()

    for i in range(0, len(bulk_sections), 2):
        y_left = draw_section(x_left, y_left, bulk_sections[i])
        if i + 1 < len(bulk_sections):
            y_right = draw_section(x_right, y_right, bulk_sections[i + 1])
        max_y = max(y_left, y_right)
        y_left = y_right = max_y

    pdf_path = "bulk_ingredient_report.pdf"
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download Bulk Order PDF", f, file_name=pdf_path, mime="application/pdf")
