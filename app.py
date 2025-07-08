import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os
import pickle

from bulk_section import draw_bulk_section
from recipes_section import draw_recipes_section, meal_recipes
from sauces_section import draw_sauces_section
from fridge_section import draw_fridge_section
from chicken_mixing_section import draw_chicken_mixing_section
from meat_veg_section import draw_meat_veg_section, bulk_sections

st.set_page_config(page_title="Bulk Ingredient Summary Report", layout="centered")

# --- Phase 2: Setup directory for saving previous reports ---
REPORTS_DIR = "production_reports"
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

def save_report(pdf_bytes, report_date):
    fname = f"{REPORTS_DIR}/daily_production_report_{report_date}.pdf"
    with open(fname, "wb") as f:
        f.write(pdf_bytes)
    return fname

def list_saved_reports():
    files = []
    for f in os.listdir(REPORTS_DIR):
        if f.endswith(".pdf"):
            # extract date in yyyy-mm-dd from filename
            try:
                d = f.split("daily_production_report_")[1].split(".pdf")[0]
                dt = datetime.strptime(d, "%Y-%m-%d")
            except Exception:
                dt = None
            files.append((f, dt))
    # Sort by date, most recent first
    files = sorted([x for x in files if x[1]], key=lambda x: x[1], reverse=True)
    return files

# --- Date Selector ---
st.title("📦 Bulk Ingredient Summary Report")
selected_date = st.date_input("Production Date", value=datetime.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")
selected_date_header = selected_date.strftime("%d/%m/%Y")

st.markdown("#### Upload CSV files for each brand (all optional, at least one required)")

c1, c2, c3 = st.columns(3)
with c1:
    clean_file = st.file_uploader("Clean Eats", type=["csv"], key="clean")
with c2:
    made_file = st.file_uploader("Made Active", type=["csv"], key="made")
with c3:
    elite_file = st.file_uploader("Elite Meals", type=["csv"], key="elite")

# --- File Read Logic ---
dfs = []
brand_names = ["Clean Eats", "Made Active", "Elite Meals"]
files = [clean_file, made_file, elite_file]
for f in files:
    if f is not None:
        df = pd.read_csv(f)
        df.columns = df.columns.str.strip().str.lower()
        dfs.append(df)
    else:
        dfs.append(None)

if all(d is None for d in dfs):
    st.warning("Please upload at least one CSV file.")
    st.stop()

# --- Find all unique meals (product name) across all uploads ---
all_meals = set()
for df in dfs:
    if df is not None:
        all_meals.update(df["product name"].str.strip())
all_meals = sorted(all_meals)

# --- Build summary table across all brands ---
data = []
for meal in all_meals:
    row = {"Meal": meal}
    total = 0
    for idx, df in enumerate(dfs):
        val = 0
        if df is not None:
            matches = df[df["product name"].str.strip() == meal]
            if not matches.empty:
                val = matches["quantity"].values[0]
        row[brand_names[idx]] = val
        total += val
    row["Total"] = total
    data.append(row)

summary_df = pd.DataFrame(data)

# --- Editable summary table ---
st.markdown("### Adjust Meal Quantities Before Generating Report")
editable_df = st.data_editor(
    summary_df,
    num_rows="dynamic",
    hide_index=True,
    column_config={"Meal": {"disabled": True}}
)

# --- Use the edited values for all calculations ---
meal_totals_total = {row["Meal"].upper(): row["Total"] for _, row in editable_df.iterrows()}

st.markdown("### Review Final Table (after editing above)")
st.dataframe(editable_df)

# --- PDF Generation ---
if st.button("Generate & Save Production Report PDF"):
    pdf = FPDF()
    pdf.set_auto_page_break(False)
    a4_w, a4_h = 210, 297
    left = 10
    page_w = a4_w - 2 * left
    col_w = page_w / 2 - 5
    ch, pad, bottom = 6, 4, a4_h - 17
    xpos = [left, left + col_w + 10]
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
    last_y = draw_meat_veg_section(pdf, meal_totals_total, xpos, col_w, ch, pad, bottom, start_y=last_y)
    # Save to Bytes
    pdf_buffer = pdf.output(dest='S').encode('latin1')
    # Save report for historical list
    report_fname = save_report(pdf_buffer, selected_date_str)
    st.success(f"Production report for {selected_date_header} saved!")
    st.download_button("📄 Download Production Report PDF", pdf_buffer, file_name=f"daily_production_report_{selected_date_str}.pdf", mime="application/pdf")

st.markdown("---")
# --- Previous Reports Section ---
st.markdown("### Previous Production Reports")
saved_reports = list_saved_reports()
if saved_reports:
    search_str = st.text_input("Search previous reports (by date, e.g., 2025-07-08):")
    filtered = []
    for fname, dt in saved_reports:
        if not search_str or search_str in fname or (dt and search_str in dt.strftime("%Y-%m-%d")):
            filtered.append((fname, dt))
    for fname, dt in filtered:
        st.markdown(f"- [{fname}]({REPORTS_DIR}/{fname}) ({dt.strftime('%d/%m/%Y')})")
else:
    st.info("No previous reports found.")

