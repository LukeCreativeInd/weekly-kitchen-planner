import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os
import glob
import io

from bulk_section import draw_bulk_section
from recipes_section import draw_recipes_section
from sauces_section import draw_sauces_section
from fridge_section import draw_fridge_section
from chicken_mixing_section import draw_chicken_mixing_section
from meat_veg_section import draw_meat_veg_section

# --- Config & Constants ---
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# --- Utility Functions ---
def load_uploaded_file(label):
    return st.file_uploader(f"Upload {label} (CSV or Excel)", type=["csv", "xlsx"], key=label)

def parse_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()
    # Defensive: normalise column headers, check required columns
    if not {"product name", "quantity"}.issubset(df.columns):
        st.error(f"{uploaded_file.name} must contain 'Product name' and 'Quantity'")
        return None
    return df

def merge_meal_totals(*dfs):
    totals = {}
    for df in dfs:
        if df is not None:
            for _, row in df.iterrows():
                key = str(row["product name"]).strip().upper()
                qty = row["quantity"] if pd.notnull(row["quantity"]) else 0
                try:
                    qty = int(qty)
                except Exception:
                    qty = 0
                totals[key] = totals.get(key, 0) + qty
    return totals

def summary_table(meal_keys, clean, made, elite, total):
    data = []
    for meal in meal_keys:
        data.append({
            "Meal": meal,
            "Clean Eats": clean.get(meal, 0),
            "Made Active": made.get(meal, 0),
            "Elite Meals": elite.get(meal, 0),
            "Total": total.get(meal, 0),
        })
    return pd.DataFrame(data)

def save_pdf_report(pdf_buffer, date_str):
    fname = f"daily_production_report_{date_str}.pdf"
    fpath = os.path.join(REPORTS_DIR, fname)
    with open(fpath, "wb") as f:
        f.write(pdf_buffer.getbuffer())
    return fpath

def list_reports():
    files = glob.glob(os.path.join(REPORTS_DIR, "*.pdf"))
    files = sorted(files, reverse=True)
    return files

# --- Streamlit UI ---
st.title("Bulk Ingredient Summary Report")

# 1–3 file uploads (optionally upload just one!)
st.markdown("#### Upload Meal Production Files")
uploaded_clean = load_uploaded_file("Clean Eats")
uploaded_made = load_uploaded_file("Made Active")
uploaded_elite = load_uploaded_file("Elite Meals")

# 1. **Upload Date Selection**
selected_date = st.date_input("Production Date", value=datetime.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

# Process uploaded files
if all(df is None for df in dfs):
    st.info("Please upload at least one file.")
    st.stop()

# Build meal totals for each file (dict: MEAL NAME (upper) → qty)
meal_totals_clean = {}
meal_totals_made = {}
meal_totals_elite = {}
if dfs[0] is not None:
    meal_totals_clean = {str(row["product name"]).strip().upper(): int(row["quantity"]) for _, row in dfs[0].iterrows()}
if dfs[1] is not None:
    meal_totals_made = {str(row["product name"]).strip().upper(): int(row["quantity"]) for _, row in dfs[1].iterrows()}
if dfs[2] is not None:
    meal_totals_elite = {str(row["product name"]).strip().upper(): int(row["quantity"]) for _, row in dfs[2].iterrows()}

# Combine totals
all_meals = set(meal_totals_clean) | set(meal_totals_made) | set(meal_totals_elite)
meal_totals_total = {meal: meal_totals_clean.get(meal, 0) + meal_totals_made.get(meal, 0) + meal_totals_elite.get(meal, 0) for meal in all_meals}

# For summary display, build table (sorted by Total desc)
summary_df = summary_table(
    sorted(all_meals, key=lambda k: meal_totals_total[k], reverse=True),
    meal_totals_clean, meal_totals_made, meal_totals_elite, meal_totals_total
)
st.markdown("#### Meal Totals by Brand")
st.dataframe(summary_df, use_container_width=True)

# ---- Generate PDF Button ----
generate = st.button("Generate Daily Production PDF")
if generate:
    pdf = FPDF()
    pdf.set_auto_page_break(False)
    a4_w, a4_h = 210, 297
    left = 10
    page_w = a4_w - 2*left
    col_w = page_w/2 - 5
    ch, pad, bottom = 6, 4, a4_h - 17
    xpos = [left, left + col_w + 10]

    # -- Draw summary table at top of PDF --
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Daily Production Report - {selected_date.strftime('%d/%m/%Y')}", ln=1, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(col_w, ch, "Meal", 1)
    pdf.cell(col_w*0.4, ch, "Clean Eats", 1)
    pdf.cell(col_w*0.4, ch, "Made Active", 1)
    pdf.cell(col_w*0.4, ch, "Elite Meals", 1)
    pdf.cell(col_w*0.4, ch, "Total", 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 10)
    for _, row in summary_df.iterrows():
        pdf.cell(col_w, ch, str(row["Meal"]), 1)
        pdf.cell(col_w*0.4, ch, str(row["Clean Eats"]), 1)
        pdf.cell(col_w*0.4, ch, str(row["Made Active"]), 1)
        pdf.cell(col_w*0.4, ch, str(row["Elite Meals"]), 1)
        pdf.cell(col_w*0.4, ch, str(row["Total"]), 1)
        pdf.ln(ch)

    # ---- Pass only total dict to all other section functions! ----
    last_y = pdf.get_y() + 8  # leave some space below summary table
    last_y = draw_bulk_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y, header_date=selected_date.strftime('%d/%m/%Y'))
    pdf.set_y(last_y)
    last_y = draw_recipes_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_sauces_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_fridge_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_chicken_mixing_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_meat_veg_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)

    # ---- Save & Download PDF ----
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    saved_path = save_pdf_report(pdf_buffer, selected_date_str)
    st.success(f"Report saved: {saved_path}")

    st.download_button(
        label="📄 Download Daily Production PDF",
        data=pdf_buffer.getvalue(),
        file_name=os.path.basename(saved_path),
        mime="application/pdf"
    )

# -------- Show Previous Reports (Search below UI) --------
st.markdown("----")
st.markdown("### Previous Daily Production Reports")
search_query = st.text_input("Search previous reports by date (YYYY-MM-DD):", "")
report_files = list_reports()
if search_query:
    report_files = [f for f in report_files if search_query in os.path.basename(f)]
if report_files:
    for f in report_files:
        st.markdown(f"[{os.path.basename(f)}]({f})")
else:
    st.info("No previous reports found.")

