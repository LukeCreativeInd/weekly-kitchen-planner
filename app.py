import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

from bulk_section import draw_bulk_section
from recipes_section import draw_recipes_section
from sauces_section import draw_sauces_section
from fridge_section import draw_fridge_section
from chicken_mixing_section import draw_chicken_mixing_section
from meat_veg_section import draw_meat_veg_section

st.title("📦 Bulk Ingredient Summary Report")
uploaded_file = st.file_uploader("Upload Production File (CSV or Excel)", type=["csv","xlsx"])
if not uploaded_file:
    st.stop()

if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file)

df.columns = df.columns.str.strip().str.lower()
if not {"product name","quantity"}.issubset(df.columns):
    st.error("CSV must contain 'Product name' and 'Quantity'")
    st.stop()

st.dataframe(df)
meal_totals = dict(zip(df["product name"].str.upper(), df["quantity"]))

pdf = FPDF()
pdf.set_auto_page_break(False)
a4_w, a4_h = 210, 297
left = 10
page_w = a4_w - 2*left
col_w = page_w/2 - 5
ch, pad, bottom = 6, 4, a4_h - 17
xpos = [left, left + col_w + 10]

# Each section returns last_y
last_y = draw_bulk_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom)
last_y = draw_recipes_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
last_y = draw_sauces_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
last_y = draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
last_y = draw_chicken_mixing_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
draw_meat_veg_section(pdf, xpos, col_w, ch, pad, start_y=last_y)

fname = f"daily_production_report_{datetime.today().strftime('%d-%m-%Y')}.pdf"
pdf.output(fname)
with open(fname, "rb") as f:
    st.download_button("📄 Download Bulk Order PDF", f, file_name=fname, mime="application/pdf")
