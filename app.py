import streamlit as st
import pandas as pd
from datetime import date
import os
from io import BytesIO
from fpdf import FPDF

from bulk_section import draw_bulk_section, bulk_sections
from recipes_section import draw_recipes_section, meal_recipes
from sauces_section import draw_sauces_section
from fridge_section import draw_fridge_section
from chicken_mixing_section import draw_chicken_mixing_section
from meat_veg_section import draw_meat_veg_section

st.set_page_config(page_title="Kitchen Planner", layout="centered")

# --- PRODUCTION DATE PICKER ---
selected_date = st.date_input("Production Date", value=date.today())
selected_date_header = selected_date.strftime("%Y/%m/%d")
selected_date_file = selected_date.strftime("%Y-%m-%d")

# --- GENERATE NEW REPORT ---
st.markdown("## 📝 Generate New Report")
uploaded_file = st.file_uploader("Upload Production File (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # --- READ FILE ---
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # --- NORMALISE COLUMNS ---
    df.columns = df.columns.str.strip().str.lower()
    if not {"product name", "quantity"}.issubset(df.columns):
        st.error("CSV must contain 'Product name' and 'Quantity'")
        st.stop()

    st.dataframe(df)
    meal_totals = dict(zip(df["product name"].str.upper(), df["quantity"]))

    # --- SETUP PDF ---
    pdf = FPDF()
    pdf.set_auto_page_break(False)
    a4_w, a4_h = 210, 297
    left = 10
    page_w = a4_w - 2*left
    col_w = page_w/2 - 5
    ch, pad, bottom = 6, 4, a4_h - 17
    xpos = [left, left + col_w + 10]

    # --- DRAW ALL SECTIONS ---
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
    last_y = draw_meat_veg_section(
        pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=last_y
    )
    pdf.set_y(last_y)

    # --- PDF SAVE & DOWNLOAD BUTTON ---
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    pdf_buffer = BytesIO(pdf_bytes)
    fname = f"daily_production_report_{selected_date_file}.pdf"
    reports_dir = "previous_reports"
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, fname)

    if st.download_button(
        "📄 Download Bulk Order PDF",
        pdf_buffer,
        file_name=fname,
        mime="application/pdf"
    ):
        # Only save the PDF if the user clicks download
        with open(report_path, "wb") as f:
            f.write(pdf_bytes)
        st.success(f"Report saved to: {report_path}")

# --- PREVIOUS REPORTS SECTION ---
st.markdown("## 📂 Previous Reports")
st.caption("Search reports by filename or date")

reports_dir = "previous_reports"
search_query = st.text_input("Search reports by filename or date", "")

report_files = []
if os.path.isdir(reports_dir):
    for fn in sorted(os.listdir(reports_dir), reverse=True):
        if fn.lower().endswith(".pdf"):
            if search_query.strip().lower() in fn.lower():
                report_files.append(fn)

if report_files:
    for fn in report_files:
        fpath = os.path.join(reports_dir, fn)
        with open(fpath, "rb") as f:
            st.download_button(
                f"Download {fn}",
                f.read(),
                file_name=fn,
                mime="application/pdf",
                key=f"download_{fn}"
            )
else:
    st.write("No previous reports found matching your search.")

# --- END ---
