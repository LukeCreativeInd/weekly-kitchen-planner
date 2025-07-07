import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime
from io import BytesIO

from bulk_section import draw_bulk_section, bulk_sections
from recipes_section import draw_recipes_section, meal_recipes
from sauces_section import draw_sauces_section
from fridge_section import draw_fridge_section
from chicken_mixing_section import draw_chicken_mixing_section
from meat_veg_section import draw_meat_veg_section

# --- CONFIG ---
st.set_page_config(page_title="Product Quantity Summary", layout="centered")
previous_reports_dir = "previous_reports"
os.makedirs(previous_reports_dir, exist_ok=True)

# --- DATE SELECTOR ---
today = datetime.today().date()
selected_date = st.date_input("Production Date", today)
selected_date_header = selected_date.strftime('%d/%m/%Y')
fname = f"daily_production_report_{selected_date.strftime('%d-%m-%Y')}.pdf"
report_path = os.path.join(previous_reports_dir, fname)

# --- PREVIOUS REPORTS SEARCH ---
st.markdown("### 📂 Previous Reports")
search_query = st.text_input("Search reports by filename or date", "")
all_reports = sorted(os.listdir(previous_reports_dir), reverse=True)
filtered_reports = [
    f for f in all_reports if search_query.lower() in f.lower()
]
if filtered_reports:
    for report_file in filtered_reports:
        st.write(
            f"📄 [{report_file}]({os.path.join(previous_reports_dir, report_file)})"
        )
else:
    st.write("No previous reports found matching your search.")

# --- FILE UPLOAD ---
st.markdown("### 📝 Generate New Report")
uploaded_file = st.file_uploader("Upload Production File (CSV or Excel)", type=["csv", "xlsx"])
if not uploaded_file:
    st.stop()

# Read data
if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file)

# Validate
df.columns = df.columns.str.strip().str.lower()
if not {"product name", "quantity"}.issubset(df.columns):
    st.error("CSV must contain 'Product name' and 'Quantity'")
    st.stop()

st.dataframe(df)
meal_totals = dict(zip(df["product name"].str.upper(), df["quantity"]))

# --- PDF GENERATION ---
pdf = FPDF()
pdf.set_auto_page_break(False)
a4_w, a4_h = 210, 297
left = 10
page_w = a4_w - 2 * left
col_w = page_w / 2 - 5
ch, pad, bottom = 6, 4, a4_h - 17
xpos = [left, left + col_w + 10]

# Draw all sections in order, tracking Y position throughout
last_y = draw_bulk_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, header_date=selected_date_header)
pdf.set_y(last_y)
last_y = draw_recipes_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
pdf.set_y(last_y)
last_y = draw_sauces_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
pdf.set_y(last_y)
last_y = draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
pdf.set_y(last_y)
last_y = draw_chicken_mixing_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y)
pdf.set_y(last_y)
last_y = draw_meat_veg_section(pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=last_y)
pdf.set_y(last_y)

# --- PDF IN MEMORY FOR DOWNLOAD ---
pdf_buffer = BytesIO()
pdf.output(pdf_buffer)
pdf_buffer.seek(0)

# --- DOWNLOAD & SAVE ONLY IF DOWNLOADED ---
if st.download_button(
    "📄 Download Bulk Order PDF",
    pdf_buffer,
    file_name=fname,
    mime="application/pdf"
):
    # Save to previous_reports folder ONLY if downloaded
    with open(report_path, "wb") as f:
        f.write(pdf_buffer.getvalue())
    st.success(f"Report saved as {fname}")

