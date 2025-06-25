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
# Streamlit App
# ----------------------------
st.title("\U0001F4E6 Bulk Ingredient Summary Report")
uploaded_file = st.file_uploader("Upload Production File (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip().str.lower()
    if not {"product name", "quantity"}.issubset(df.columns):
        st.error("CSV must contain 'Product name' and 'Quantity' columns.")
        st.stop()

    st.success("CSV uploaded successfully!")
    st.dataframe(df)

    meal_totals = dict(zip(df["product name"].str.upper(), df["quantity"]))

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    # ----------------------------
    # Page 1: Bulk Summary
    # ----------------------------
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

        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(col_width, cell_height, section["title"], ln=1, fill=True)
        pdf.ln(1)

        pdf.set_x(x)
        pdf.set_font("Arial", "B", 8)
        pdf.cell(col_width * 0.4, cell_height, "Ingredient", 1)
        pdf.cell(col_width * 0.15, cell_height, "Qty/Meal", 1)
        pdf.cell(col_width * 0.15, cell_height, "Meals", 1)
        pdf.cell(col_width * 0.15, cell_height, "Total", 1)
        pdf.cell(col_width * 0.15, cell_height, "Batches", 1)
        pdf.ln(cell_height)

        pdf.set_font("Arial", "", 8)
        amount = sum(meal_totals.get(meal.upper(), 0) for meal in section["meals"])
        batches_required = math.ceil(amount / section["batch_size"]) if section["batch_size"] > 0 else 0

        for ing, per in section["ingredients"].items():
            total_qty = per * amount
            if section["batch_size"] > 0 and batches_required > 0:
                adjusted = round(total_qty / batches_required)
            else:
                adjusted = round(total_qty, 2)
            batch_label = batches_required if ing == section["batch_ingredient"] else ""

            pdf.set_x(x)
            pdf.cell(col_width * 0.4, cell_height, ing[:20], 1)
            pdf.cell(col_width * 0.15, cell_height, str(per), 1)
            pdf.cell(col_width * 0.15, cell_height, str(amount), 1)
            pdf.cell(col_width * 0.15, cell_height, str(adjusted), 1)
            pdf.cell(col_width * 0.15, cell_height, str(batch_label), 1)
            pdf.ln(cell_height)

        column_heights[column_index] = pdf.get_y() + padding_after_table

    for sec in bulk_sections:
        est = column_heights[current_column] + (len(sec["ingredients"]) + 3) * cell_height
        if est > 270:
            current_column = 1 - current_column
        draw_section(current_column, sec)

    # ----------------------------
    # Page 2: Meal Recipes
    # ----------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meal Recipes", ln=True, align="C")
    pdf.ln(5)

    meal_recipes = {
        "Spaghetti Bolognese": {
            "batch": 90,
            "ingredients": {
                "Beef Mince": 100,
                "Napoli Sauce": 65,
                "Crushed Tomatoes": 45,
                "Beef Stock": 30,
                "Onion": 15,
                "Zucchini": 15,
                "Carrot": 15,
                "Vegetable Oil": 1,
                "Salt": 2,
                "Pepper": 0.5,
                "Spaghetti": 68
            }
        },
       "Beef Chow Mein": {
        "batch": 80,
        "ingredients": {
        "Beef Mince": 120,
        "Celery": 42,
        "Carrot": 42,
        "Cabbage": 42,
        "Onion": 42,
        "Oil": 2,
        "Pepper": 0.8,
        "Soy Sauce": 13,
        "Oyster Sauce": 13,
        "Rice": 130
    }
           
},
        "Shepherd's Pie": {
    "batch": 82,
    "ingredients": {
        "Beef Mince": 100,
        "Oil": 2,
        "Carrots": 15,
        "Capsicum": 15,
        "Onion": 15,
        "Mushroom": 15,
        "Peas": 15,
        "Tomato Paste": 6,
        "Beef Stock": 20,
        "Salt": 2,
        "Pepper": 0.5,
        "Napoli Sauce": 70
    }
},
        "Beef Burrito Bowl": {
    "batch": 130,
    "ingredients": {
        "Beef Mince": 95,
        "Onion": 12,
        "Capsicum": 12,
        "Vegetable Oil": 2,
        "Taco Seasoning": 7,
        "Salt": 1.5,
        "Pepper": 0.5,
        "Beef Stock": 40
    }
},
        "Beef Meatballs": {
    "batch": 0,
    "ingredients": {
        "Mince": 150,
        "Onion": 10,
        "Parsley": 3,
        "Salt": 1.5,
        "Pepper": 0.2
    }
        },
        "Lebanese Beef Stew": {
    "batch": 80,
    "ingredients": {
        "Chuck Diced": 97,
        "Onion": 30,
        "Carrot": 30,
        "Potato": 30,
        "Peas": 30,
        "Oil": 2,
        "Salt": 2.5,
        "Pepper": 0.5,
        "Tomato Paste": 20,
        "Water": 30,
        "Beef Stock": 30,
        "Rice": 130
    }
},
        "Mongolian Beef": {
    "batch": 0,
    "ingredients": {
        "Chuck": 97,
        "Baking Soda": 2.5,
        "Water": 10,
        "Soy Sauce": 5,
        "Cornflour": 2.5
    }
},
     "Chicken With Vegetables": {
    "batch": 0,
    "ingredients": {
        "Chicken": 135,
        "Corn": 52,
        "Beans": 60,
        "Broccoli": 67
    }
},
        "Chicken Sweet Potato and Beans": {
    "batch": 0,
    "ingredients": {
        "Chicken": 135,
        "Beans": 60
    }
},
"Naked Chicken Parma": {
    "batch": 0,
    "ingredients": {
        "Chicken": 150
    }
},
        "Chicken Pesto Pasta": {
    "batch": 0,
    "ingredients": {
        "Chicken": 130,
        "Penne": 59,
        "Sundried Tomatos": 24
    }
},
        "Chicken and Broccoli Pasta": {
    "batch": 0,
    "ingredients": {
        "Chicken": 130,
        "Penne": 59,
        "Broccoli": 40
    }
},
"Butter Chicken": {
    "batch": 0,
    "ingredients": {
        "Chicken": 140,
        "Peas": 40,
        "Rice": 130
    }
},
"Thai Green Chicken Curry": {
    "batch": 0,
    "ingredients": {
        "Chicken": 140,
        "Rice": 130
    }
},
        "Moroccan Chicken": {
    "batch": 0,
    "ingredients": {
        "Chicken": 180
    },
    "sub_section": {
        "title": "Chickpea Recipe",
        "ingredients": {
            "Onion": 20,
            "Zucchini": 30,
            "Red Capsicum": 30,
            "Garlic": 2,
            "Oil": 2,
            "Chickpeas": 115,
            "Mix Spices": 1.7,
            "Chicken Stock": 50
        }
    }

    meal_column_heights = [pdf.get_y(), pdf.get_y()]
    meal_current_column = 0

    def draw_meal(column_index, name, data):
        x = column_x[column_index]
        y = meal_column_heights[column_index]
        pdf.set_xy(x, y)

        total_meals = meal_totals.get(name.upper(), 0)
        batches = math.ceil(total_meals / data.get("batch", 0)) if data.get("batch", 0) > 0 else ""

        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(col_width, cell_height, name, ln=1, fill=True)

        pdf.set_x(x)
        pdf.set_font("Arial", "B", 8)
        pdf.cell(col_width * 0.3, cell_height, "Ingredient", 1)
        pdf.cell(col_width * 0.15, cell_height, "Qty/Meal", 1)
        pdf.cell(col_width * 0.15, cell_height, "Meals", 1)
        pdf.cell(col_width * 0.25, cell_height, "Batch Total", 1)
        pdf.cell(col_width * 0.15, cell_height, "Batches", 1)
        pdf.ln(cell_height)

        pdf.set_font("Arial", "", 8)
        for i, (ing, qty) in enumerate(data.get("ingredients", {}).items()):
            total_qty = qty * total_meals
            num_batches = math.ceil(total_meals / data.get("batch", 0)) if data.get("batch", 0) > 0 else 0
            batch_total = round(total_qty / num_batches) if num_batches > 0 else 0
            batch_label = str(batches) if i == 0 else ""

            pdf.set_x(x)
            pdf.cell(col_width * 0.3, cell_height, ing[:20], 1)
            pdf.cell(col_width * 0.15, cell_height, str(qty), 1)
            pdf.cell(col_width * 0.15, cell_height, str(total_meals), 1)
            pdf.cell(col_width * 0.25, cell_height, str(batch_total), 1)
            pdf.cell(col_width * 0.15, cell_height, batch_label, 1)
            pdf.ln(cell_height)

        meal_column_heights[column_index] = pdf.get_y() + padding_after_table

    for meal_name, data in meal_recipes.items():
        estm = meal_column_heights[meal_current_column] + (len(data.get("ingredients", {})) + 3) * cell_height
        if estm > 270:
            meal_current_column = 1 - meal_current_column
        draw_meal(meal_current_column, meal_name, data)

    # ----------------------------
    # Page 3: Sauces Requirements
    # ----------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Sauces Requirements", ln=True, align="C")
    pdf.ln(5)

    # Aggregate all sauce-type ingredients from recipes
    sauce_totals = {}
    for name, data in meal_recipes.items():
        total_meals = meal_totals.get(name.upper(), 0)
        for ing, qty in data.get("ingredients", {}).items():
            if "sauce" in ing.lower():
                sauce_totals[ing] = sauce_totals.get(ing, 0) + qty * total_meals

    # Table header
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_width * 0.5, cell_height, "Sauce", 1)
    pdf.cell(col_width * 0.5, cell_height, "Total Quantity", 1)
    pdf.ln(cell_height)

    pdf.set_font("Arial", "", 8)
    for sauce, total_qty in sauce_totals.items():
        pdf.cell(col_width * 0.5, cell_height, sauce[:20], 1)
        pdf.cell(col_width * 0.5, cell_height, str(total_qty), 1)
        pdf.ln(cell_height)

    # Output PDF
    filename_date = datetime.today().strftime("%d-%m-%Y")
    pdf_path = f"daily_production_report_{filename_date}.pdf"
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button("\U0001F4C4 Download Bulk Order PDF", f, file_name=pdf_path, mime="application/pdf")
