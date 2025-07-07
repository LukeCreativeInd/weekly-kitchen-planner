import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime, date
import os
import glob

from bulk_section import draw_bulk_section, bulk_sections
from recipes_section import draw_recipes_section, meal_recipes
from sauces_section import draw_sauces_section
from fridge_section import draw_fridge_section
from chicken_mixing_section import draw_chicken_mixing_section
from meat_veg_section import draw_meat_veg_section

# ---- Directory to save reports ----
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

st.title("📦 Bulk Ingredient Summary Report")

# 1. Date selector
selected_date = st.date_input(
    "Select Production Date",
    value=date.today(),
    format="DD/MM/YYYY"
)
selected_date_str = selected_date.strftime('%Y-%m-%d')
selected_date_header = selected_date.strftime('%d/%m/%Y')

# 2. File uploader
uploaded_file = st.file_uploader("Upload Production File (CSV or Excel)", type=["csv", "xlsx"])
if not uploaded_file:
    st.info("Please upload a production file to generate a report.")
else:
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

    # --- PDF Generation ---
    pdf = FPDF()
    pdf.set_auto_page_break(False)
    a4_w, a4_h = 210, 297
    left = 10
    page_w = a4_w - 2 * left
    col_w = page_w / 2 - 5
    ch, pad, bottom = 6, 4, a4_h - 17
    xpos = [left, left + col_w + 10]

    # Pass the date to the bulk section for title header
    last_y = draw_bulk_section(
        pdf, meal_totals, xpos, col_w, ch, pad, bottom, header_date=selected_date_header
    )
    pdf.set_y(last_y)
    last_y = draw_recipes_section(
        pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y
    )
    pdf.set_y(last_y)
    last_y = draw_sauces_section(
        pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y
    )
    pdf.set_y(last_y)
    last_y = draw_fridge_section(
        pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y
    )
    pdf.set_y(last_y)
    last_y = draw_chicken_mixing_section(
        pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=last_y
    )
    pdf.set_y(last_y)
    last_y = draw_meat_veg_section(
        pdf, meal_totals, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=last_y
    )

    # --- Save PDF ---
    fname = f"production_report_{selected_date_str}.pdf"
    full_path = os.path.join(REPORTS_DIR, fname)
    pdf.output(full_path)

    with open(full_path, "rb") as f:
        st.success(f"Report generated for {selected_date_header}!")
        st.download_button(
            "📄 Download Bulk Order PDF",
            f,
            file_name=fname,
            mime="application/pdf"
        )

# --- Section: List & Search Previous Reports ---
st.markdown("---")
st.header("📁 Previously Generated Reports")

# 3. Search/filter box
search_query = st.text_input("Search for a report (type date, e.g. 2025-07-04 or keywords):", "")

# 4. List all reports (most recent first)
all_reports = sorted(
    glob.glob(os.path.join(REPORTS_DIR, "production_report_*.pdf")),
    reverse=True
)

# Filter by search box
if search_query.strip():
    filtered = [f for f in all_reports if search_query.lower() in os.path.basename(f).lower()]
else:
    filtered = all_reports

if not filtered:
    st.info("No reports found matching your search.")
else:
    for f in filtered:
        basename = os.path.basename(f)
        date_part = basename.replace("production_report_", "").replace(".pdf", "")
        display_date = datetime.strptime(date_part, "%Y-%m-%d").strftime('%d/%m/%Y')
        with open(f, "rb") as pdf_file:
            st.download_button(
                label=f"Download {display_date}",
                data=pdf_file,
                file_name=basename,
                mime="application/pdf",
                key=basename
            )

# --- END OF APP ---
