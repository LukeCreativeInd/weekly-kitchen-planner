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

# ---- PHASE 2: Select production date ----
selected_date = st.date_input(
    "Production Date (used in filename and PDF)", 
    value=datetime.today()
)
selected_date_header = selected_date.strftime('%d/%m/%Y')
selected_date_file = selected_date.strftime('%Y-%m-%d')

# ---- Show all previously generated reports ----
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

all_reports = sorted([f for f in os.listdir(REPORTS_DIR) if f.endswith('.pdf')], reverse=True)
search_q = st.text_input("Search previous reports (by filename/date):")
filtered_reports = [f for f in all_reports if search_q.lower() in f.lower()]

st.markdown("#### Previous Production Reports")
if filtered_reports:
    for report in filtered_reports:
        with open(os.path.join(REPORTS_DIR, report), "rb") as f:
            st.download_button(f"📄 {report}", f, file_name=report, mime="application/pdf")
else:
    st.info("No previous reports found (or none match search).")

st.divider()

# ---- File Uploaders for all brands ----
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

# ---- Calculate brand totals table for reporting ----
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

# For recipe/section processing
all_meal_totals = dict(all_df.groupby("product name")["quantity"].sum().items())

# ---- Generate PDF only if requested ----
if st.button("Generate and Save PDF Report"):
    pdf = FPDF()
    pdf.set_auto_page_break(False)
    a4_w, a4_h = 210, 297
    left = 10
    page_w = a4_w - 2 * left
    col_w = page_w / 2 - 5
    ch, pad, bottom = 6, 4, a4_h - 17
    xpos = [left, left + col_w + 10]

    # 1. Brand summary table
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Meal Totals by Brand - {selected_date_header}", ln=1, align='C')
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

    # 2. All sections (using all_meal_totals as before)
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

    # 3. Save PDF and present download button
    fname = f"daily_production_report_{selected_date_file}.pdf"
    path = os.path.join(REPORTS_DIR, fname)
    pdf.output(path)

    with open(path, "rb") as f:
        st.success(f"PDF saved as {fname}")
        st.download_button("📄 Download Bulk Order PDF", f, file_name=fname, mime="application/pdf")
