import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

from recipes_section import draw_recipes_section, meal_recipes
from bulk_section import draw_bulk_section, bulk_sections
from sauces_section import draw_sauces_section
from fridge_section import draw_fridge_section
from chicken_mixing_section import draw_chicken_mixing_section
from meat_veg_section import draw_meat_veg_section

REPORTS_DIR = "production_reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

st.title("📦 Bulk Ingredient Summary Report")

# --- Date picker ---
selected_date = st.date_input(
    "Production date (for report heading & saving)",
    value=datetime.today()
)
selected_date_header = selected_date.strftime('%d/%m/%Y')

# --- File uploaders ---
st.markdown("### Upload meal quantity files for each brand (at least one required)")
uploaded_clean = st.file_uploader("Upload Clean Eats file", type=["csv", "xlsx"], key="clean")
uploaded_made = st.file_uploader("Upload Made Active file", type=["csv", "xlsx"], key="made")
uploaded_elite = st.file_uploader("Upload Elite Meals file", type=["csv", "xlsx"], key="elite")

brand_files = [
    ("Clean Eats", uploaded_clean),
    ("Made Active", uploaded_made),
    ("Elite Meals", uploaded_elite)
]
dfs = []
meal_brand_maps = []

for brand, file in brand_files:
    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        df.columns = df.columns.str.strip().str.lower()
        if not {"product name", "quantity"}.issubset(df.columns):
            st.error(f"{brand} file must contain 'Product name' and 'Quantity'")
            st.stop()
        dfs.append(df)
        meal_brand_maps.append(dict(zip(df["product name"].str.upper(), df["quantity"])))
    else:
        dfs.append(None)
        meal_brand_maps.append({})

if all(df is None for df in dfs):
    st.warning("Please upload at least one file to proceed.")
    st.stop()

# Get all unique product names (for summary table)
all_meal_names = set()
for df in dfs:
    if df is not None:
        all_meal_names.update(df["product name"].str.upper())

# Build summary table (Meal | Clean | Made | Elite | Total)
summary_rows = []
for meal in sorted(all_meal_names):
    ce = meal_brand_maps[0].get(meal, 0)
    ma = meal_brand_maps[1].get(meal, 0)
    el = meal_brand_maps[2].get(meal, 0)
    total = ce + ma + el
    summary_rows.append({
        "Meal": meal.title(),
        "Clean Eats": ce,
        "Made Active": ma,
        "Elite Meals": el,
        "Total": total
    })
summary_df = pd.DataFrame(summary_rows)

# Use combined totals for all recipe calculations
meal_totals_total = {row["Meal"].upper(): row["Total"] for row in summary_rows}

# --- Display the summary table ---
st.markdown("### Quantity Summary Table")
st.dataframe(summary_df, hide_index=True)

# ---- PDF creation ----
if st.button("Generate & Save Production Report PDF"):
    pdf = FPDF()
    pdf.set_auto_page_break(False)
    a4_w, a4_h = 210, 297
    left = 10
    page_w = a4_w - 2 * left
    col_w = page_w / 2 - 5
    ch, pad, bottom = 6, 4, a4_h - 17
    xpos = [left, left + col_w + 10]

    # --- Summary Table as First Page ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Production Summary ({selected_date_header})", ln=1, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    th = 8
    col_widths = [70, 25, 25, 25, 25]  # Make first col wider for full meal names
    for i, col in enumerate(summary_df.columns):
        pdf.cell(col_widths[i], th, col, border=1)
    pdf.ln(th)
    pdf.set_font("Arial", "", 10)
    for _, row in summary_df.iterrows():
        pdf.cell(col_widths[0], th, str(row["Meal"]), border=1)
        pdf.cell(col_widths[1], th, str(row["Clean Eats"]), border=1)
        pdf.cell(col_widths[2], th, str(row["Made Active"]), border=1)
        pdf.cell(col_widths[3], th, str(row["Elite Meals"]), border=1)
        pdf.cell(col_widths[4], th, str(row["Total"]), border=1)
        pdf.ln(th)

    # --- Draw all report sections on subsequent pages ---
    last_y = draw_bulk_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=None, header_date=selected_date_header)
    pdf.set_y(last_y)
    last_y = draw_recipes_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_sauces_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_fridge_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_chicken_mixing_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_meat_veg_section(pdf, meal_totals_total, meal_recipes, bulk_sections, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)

    fname = f"daily_production_report_{selected_date}.pdf"
    save_path = os.path.join(REPORTS_DIR, fname)
    pdf.output(save_path)
    with open(save_path, "rb") as f:
        st.download_button("📄 Download Bulk Order PDF", f, file_name=fname, mime="application/pdf")
    st.success(f"Report saved as {fname}!")

# ---- Previous reports section BELOW upload ----
st.markdown("---")
st.markdown("## Previous Reports")
search_query = st.text_input("Search previous reports by date or keyword").lower()
report_files = sorted([f for f in os.listdir(REPORTS_DIR) if f.endswith(".pdf")], reverse=True)
filtered_reports = [f for f in report_files if search_query in f.lower()]
if filtered_reports:
    for rep in filtered_reports:
        rep_path = os.path.join(REPORTS_DIR, rep)
        with open(rep_path, "rb") as f:
            st.download_button(f"Download {rep}", f, file_name=rep, mime="application/pdf")
else:
    st.info("No previous reports found.")
