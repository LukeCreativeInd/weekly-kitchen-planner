import streamlit as st
import pandas as pd
import math
from fpdf import FPDF

# ----------------------------
# RECIPE & BULK DEFINITIONS
# ----------------------------

# Meal recipe definitions (per meal)
meal_recipes = {
    "SPAGHETTI BOLOGNESE": {
        "BEEF MINCE": 100,
        "NAPOLI SAUCE": 65,
        "BEEF STOCK": 30,
        "ONION": 15,
        "ZUCCHINI": 15,
        "CARROT": 15,
        "CRUSHED TOMATOS": 45,
        "VEGETABLE OIL": 1,
        "SALT": 2,
        "PEPPER": 0.5,
        "SPAGHETTI": 68,
    }
}

# Bulk ingredient requirements
bulk_order_sections = {
    "Pasta Order": [
        {
            "ingredient": "Spaghetti",
            "batch_size": 68,
            "source_meal": "SPAGHETTI BOLOGNESE",
            "grams_per_meal": 68
        },
        {
            "ingredient": "Oil",
            "batch_size": 0.7,
            "source_meal": "SPAGHETTI BOLOGNESE",
            "grams_per_meal": 0.7
        }
    ]
}

# ----------------------------
# PDF Generator Class
# ----------------------------

class MealPrepPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        if self.page_no() == 1:
            self.cell(0, 10, "Weekly Ingredient Report", ln=True, align="C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", "B", 11)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 10, title, ln=True, fill=True)

    def ingredient_table(self, headers, data, col_widths):
        self.set_font("Arial", "B", 10)
        for i, name in enumerate(headers):
            self.cell(col_widths[i], 8, name, border=1, align="C")
        self.ln()
        self.set_font("Arial", "", 10)
        for row in data:
            for i, value in enumerate(row):
                self.cell(col_widths[i], 8, str(value), border=1)
            self.ln()

# ----------------------------
# Streamlit App
# ----------------------------

st.title("📦 Meal Production Report to PDF")

uploaded_file = st.file_uploader("Upload Production CSV (Meal,Quantity)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")
    st.dataframe(df)

    if st.button("Generate PDF Report"):
        meal_totals = dict(zip(df["Meal"], df["Quantity"]))

        # Generate PDF
        pdf = MealPrepPDF()
        pdf.add_page()

        # Page 1: Bulk Order Summary
        for section, items in bulk_order_sections.items():
            table_data = []
            for i, item in enumerate(items):
                meal = item["source_meal"]
                meals_required = meal_totals.get(meal, 0)
                batch_size = item["batch_size"]
                batch_required = math.ceil(meals_required / batch_size) if i == 0 else ""
                table_data.append([
                    item["ingredient"],
                    batch_size,
                    meals_required,
                    batch_required
                ])
            pdf.section_title(section)
            pdf.ingredient_table(["Ingredient", "Batch Size", "Meals Required", "Batches Required"], table_data, [50, 40, 50, 50])

        # Page 2+: Meal Breakdowns
        for meal_name, ingredients in meal_recipes.items():
            if meal_name in meal_totals:
                qty = meal_totals[meal_name]
                breakdown = []
                for ing, grams in ingredients.items():
                    total = grams * qty
                    breakdown.append([ing, grams, qty, total])
                pdf.add_page()
                pdf.section_title(meal_name)
                pdf.ingredient_table(["Ingredient", "Quantity", "Amount", "Total"], breakdown, [60, 40, 30, 40])

        # Save PDF
        pdf_path = "meal_production_report.pdf"
        pdf.output(pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download PDF", f, file_name=pdf_path, mime="application/pdf")
