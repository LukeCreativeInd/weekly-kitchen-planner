import streamlit as st
import pandas as pd
import math
from fpdf import FPDF
from datetime import datetime

    # ------------------
    # Chicken Mixing + All Mixes
    # ------------------
    pdf.ln(5)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Chicken Mixing",ln=1,align='C')
    pdf.ln(5)
    mixes = [
        ("Pesto", [("Chicken", 110), ("Sauce", 80)], "CHICKEN PESTO PASTA"),
        ("Butter Chicken", [("Chicken", 120), ("Sauce", 90)], "BUTTER CHICKEN"),
        ("Broccoli Pasta", [("Chicken", 100), ("Sauce", 100)], "CHICKEN AND BROCCOLI PASTA"),
        ("Thai", [("Chicken", 110), ("Sauce", 90)], "THAI GREEN CHICKEN CURRY")
    ]
    for mix_title, ingredients, meal_key in mixes:
        pdf.set_x(left)
        pdf.set_font("Arial","B",11)
        pdf.set_fill_color(230,230,230)
        pdf.cell(col_w, ch, mix_title, ln=1, fill=True)
        pdf.ln(2)
        pdf.set_x(left)
        pdf.set_font("Arial","B",8)
        headers = ["Ingredient", "Quantity", "Amount", "Total", "Batches"]
        widths  = [0.3,      0.2,        0.2,      0.2,      0.1      ]
        for h, w in zip(headers, widths):
            pdf.cell(col_w * w, ch, h, 1)
        pdf.ln(ch)
        pdf.set_font("Arial","",8)
        amt = meal_totals.get(meal_key.upper(), 0)
        raw_batches = math.ceil(amt / 50) if amt > 0 else 0
        batches = raw_batches + (raw_batches % 2)
        for ingr, qty in ingredients:
            total = (qty * amt) / batches if batches else 0
            pdf.set_x(left)
            pdf.cell(col_w * 0.3, ch, ingr, 1)
            pdf.cell(col_w * 0.2, ch, str(qty), 1)
            pdf.cell(col_w * 0.2, ch, str(amt), 1)
            pdf.cell(col_w * 0.2, ch, str(round(total, 2)), 1)
            pdf.cell(col_w * 0.1, ch, str(batches), 1)
            pdf.ln(ch)

    # ------------------
    # Save & Download
    # ------------------
    # ------------------
    fname=f"daily_production_report_{datetime.today().strftime('%d-%m-%Y')}.pdf"
    pdf.output(fname)
    with open(fname,"rb") as f: st.download_button("📄 Download Bulk Order PDF", f, file_name=fname, mime="application/pdf")
