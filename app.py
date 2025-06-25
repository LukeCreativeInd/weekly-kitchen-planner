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
# SAUCE SECTION DEFINITIONS
# ----------------------------
sauce_sections = [
    {
        "title": "Thai Sauce",
        "meal": "THAI GREEN CHICKEN CURRY",
        "ingredients": {
            "Green Curry Paste": 7,
            "Coconut Cream": 82
        }
    },
    {
        "title": "Lamb Sauce",
        "meal": "LAMB SOUVLAKI",
        "ingredients": {
            "Greek Yogurt": 20,
            "Garlic": 2,
            "Salt": 1
        }
    }
]

# Placeholders for total meal counts (should be replaced with uploaded CSV data in actual app)
meal_totals = {
    "THAI GREEN CHICKEN CURRY": 82,
    "LAMB SOUVLAKI": 91
}

# PDF Creation
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Sauce Recipes", 0, 1, "C")
        self.ln(2)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=10)
pdf.add_page()
pdf.set_font("Arial", "", 10)

left_margin = 10
page_width = 210 - 2 * left_margin
col_width = page_width / 2 - 5
cell_height = 6
padding_after_table = 4
column_heights = [pdf.get_y(), pdf.get_y()]
column_x = [left_margin, left_margin + col_width + 10]
current_column = 0

def draw_sauce_section(column_index, title, ingredients_dict, total_meals):
    x = column_x[column_index]
    y = column_heights[column_index]
    pdf.set_xy(x, y)

    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_width, cell_height, title, ln=1, fill=True)

    pdf.set_x(x)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_width * 0.4, cell_height, "Ingredient", 1)
    pdf.cell(col_width * 0.2, cell_height, "Meal Amt", 1)
    pdf.cell(col_width * 0.2, cell_height, "Total Meals", 1)
    pdf.cell(col_width * 0.2, cell_height, "Required", 1)
    pdf.ln(cell_height)

    pdf.set_font("Arial", "", 8)
    for ingredient, meal_amt in ingredients_dict.items():
        required = meal_amt * total_meals
        pdf.set_x(x)
        pdf.cell(col_width * 0.4, cell_height, ingredient[:20], 1)
        pdf.cell(col_width * 0.2, cell_height, str(meal_amt), 1)
        pdf.cell(col_width * 0.2, cell_height, str(total_meals), 1)
        pdf.cell(col_width * 0.2, cell_height, str(required), 1)
        pdf.ln(cell_height)

    column_heights[column_index] = pdf.get_y() + padding_after_table

for sauce in sauce_sections:
    draw_sauce_section(current_column, sauce["title"], sauce["ingredients"], meal_totals.get(sauce["meal"], 0))
    current_column = 1 - current_column

# Save PDF using relative path for compatibility
pdf_path = "final_sauce_sections.pdf"
pdf.output(pdf_path)
with open(pdf_path, "rb") as f:
    st.download_button("\U0001F4C4 Download Sauce Section PDF", f, file_name=pdf_path, mime="application/pdf")
