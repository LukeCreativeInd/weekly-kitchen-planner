import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
from bulk_section import draw_bulk_section
from recipes_section import draw_recipes_section, meal_recipes
from sauces_section import draw_sauces_section
from fridge_section import draw_fridge_section
from chicken_mixing_section import draw_chicken_mixing_section
from meat_veg_section import draw_meat_veg_section

# --- Storage for reports ---
REPORTS_DIR = "previous_reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

st.title("Bulk Ingredient Summary Report")

# --- Date Selector ---
selected_date = st.date_input("Select Production Date", value=datetime.today())
selected_date_str = selected_date.strftime('%Y-%m-%d')
selected_date_header = selected_date.strftime('%d/%m/%Y')

# --- Individual File Uploaders ---
st.markdown("#### Upload Production Files for Each Brand (CSV or Excel)")
clean_eats_file = st.file_uploader("Upload Clean Eats", type=["csv", "xlsx"], key="clean_eats")
made_active_file = st.file_uploader("Upload Made Active", type=["csv", "xlsx"], key="made_active")
elite_meals_file = st.file_uploader("Upload Elite Meals", type=["csv", "xlsx"], key="elite_meals")

group_labels = ["Clean Eats", "Made Active", "Elite Meals"]
group_files = [clean_eats_file, made_active_file, elite_meals_file]
group_dfs = [None, None, None]

# --- Parse files into dataframes ---
for idx, file in enumerate(group_files):
    if file is not None:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        df.columns = df.columns.str.strip().str.lower()
        if {"product name", "quantity"}.issubset(df.columns):
            group_dfs[idx] = df.copy()
        else:
            st.error(f"File for {group_labels[idx]} missing required columns.")
    else:
        group_dfs[idx] = None

# --- Build Summary Table (before editing) ---
def build_summary_table(dfs, group_labels):
    # Union of all product names
    all_names = set()
    for df in dfs:
        if df is not None:
            all_names.update(df["product name"].str.strip().str.upper())
    all_names = sorted(all_names)
    # Build the summary
    rows = []
    for name in all_names:
        row = {"Meal": name}
        total = 0
        for idx, df in enumerate(dfs):
            val = 0
            if df is not None:
                found = df[df["product name"].str.strip().str.upper() == name]
                if not found.empty:
                    val = found["quantity"].iloc[0]
            row[group_labels[idx]] = val
            total += val
        row["Total"] = total
        rows.append(row)
    return pd.DataFrame(rows)

# --- Interactive Table for Edits ---
meal_summary_df = None
if any(df is not None for df in group_dfs):
    meal_summary_df = build_summary_table(group_dfs, group_labels)
    st.markdown("#### Edit Meals to Produce (across all groups)")
    edited_df = st.data_editor(
        meal_summary_df,
        num_rows="dynamic",
        key="edit_meal_summary"
    )
    meal_summary_df = edited_df

# --- Wait for input before PDF generation ---
if meal_summary_df is not None and not meal_summary_df.empty:
    meal_totals_total = dict(zip(meal_summary_df["Meal"].str.upper(), meal_summary_df["Total"]))
else:
    meal_totals_total = {}

# --- PDF Generation ---
if st.button("Generate & Save Production Report PDF") and meal_summary_df is not None and not meal_summary_df.empty:
    pdf = FPDF()
    pdf.set_auto_page_break(False)
    a4_w, a4_h = 210, 297
    left = 10
    page_w = a4_w - 2 * left
    ch, pad, bottom = 6, 4, a4_h - 17
    xpos = [left, left + page_w // 2 + 5]

    # 1. Draw Summary Table as first table (wide format)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 12, f"Daily Production Report - {selected_date_header}", ln=1, align="C")
    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    col_w_meal = page_w * 0.35
    col_w_grp = (page_w - col_w_meal) / (len(group_labels)+1)
    headers = ["Meal"] + group_labels + ["Total"]
    for i, h in enumerate(headers):
        w = col_w_meal if i == 0 else col_w_grp
        pdf.cell(w, ch+2, h, 1, 0, "C", fill=True)
    pdf.ln(ch+2)
    pdf.set_font("Arial", "", 10)
    for _, row in meal_summary_df.iterrows():
        pdf.cell(col_w_meal, ch, str(row["Meal"]), 1)
        for g in group_labels:
            pdf.cell(col_w_grp, ch, str(row.get(g, 0)), 1, 0, "C")
        pdf.cell(col_w_grp, ch, str(row["Total"]), 1, 0, "C")
        pdf.ln(ch)

    last_y = pdf.get_y() + 4

    # 2. Draw all other sections as before, using meal_totals_total
    last_y = draw_bulk_section(pdf, meal_totals_total, xpos, page_w//2-5, ch, pad, bottom, start_y=last_y, header_date=selected_date_header)
    pdf.set_y(last_y)
    last_y = draw_recipes_section(pdf, meal_totals_total, xpos, page_w//2-5, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_sauces_section(pdf, meal_totals_total, xpos, page_w//2-5, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_fridge_section(pdf, meal_totals_total, xpos, page_w//2-5, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_chicken_mixing_section(pdf, meal_totals_total, xpos, page_w//2-5, ch, pad, bottom, start_y=last_y)
    pdf.set_y(last_y)
    last_y = draw_meat_veg_section(pdf, meal_totals_total, xpos, page_w//2-5, ch, pad, bottom, start_y=last_y)

    # 3. Save & download
    pdf_buffer = pdf.output(dest='S').encode('latin1')
    save_path = os.path.join(REPORTS_DIR, f"production_report_{selected_date_str}.pdf")
    with open(save_path, "wb") as f:
        f.write(pdf_buffer)
    st.success(f"Production report for {selected_date_header} saved!")
    st.download_button(
        "📄 Download Production Report PDF",
        pdf_buffer,
        file_name=f"daily_production_report_{selected_date_str}.pdf",
        mime="application/pdf"
    )

# --- Historical Reports & Search ---
st.divider()
st.markdown("#### Previous Reports")
reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".pdf")]
search = st.text_input("Search previous reports by date (yyyy-mm-dd) or keyword:")
filtered_reports = [r for r in reports if search.lower() in r.lower()]
if filtered_reports:
    for r in sorted(filtered_reports, reverse=True):
        with open(os.path.join(REPORTS_DIR, r), "rb") as f:
            st.download_button(f"Download {r}", f, file_name=r, mime="application/pdf")
else:
    st.info("No previous reports found.")
