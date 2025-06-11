import streamlit as st
import pandas as pd
import math
from fpdf import FPDF
from datetime import datetime

# ----------------------------
# BULK RECIPE DEFINITIONS
# ----------------------------
bulk_sections = [
    {"title": "Spaghetti Order", "batch_ingredient": "Spaghetti", "batch_size": 85, "ingredients": {"Spaghetti": 68, "Oil": 0.7}, "meals": ["Spaghetti Bolognese"]},
    {"title": "Penne Order", "batch_ingredient": "Penne", "batch_size": 157, "ingredients": {"Penne": 59, "Oil": 0.7}, "meals": ["Chicken Pesto Pasta", "Chicken and Broccoli Pasta"]},
    {"title": "Rice Order", "batch_ingredient": "Rice", "batch_size": 180, "ingredients": {"Rice": 60, "Oil": 0.7}, "meals": ["Beef Chow Mein", "Beef Burrito Bowl", "Lebanese Beef Stew", "Mongolian Beef", "Butter Chicken", "Thai Green Chicken Curry", "Beans Nacho", "Chicken Fajita Bowl"]},
    {"title": "Moroccan Chicken", "batch_ingredient": "Chicken", "batch_size": 0, "ingredients": {"Chicken": 180, "Oil": 2, "Lemon Juice": 6, "Moroccan Chicken Mix": 4}, "meals": ["Moroccan Chicken"]},
    {"title": "Steak", "batch_ingredient": "Steak", "batch_size": 0, "ingredients": {"Steak": 110, "Oil": 1.5, "Baking Soda": 3}, "meals": ["Steak with Mushroom Sauce", "Steak On Its Own"]},
    {"title": "Lamb Marinate", "batch_ingredient": "Lamb Shoulder", "batch_size": 0, "ingredients": {"Lamb Shoulder": 162, "Oil": 2, "Salt": 1.5, "Oregano": 1.2}, "meals": ["Naked Chicken Parma", "Lamb Souvlaki"]},
    {"title": "Potato Mash", "batch_ingredient": "Potato", "batch_size": 0, "ingredients": {"Potato": 150, "Cooking Cream": 20, "Butter": 7, "Salt": 1.5, "White Pepper": 0.5}, "meals": ["Beef Meatballs", "Steak with Mushroom Sauce"]},
    {"title": "Sweet Potato Mash", "batch_ingredient": "Sweet Potato", "batch_size": 0, "ingredients": {"Sweet Potato": 185, "Salt": 1, "White Pepper": 0.5}, "meals": ["Shepherd's Pie", "Chick Sweet Potato and Beans"]},
    {"title": "Roasted Potatoes", "batch_ingredient": "Roasted Potatoes", "batch_size": 60, "ingredients": {"Roasted Potatoes": 190, "Oil": 1, "Spices Mix": 2.5}, "meals": []},
    {"title": "Roasted Lemon Potatoes", "batch_ingredient": "Potatoes", "batch_size": 60, "ingredients": {"Potatoes": 207, "Oil": 1, "Salt": 1.2}, "meals": ["Roasted Lemon Chicken"]},
    {"title": "Roasted Thai Potatoes ", "batch_ingredient": "Potato", "batch_size": 0, "ingredients": {"Potato": 60, "Salt": 1}, "meals": ["Thai Green Chicken Curry"]},
    {"title": "Lamb Onion Marinated", "batch_ingredient": "Red Onion", "batch_size": 0, "ingredients": {"Red Onion": 30, "Parsley": 1.5, "Paprika": 0.5}, "meals": ["Lamb Souvlaki"]},
    {"title": "Green Beans", "batch_ingredient": "Green Beans", "batch_size": 0, "ingredients": {"Green Beans": 60}, "meals": ["Chicken with Vegetables", "Chick Sweet Potato and Beans", "Steak with Mushroom Sauce"]}
]

# ----------------------------
# MEAL RECIPE DEFINITIONS (Flexible for Part 2)
# ----------------------------
meal_recipes = {
    "Spaghetti Bolognese": {
        "batch_ingredient": "Spaghetti",
        "batch_size": 68,
        "ingredients": {
            "Beef Mince": 100,
            "Napoli Sauce": 65,
            "Beef Stock": 30,
            "Onion": 15,
            "Zucchini": 15,
            "Carrot": 15,
            "Crushed Tomatos": 45,
            "Vegetable Oil": 1,
            "Salt": 2,
            "Pepper": 0.5,
            "Spaghetti": 68
        }
    }
}

# ----------------------------
# Streamlit App
# ----------------------------
st.title("\U0001F4E6 Bulk Ingredient Summary Report")
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
    report_date = datetime.today().strftime("%d/%m/%Y")
    pdf.cell(0, 10, f"Daily Production Report - {report_date}", ln=True, align="C")
    pdf.ln(5)

    left_margin = 10
    page_width = 210 - 2 * left_margin
    col_width = page_width / 2 - 5
    cell_height = 6
    padding_after_table = 4

    column_heights = [pdf.get_y(), pdf.get_y()]
    column_x = [left_margin, left_margin + col_width + 10]
    current_column = 0

    def draw_section(column_index, section):
        x = column_x[column_index]
        y = column_heights[column_index]
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
        pdf.cell(col_width * 0.38, cell_height, "Ingredient", 1)
        pdf.cell(col_width * 0.14, cell_height, "Quantity", 1)
        pdf.cell(col_width * 0.14, cell_height, "Meals", 1)
        pdf.cell(col_width * 0.22, cell_height, "Batch Total", 1)
        pdf.cell(col_width * 0.12, cell_height, "Batches", 1)
        pdf.ln(cell_height)

        pdf.set_font("Arial", "", 8)
        batches_required = math.ceil(amount / batch_size) if batch_size > 0 else 0

        for ingredient, qty_per_meal in ingredients.items():
            total = qty_per_meal * amount
            if batch_size > 0 and batches_required > 0:
                adjusted_total = round(total / batches_required)
            else:
                adjusted_total = round(total, 2)
            batches = batches_required if batch_size > 0 and ingredient == batch_ingredient else ""

            pdf.set_x(x)
            pdf.cell(col_width * 0.38, cell_height, ingredient[:20], 1)
            pdf.cell(col_width * 0.14, cell_height, str(qty_per_meal), 1)
            pdf.cell(col_width * 0.14, cell_height, str(amount), 1)
            pdf.cell(col_width * 0.22, cell_height, str(adjusted_total), 1)
            pdf.cell(col_width * 0.12, cell_height, str(batches), 1)
            pdf.ln(cell_height)

        column_heights[column_index] = pdf.get_y() + padding_after_table

    for section in bulk_sections:
        estimated_height = column_heights[current_column] + (len(section["ingredients"]) + 2) * cell_height + padding_after_table
        if estimated_height > 270:
            current_column = 1 - current_column
        draw_section(current_column, section)

    # ----------------------------
    # Add Meal Breakdown Section
    # ----------------------------
    for meal_name, data in meal_recipes.items():
        meal_quantity = meal_totals.get(meal_name.upper(), 0)
        if meal_quantity == 0:
            continue

        estimated_height = column_heights[current_column] + (len(data["ingredients"]) + 2) * cell_height + padding_after_table
        if estimated_height > 270:
            current_column = 1 - current_column

        x = column_x[current_column]
        y = column_heights[current_column]
        pdf.set_xy(x, y)

        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(col_width, cell_height, meal_name, ln=1, fill=True)

        pdf.set_x(x)
        pdf.set_font("Arial", "B", 8)
        pdf.cell(col_width * 0.38, cell_height, "Ingredient", 1)
        pdf.cell(col_width * 0.14, cell_height, "Meals", 1)
        pdf.cell(col_width * 0.36, cell_height, "Batch Total", 1)
        pdf.cell(col_width * 0.12, cell_height, "Batch", 1)
        pdf.ln(cell_height)

        pdf.set_font("Arial", "", 8)
        batch_size = data.get("batch_size", 0)
        batches_required = math.ceil(meal_quantity / batch_size) if batch_size > 0 else 0

        for idx, (ingredient, qty_per_meal) in enumerate(data["ingredients"].items()):
            total = qty_per_meal * meal_quantity
            batch_total = round(total / batches_required) if batch_size > 0 and batches_required > 0 else round(total, 2)
            batch_text = str(batches_required) if idx == 0 and batch_size > 0 else ""

            pdf.set_x(x)
            pdf.cell(col_width * 0.38, cell_height, ingredient[:20], 1)
            pdf.cell(col_width * 0.14, cell_height, str(meal_quantity), 1)
            pdf.cell(col_width * 0.36, cell_height, str(batch_total), 1)
            pdf.cell(col_width * 0.12, cell_height, batch_text, 1)
            pdf.ln(cell_height)

        column_heights[current_column] = pdf.get_y() + padding_after_table

    filename_date = datetime.today().strftime("%d-%m-%Y")
    pdf_path = f"daily_production_report_{filename_date}.pdf"
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button("\U0001F4C4 Download Bulk Order PDF", f, file_name=pdf_path, mime="application/pdf")
