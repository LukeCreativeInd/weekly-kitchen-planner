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
col1, col2, col3 = st.columns(3)
with col1:
    file_clean = st.file_uploader("Upload Clean Eats File", type=["csv", "xlsx"], key="clean")
with col2:
    file_made = st.file_uploader("Upload Made Active File", type=["csv", "xlsx"], key="made")
with col3:
    file_elite = st.file_uploader("Upload Elite Meals File", type=["csv", "xlsx"], key="elite")

file_dfs = []
labels = []
if file_clean:
    df = pd.read_csv(file_clean) if file_clean.name.endswith(".csv") else pd.read_excel(file_clean)
    df["Source"] = "Clean Eats"
    file_dfs.append(df)
    labels.append("Clean Eats")
if file_made:
    df = pd.read_csv(file_made) if file_made.name.endswith(".csv") else pd.read_excel(file_made)
    df["Source"] = "Made Active"
    file_dfs.append(df)
    labels.append("Made Active")
if file_elite:
    df = pd.read_csv(file_elite) if file_elite.name.endswith(".csv") else pd.read_excel(file_elite)
    df["Source"] = "Elite Meals"
    file_dfs.append(df)
    labels.append("Elite Meals")

if file_dfs:
    df_all = pd.concat(file_dfs, ignore_index=True)
    # Normalise columns
    df_all.columns = df_all.columns.str.strip().str.lower()
    if not {"product name", "quantity", "source"}.issubset(df_all.columns):
        st.error("CSV must contain 'Product name', 'Quantity', and 'Source'")
        st.stop()

    # Summary Table
    summary = df_all.pivot_table(
        index="product name",
        columns="source",
        values="quantity",
        aggfunc="sum",
        fill_value=0
    )
    summary["Total"] = summary.sum(axis=1)
    summary = summary.reset_index()
    # Ensure all three columns exist
    for lbl in ["Clean Eats", "Made Active", "Elite Meals"]:
        if lbl not in summary.columns:
            summary[lbl] = 0
    # Sort columns for display
    display_cols = ["product name", "Clean Eats", "Made Active", "Elite Meals", "Total"]
    summary = summary[display_cols]
    st.markdown("### Meal Quantities Per Client")
    st.dataframe(summary)

    # Build meal_totals as required by the rest of the app (by uppercase product name)
    meal_totals = dict(
        zip(summary["product name"].str.upper(), summary["Total"])
    )

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
