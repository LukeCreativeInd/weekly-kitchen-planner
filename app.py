import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

from bulk_section import draw_bulk_section, bulk_sections
from recipes_section import draw_recipes_section, meal_recipes
from sauces_section import draw_sauces_section
from fridge_section import draw_fridge_section
from chicken_mixing_section import draw_chicken_mixing_section
from meat_veg_section import draw_meat_veg_section

st.set_page_config(page_title="📦 Bulk Ingredient Summary Report", layout="wide")

st.title("📦 Bulk Ingredient Summary Report (All Brands)")

# Multi-file uploader for the three brands
uploaded_clean = st.file_uploader("Upload Clean Eats File", type=["csv", "xlsx"], key="clean")
uploaded_made = st.file_uploader("Upload Made Active File", type=["csv", "xlsx"], key="made")
uploaded_elite = st.file_uploader("Upload Elite Meals File", type=["csv", "xlsx"], key="elite")

# Collect and combine data
dfs = []
brand_names = []
if uploaded_clean:
    df_clean = pd.read_csv(uploaded_clean) if uploaded_clean.name.endswith(".csv") else pd.read_excel(uploaded_clean)
    df_clean.columns = df_clean.columns.str.strip().str.lower()
    df_clean["Brand"] = "Clean Eats"
    dfs.append(df_clean)
    brand_names.append("Clean Eats")
if uploaded_made:
    df_made = pd.read_csv(uploaded_made) if uploaded_made.name.endswith(".csv") else pd.read_excel(uploaded_made)
    df_made.columns = df_made.columns.str.strip().str.lower()
    df_made["Brand"] = "Made Active"
    dfs.append(df_made)
    brand_names.append("Made Active")
if uploaded_elite:
    df_elite = pd.read_csv(uploaded_elite) if uploaded_elite.name.endswith(".csv") else pd.read_excel(uploaded_elite)
    df_elite.columns = df_elite.columns.str.strip().str.lower()
    df_elite["Brand"] = "Elite Meals"
    dfs.append(df_elite)
    brand_names.append("Elite Meals")

if not dfs:
    st.warning("Upload at least one production file to continue.")
    st.stop()

all_df = pd.concat(dfs, ignore_index=True)
all_df["product name"] = all_df["product name"].str.strip()

# Calculate brand totals table
brands = ["Clean Eats", "Made Active", "Elite Meals"]
meals = sorted(all_df["product name"].unique())
table_data = []
for meal in meals:
    row = [meal]
    total = 0
    for brand in brands:
        val = all_df.loc[(all_df["product name"] == meal) & (all_df["Brand"] == brand), "quantity"].sum()
        row.append(int(val))
        total += int(val)
    row.append(total)
    table_data.append(row)

table_columns = ["Meal"] + brands + ["Total"]
summary_df = pd.DataFrame(table_data, columns=table_columns)
st.markdown("### Meal Totals by Brand")
st.dataframe(summary_df, use_container_width=True)

# Convert brand totals to dict for recipe processing
all_meal_totals = dict(all_df.groupby("product name")["quantity"].sum().items())

# Set up PDF
pdf = FPDF()
pdf.set_auto_page_break(False)
a4_w, a4_h = 210, 297
left = 10
page_w = a4_w - 2 * left
col_w = page_w / 2 - 5
ch, pad, bottom = 6, 4, a4_h - 17
xpos = [left, left + col_w + 10]

# --- NEW: Write summary table to PDF ---
pdf.add_page()
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, f"Meal Totals by Brand - {datetime.today().strftime('%d/%m/%Y')}", ln=1, align='C')
pdf.ln(3)
pdf.set_font("Arial", "B", 10)
pdf.set_fill_color(230, 230, 230)
for i, col in enumerate(table_columns):
    w = col_w * 1.2 if i == 0 else col_w * 0.5
    pdf.cell(w, ch, col, 1, fill=True)
pdf.ln(ch)
pdf.set_font("Arial", "", 10)
for row in table_data:
    for i, val in enumerate(row):
        w = col_w * 1.2 if i == 0 else col_w * 0.5
        pdf.cell(w, ch, str(val), 1)
    pdf.ln(ch)
pdf.ln(5)

# --- Draw the rest of the sections ---
last_y = pdf.get_y()
last_y = draw_bulk_section(pdf, all_meal_totals, xpos, col_w, ch, pad, bottom)
pdf.set_y(last_y)
last_y = draw_recipes_section(pdf, all_meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
pdf.set_y(last_y)
last_y = draw_sauces_section(pdf, all_meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
pdf.set_y(last_y)
last_y = draw_fridge_section(pdf, all_meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
pdf.set_y(last_y)
last_y = draw_chicken_mixing_section(pdf, all_meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
pdf.set_y(last_y)
last_y = draw_meat_veg_section(pdf, all_meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=last_y)

# --- Download button ---
fname = f"daily_production_report_{datetime.today().strftime('%Y-%m-%d')}.pdf"
pdf.output(fname)
with open(fname, "rb") as f:
    st.download_button("📄 Download Bulk Order PDF", f, file_name=fname, mime="application/pdf")
