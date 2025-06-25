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
    {"title": "Sweet Potato Mash", "batch_ingredient": "Sweet Potato", "batch_size": 0, "ingredients": {"Sweet Potato": 185, "Salt": 1, "White Pepper": 0.5}, "meals": ["Shepherd's Pie", "Chicken Sweet Potato and Beans"]},
    {"title": "Roasted Potatoes", "batch_ingredient": "Roasted Potatoes", "batch_size": 60, "ingredients": {"Roasted Potatoes": 190, "Oil": 1, "Spices Mix": 2.5}, "meals": []},
    {"title": "Roasted Lemon Potatoes", "batch_ingredient": "Potatoes", "batch_size": 60, "ingredients": {"Potatoes": 207, "Oil": 1, "Salt": 1.2}, "meals": ["Roasted Lemon Chicken"]},
    {"title": "Roasted Thai Potatoes", "batch_ingredient": "Potato", "batch_size": 0, "ingredients": {"Potato": 60, "Salt": 1}, "meals": ["Thai Green Chicken Curry"]},
    {"title": "Lamb Onion Marinated", "batch_ingredient": "Red Onion", "batch_size": 0, "ingredients": {"Red Onion": 30, "Parsley": 1.5, "Paprika": 0.5}, "meals": ["Lamb Souvlaki"]},
    {"title": "Green Beans", "batch_ingredient": "Green Beans", "batch_size": 0, "ingredients": {"Green Beans": 60}, "meals": ["Chicken with Vegetables", "Chicken Sweet Potato and Beans", "Steak with Mushroom Sauce"]}
]

# ----------------------------
# Streamlit App
# ----------------------------
st.title("📦 Bulk Ingredient Summary Report")
uploaded_file = st.file_uploader("Upload Production File (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Read and validate data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()
    if not {"product name", "quantity"}.issubset(df.columns):
        st.error("CSV must contain 'Product name' and 'Quantity'")
        st.stop()
    st.success("File uploaded successfully!")
    st.dataframe(df)
    meal_totals = dict(zip(df["product name"].str.upper(), df["quantity"]))

    # PDF setup
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)
    left, page_w = 10, 210 - 20
    col_w = page_w / 2 - 5
    ch, pad, bottom = 6, 4, 280
    xpos = [left, left + col_w + 10]

    # ------------------
    # Page1: Bulk Summary
    # ------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Daily Production Report - {datetime.today().strftime('%d/%m/%Y')}", ln=1, align='C')
    pdf.ln(5)
    heights = [pdf.get_y(), pdf.get_y()]
    col = 0

    def draw_bulk(idx, sec):
        x, y = xpos[idx], heights[idx]
        pdf.set_xy(x, y)
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(col_w, ch, sec['title'], ln=1, fill=True)
        pdf.set_x(x)
        pdf.set_font("Arial", "B", 8)
        for h, w in [("Ingredient", 0.4), ("Qty/Meal", 0.15), ("Meals", 0.15), ("Total", 0.15), ("Batches", 0.15)]:
            pdf.cell(col_w * w, ch, h, 1)
        pdf.ln(ch)
        pdf.set_font("Arial", "", 8)
        totm = sum(meal_totals.get(m.upper(), 0) for m in sec['meals'])
        batches = math.ceil(totm / sec['batch_size']) if sec['batch_size'] > 0 else 0
        for ingr, per in sec['ingredients'].items():
            total_qty = per * totm
            adj = round(total_qty / batches) if batches else round(total_qty, 2)
            lbl = str(batches) if ingr == sec['batch_ingredient'] else ""
            pdf.set_x(x)
            pdf.cell(col_w * 0.4, ch, ingr[:20], 1)
            pdf.cell(col_w * 0.15, ch, str(per), 1)
            pdf.cell(col_w * 0.15, ch, str(totm), 1)
            pdf.cell(col_w * 0.15, ch, str(adj), 1)
            pdf.cell(col_w * 0.15, ch, lbl, 1)
            pdf.ln(ch)
        heights[idx] = pdf.get_y() + pad

    for sec in bulk_sections:
        block_h = (len(sec['ingredients']) + 2) * ch + pad
        if heights[col] + block_h > bottom:
            if col == 0:
                col = 1
            else:
                pdf.add_page()
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Daily Production Report - Continued", ln=1, align='C')
                pdf.ln(5)
                y0 = pdf.get_y()
                heights = [y0, y0]
                col = 0
        draw_bulk(col, sec)

    # ------------------
    # Page2: Meal Recipes
    # ------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Meal Recipes", ln=1, align='C')
    pdf.ln(5)
    meal_recipes = {
        # ... (existing recipes) ...
    }
    heights = [pdf.get_y(), pdf.get_y()]
    col = 0
    def draw_meal(idx, name, data): pass
    # ... (drawing meal recipes) ...

    # ------------------
    # Page3: Sauces
    # ------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Sauces", ln=1, align='C')
    pdf.ln(5)
    sauces = {
        "Thai Sauce": {"ingredients": [("Green Curry Paste", 7), ("Coconut Cream", 82)], "meal_key": "THAI GREEN CHICKEN CURRY"},
        "Lamb Sauce": {"ingredients": [("Greek Yogurt", 20), ("Garlic", 2), ("Salt", 1)], "meal_key": "LAMB SOUVLAKI"}
    }
    heights = [pdf.get_y(), pdf.get_y()]
    col = 0
    def draw_sauce(idx, name, data): pass
    # ... (drawing sauces) ...

    # ------------------
    # Page4: To Pack In Fridge
    # ------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "To Pack In Fridge", ln=1, align='C')
    pdf.ln(5)
    # Table heading
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Sauces to Prepare", ln=1, fill=True)
    pdf.ln(2)
    sauce_prep = [
        ("MONGOLIAN", 70, "MONGOLIAN BEEF"),
        ("MEATBALLS", 120, "BEEF MEATBALLS"),
        ("LEMON", 50, "ROASTED LEMON CHICKEN"),
        ("MUSHROOM", 100, "STEAK WITH MUSHROOM SAUCE"),
        ("FAJITA SAUCE", 33, "CHICKEN FAJITA BOWL"),
        ("BURRITO SAUCE", 43, "BEEF BURRITO BOWL")
    ]
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w*0.4, ch, "Sauce", 1)
    pdf.cell(col_w*0.2, ch, "Quantity", 1)
    pdf.cell(col_w*0.2, ch, "Amount", 1)
    pdf.cell(col_w*0.2, ch, "Total", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    for sauce, qty, meal_key in sauce_prep:
        amount = meal_totals.get(meal_key, 0)
        total = qty * amount
        pdf.cell(col_w*0.4, ch, sauce, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amount), 1)
        pdf.cell(col_w*0.2, ch, str(total), 1)
        pdf.ln(ch)

    # ------------------
    # Chicken Mixing
    # ------------------
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Chicken Mixing", ln=1, align='C')
    pdf.ln(5)
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Pesto", ln=1, fill=True)
    pdf.ln(2)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w*0.3, ch, "Ingredient", 1)
    pdf.cell(col_w*0.2, ch, "Quantity", 1)
    pdf.cell(col_w*0.2, ch, "Amount", 1)
    pdf.cell(col_w*0.2, ch, "Total", 1)
    pdf.cell(col_w*0.15, ch, "Batches", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    amt = meal_totals.get("CHICKEN PESTO PASTA", 0)
    batches = math.ceil(amt/50) if amt>0 else 0
    for ingr, qty in [("Chicken",110),("Sauce",80)]:
        total = (qty*amt)/batches if batches else 0
        pdf.cell(col_w*0.3, ch, ingr, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(total,2)), 1)
        pdf.cell(col_w*0.15, ch, str(batches), 1)
        pdf.ln(ch)

    # ------------------
    # Butter Chicken
    # ------------------
    pdf.ln(5)
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Butter Chicken", ln=1, fill=True)
    pdf.ln(2)
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w*0.3, ch, "Ingredient", 1)
    pdf.cell(col_w*0.2, ch, "Quantity", 1)
    pdf.cell(col_w*0.2, ch, "Amount", 1)
    pdf.cell(col_w*0.2, ch, "Total", 1)
    pdf.cell(col_w*0.15, ch, "Batches", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    amt = meal_totals.get("BUTTER CHICKEN", 0)
    batches = math.ceil(amt/50) if amt>0 else 0
    for ingr, qty in [("Chicken",120),("Sauce",90)]:
        total = (qty*amt)/batches if batches else 0
        pdf.cell(col_w*0.3, ch, ingr, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(total,2)), 1)
        pdf.cell(col_w*0.15, ch, str(batches), 1)
        pdf.ln(ch)

    # ------------------
    # Broccoli Pasta
    # ------------------
    pdf.ln(5)
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Broccoli Pasta", ln=1, fill=True)
    pdf.ln(2)
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w*0.3, ch, "Ingredient", 1)
    pdf.cell(col_w*0.2, ch, "Quantity", 1)
    pdf.cell(col_w*0.2, ch, "Amount", 1)
    pdf.cell(col_w*0.2, ch, "Total", 1)
    pdf.cell(col_w*0.15, ch, "Batches", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    amt = meal_totals.get("CHICKEN AND BROCCOLI PASTA", 0)
    batches = math.ceil(amt/50) if amt>0 else 0
    for ingr, qty in [("Chicken",100),("Sauce",100)]:
        total = (qty*amt)/batches if batches else 0
        pdf.cell(col_w*0.3, ch, ingr, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(total,2)), 1)
        pdf.cell(col_w*0.15, ch, str(batches), 1)
        pdf.ln(ch)

    # ------------------
    # Thai Mixing
    # ------------------
    pdf.ln(5)
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Thai", ln=1, fill=True)
    pdf.ln(2)
    pdf.set_x(left)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(col_w*0.3, ch, "Ingredient", 1)
    pdf.cell(col_w*0.2, ch, "Quantity", 1)
    pdf.cell(col_w*0.2, ch, "Amount", 1)
    pdf.cell(col_w*0.2, ch, "Total", 1)
    pdf.cell(col_w*0.15, ch, "Batches", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)
    amt = meal_totals.get("THAI GREEN CHICKEN CURRY", 0)
    batches = math.ceil(amt/50) if amt>0 else 0
    for ingr, qty in [("Chicken",110),("Sauce",90)]:
        total = (qty*amt)/batches if batches else 0
        pdf.cell(col_w*0.3, ch, ingr, 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(total,2)), 1)
        pdf.cell(col_w*0.15, ch, str(batches), 1)
        pdf.ln(ch)

    # ------------------
    # Save & download
    # ------------------
    fname = f"daily_production_report_{datetime.today().strftime('%d-%m-%Y')}.pdf"
    pdf.output(fname)
    with open(fname, "rb") as f:
        st.download_button("📄 Download Bulk Order PDF", f, file_name=fname, mime="application/pdf")
