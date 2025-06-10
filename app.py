import streamlit as st
import pandas as pd
import math
from fpdf import FPDF

# ----------------------------
# BULK RECIPE DEFINITIONS
# ----------------------------
# Each entry defines a section title, batch-driving ingredient, and ingredient breakdown
bulk_sections = [
    {
        "title": "Pasta Order",
        "batch_ingredient": "Spaghetti",
        "batch_size": 68,
        "meals": ["SPAGHETTI BOLOGNESE"],
        "ingredients": {
            "Spaghetti": 68,
            "Oil": 0.7
        }
    },
    {
        "title": "Penne Order",
        "batch_ingredient": "Penne",
        "batch_size": 59,
        "meals": ["CHICKEN PESTO PASTA", "CHICKEN AND BROCCOLI PASTA"],
        "ingredients": {
            "Penne": 59,
            "Oil": 0.7
        }
    },
    {
        "title": "Rice Order",
        "batch_ingredient": "Rice",
        "batch_size": 53,
        "meals": ["BEEF CHOW MEIN", "BEEF BURRITO BOWL", "LEBANESE BEEF STEW", "MONGOLIAN BEEF",
                   "BUTTER CHICKEN", "THAI GREEN CHICKEN CURRY", "BEAN NACHO", "CHICKEN FAJITA BOWL"],
        "ingredients": {
            "Rice": 53,
            "Water": 95,
            "Salt": 1,
            "Oil": 1.5
        }
    },
    {
        "title": "Italian Herbs Chicken",
        "batch_ingredient": "Chicken",
        "batch_size": 155,
        "meals": ["CHICKEN WITH VEGETABLES", "CHICK SWEET POTATO AND BEANS",
                   "NAKED CHICKEN PARMA", "CHICKEN ON ITS OWN"],
        "ingredients": {
            "Chicken": 155,
            "Italian Herbs Mix": 2,
            "Oil": 4
        }
    },
    {
        "title": "Normal Chicken",
        "batch_ingredient": "Chicken",
        "batch_size": 130,
        "meals": ["CHICKEN PESTO PASTA", "CHICKEN AND BROCCOLI PASTA", "BUTTER CHICKEN",
                   "THAI GREEN CHICKEN CURRY", "CREAMY CHICKEN AND MUSHROOM GNOCCHI"],
        "ingredients": {
            "Chicken": 130,
            "Normal Chicken Mix": 1.7,
            "Oil": 3
        }
    },
    {
        "title": "Moroccan Chicken",
        "batch_ingredient": "Chicken",
        "batch_size": 180,
        "meals": ["MORROCAN CHICKEN"],
        "ingredients": {
            "Chicken": 180,
            "Oil": 2,
            "Lemon Juice": 6,
            "Moroccan Chicken Mix": 4
        }
    },
    {
        "title": "Chicken Thigh",
        "batch_ingredient": "Chicken Thigh",
        "batch_size": 150,
        "meals": ["ROASTED LEMON CHICKEN", "CHICKEN FAJITA BOWL"],
        "ingredients": {
            "Chicken Thigh": 150,
            "Roast Chicken Mix": 4,
            "Oil": 4
        }
    },
    {
        "title": "Topside Steak",
        "batch_ingredient": "Steak",
        "batch_size": 110,
        "meals": ["STEAK WITH MUSHROOM SAUCE", "STEAK ON ITS OWN"],
        "ingredients": {
            "Steak": 110,
            "Oil": 1.5,
            "Baking Soda": 3
        }
    },
    {
        "title": "Lamb Shoulder Marinated",
        "batch_ingredient": "Lamb Shoulder",
        "batch_size": 162,
        "meals": ["LAMB SOUVLAKI"],
        "ingredients": {
            "Lamb Shoulder": 162,
            "Oil": 2,
            "Salt": 1.5,
            "Oregano": 1.2
        }
    },
    {
        "title": "Lamb Veg Marinated",
        "batch_ingredient": "Red Onion",
        "batch_size": 30,
        "meals": ["LAMB SOUVLAKI"],
        "ingredients": {
            "Red Onion": 30,
            "Parsley": 1.5,
            "Paprika": 0.5
        }
    },
    {
        "title": "Roasted Lemon Potato",
        "batch_ingredient": "Potatoes",
        "batch_size": 207,
        "meals": ["ROASTED LEMON CHICKEN"],
        "ingredients": {
            "Potatoes": 207,
            "Oil": 1,
            "Salt": 1.2
        }
    },
    {
        "title": "Roasted Potatoes Thai",
        "batch_ingredient": "Potato",
        "batch_size": 60,
        "meals": ["THAI GREEN CHICKEN CURRY"],
        "ingredients": {
            "Potato": 60,
            "Salt": 1
        }
    },
    {
        "title": "Potato Mash",
        "batch_ingredient": "Potato",
        "batch_size": 150,
        "meals": ["BEEF MEATBALLS", "STEAK WITH MUSHROOM SAUCE"],
        "ingredients": {
            "Potato": 150,
            "Cooking Cream": 20,
            "Butter": 7,
            "Salt": 1.5,
            "White Pepper": 0.5
        }
    },
    {
        "title": "Sweet Potato Mash",
        "batch_ingredient": "Sweet Potato",
        "batch_size": 185,
        "meals": ["SHEPHERD'S PIE", "CHICK SWEET POTATO AND BEANS"],
        "ingredients": {
            "Sweet Potato": 185,
            "Salt": 1,
            "White Pepper": 0.5
        }
    },
    {
        "title": "Green Beans",
        "batch_ingredient": "Green Beans",
        "batch_size": 60,
        "meals": ["CHICKEN WITH VEGETABLES", "CHICK SWEET POTATO AND BEANS", "STEAK WITH MUSHROOM SAUCE"],
        "ingredients": {
            "Green Beans": 60
        }
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

    for section in bulk_sections:
        section_title = section["title"]
        batch_ingredient = section["batch_ingredient"]
        batch_size = section["batch_size"]
        ingredients = section["ingredients"]
        source_meals = section["meals"]

        # Total meals using this bulk
        total_meals = sum(meal_totals.get(meal.upper(), 0) for meal in source_meals)

        # Start Section
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 8, section_title, ln=True, fill=True)

        # Table Header
        pdf.set_font("Arial", "B", 10)
        pdf.cell(60, 8, "Ingredient", 1)
        pdf.cell(40, 8, "Batch Size", 1)
        pdf.cell(40, 8, "Meals Required", 1)
        pdf.cell(40, 8, "Batches Required", 1)
        pdf.ln()

        pdf.set_font("Arial", "", 10)
        for idx, (ingredient, per_meal) in enumerate(ingredients.items()):
            is_batch_driver = (ingredient == batch_ingredient)
            batch_display = batch_size if ingredient in section["ingredients"] else ""
            batches = math.ceil(total_meals / batch_size) if is_batch_driver and batch_size > 0 else ""
            pdf.cell(60, 8, ingredient, 1)
            pdf.cell(40, 8, str(batch_size if is_batch_driver else per_meal), 1)
            pdf.cell(40, 8, str(total_meals), 1)
            pdf.cell(40, 8, str(batches), 1)
            pdf.ln()

        pdf.ln(3)

    # Save PDF
    pdf_path = "bulk_ingredient_report.pdf"
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download Bulk Order PDF", f, file_name=pdf_path, mime="application/pdf")
