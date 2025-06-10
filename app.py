import streamlit as st
import pandas as pd
import math
from fpdf import FPDF

# ----------------------------
# BULK RECIPE DEFINITIONS
# ----------------------------
bulk_sections = [
    # (Same definitions as before - unchanged for brevity)
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

        # Summary row for meals and batches
        batches = math.ceil(total_meals / batch_size) if batch_size > 0 else 0
        pdf.set_font("Arial", "I", 7)
        pdf.cell(col_width, cell_height, f"Total Meals: {total_meals} | Batches: {batches}", 0, ln=True)

        if section_count % 2 == 1:
            pdf.ln(3)

        section_count += 1

    # Save PDF
    pdf_path = "bulk_ingredient_report.pdf"
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download Bulk Order PDF", f, file_name=pdf_path, mime="application/pdf")
