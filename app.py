import streamlit as st
import pandas as pd
import math
from fpdf import FPDF
from datetime import datetime

# ------------------
# To Pack In Fridge (2-column layout)
# ------------------
pdf.set_font("Arial","B",14)
pdf.cell(0,10,"To Pack In Fridge",ln=1,align='C')
pdf.ln(5)
# draw first two tables side by side
start_y = pdf.get_y()
# Table 1: Sauces to Prepare
pdf.set_xy(xpos[0], start_y)
pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
pdf.cell(col_w, ch, "Sauces to Prepare", ln=1, fill=True)
pdf.set_x(xpos[0]); pdf.set_font("Arial","B",8)
pdf.cell(col_w*0.4, ch, "Sauce",1); pdf.cell(col_w*0.2, ch, "Qty",1); pdf.cell(col_w*0.2, ch, "Amt",1); pdf.cell(col_w*0.2, ch, "Total",1)
pdf.ln(ch); pdf.set_font("Arial","",8)
for sauce,qty,meal_key in sauce_prep:
    pdf.set_x(xpos[0])
    amt = meal_totals.get(meal_key.upper(),0)
    total = qty * amt
    pdf.cell(col_w*0.4, ch, sauce,1)
    pdf.cell(col_w*0.2, ch, str(qty),1)
    pdf.cell(col_w*0.2, ch, str(amt),1)
    pdf.cell(col_w*0.2, ch, str(total),1)
    pdf.ln(ch)
# Table 2: Beef Burrito Mix
pdf.set_xy(xpos[1], start_y)
pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
pdf.cell(col_w, ch, "Beef Burrito Mix", ln=1, fill=True)
pdf.set_x(xpos[1]); pdf.set_font("Arial","B",8)
pdf.cell(col_w*0.3, ch, "Ingredient",1); pdf.cell(col_w*0.2, ch, "Qty",1); pdf.cell(col_w*0.2, ch, "Amt",1); pdf.cell(col_w*0.2, ch, "Total",1); pdf.cell(col_w*0.1, ch, "Batches",1)
pdf.ln(ch); pdf.set_font("Arial","",8)
amt_bb = meal_totals.get("BEEF BURRITO BOWL",0)
raw_bb = math.ceil(amt_bb/60) if amt_bb>0 else 0
batches_bb = raw_bb + (raw_bb % 2)
for ingr,qty in bb_rows:
    pdf.set_x(xpos[1])
    total_bb = (qty*amt_bb)/batches_bb if batches_bb else 0
    pdf.cell(col_w*0.3,ch,ingr,1); pdf.cell(col_w*0.2,ch,str(qty),1); pdf.cell(col_w*0.2,ch,str(amt_bb),1); pdf.cell(col_w*0.2,ch,str(round(total_bb,2)),1); pdf.cell(col_w*0.1,ch,str(batches_bb),1)
    pdf.ln(ch)
# draw Parma Mix below table1 in first column
# calculate bottom Y of first two tables
y_bottom = max(pdf.get_y(), pdf.get_y())
pdf.set_xy(xpos[0], y_bottom + pad)
pdf.set_font("Arial","B",11); pdf.set_fill_color(230,230,230)
pdf.cell(col_w, ch, "Parma Mix", ln=1, fill=True)
pdf.set_x(xpos[0]); pdf.set_font("Arial","B",8)
pdf.cell(col_w*0.4, ch, "Ingredient",1); pdf.cell(col_w*0.3, ch, "Qty",1); pdf.cell(col_w*0.3, ch, "Amt",1)
pdf.ln(ch); pdf.set_font("Arial","",8)
amt_pm = meal_totals.get("NAKED CHICKEN PARMA",0)
for ingr,qty in pm_rows:
    pdf.set_x(xpos[0])
    pdf.cell(col_w*0.4,ch,ingr,1); pdf.cell(col_w*0.3,ch,str(qty),1); pdf.cell(col_w*0.3,ch,str(amt_pm),1)
    pdf.ln(ch)
# prepare for Chicken Mixing
draw_mix_start = y_bottom + pad + (len(pm_rows)+2)*ch + pad
pdf.set_xy(left, draw_mix_start)
# initialize mixing columns below the heading
mix_start_y = pdf.get_y()
# define mixes data
mixes = [
    ("Pesto", [("Chicken",110),("Sauce",80)], "CHICKEN PESTO PASTA", 50),
    ("Butter Chicken", [("Chicken",120),("Sauce",90)], "BUTTER CHICKEN", 50),
    ("Broccoli Pasta", [("Chicken",100),("Sauce",100)], "CHICKEN AND BROCCOLI PASTA", 50),
    ("Thai", [("Chicken",110),("Sauce",90)], "THAI GREEN CHICKEN CURRY", 50),
    ("Gnocchi", [("Gnocchi",150),("Chicken",80),("Sauce",200),("Spinach",25)], "CREAMY CHICKEN & MUSHROOM GNOCCHI", 36)
]
mix_heights = [mix_start_y, mix_start_y]
mix_heights = [mix_start_y, mix_start_y]
mix_col = 0
for mix_title, data_key, meal_key, divisor in mixes:
    # estimate block height
    rows = len(data_key) + 2
    block_h = (rows + 1) * ch + pad
    mix_heights, mix_col = next_pos(mix_heights, mix_col, block_h)
    x, y = xpos[mix_col], mix_heights[mix_col]
    pdf.set_xy(x, y)
    # header
    pdf.set_font("Arial","B",11)
    pdf.set_fill_color(230,230,230)
    pdf.cell(col_w, ch, mix_title, ln=1, fill=True)
    pdf.set_x(x)
    pdf.set_font("Arial","B",8)
    for header, w in [("Ingredient",0.3),("Quantity",0.2),("Amount",0.2),("Total",0.2),("Batches",0.1)]:
        pdf.cell(col_w * w, ch, header, 1)
    pdf.ln(ch)
    # rows
    pdf.set_font("Arial","",8)
    amt = meal_totals.get(meal_key.upper(), 0)
    rb = math.ceil(amt/divisor) if amt>0 else 0
    batches = rb + (rb % 2)
    for ingr, qty in data_key:
        total = (qty * amt) / batches if batches else 0
        pdf.set_x(x)
        pdf.cell(col_w*0.3, ch, ingr[:20], 1)
        pdf.cell(col_w*0.2, ch, str(qty), 1)
        pdf.cell(col_w*0.2, ch, str(amt), 1)
        pdf.cell(col_w*0.2, ch, str(round(total,2)), 1)
        pdf.cell(col_w*0.1, ch, str(batches), 1)
        pdf.ln(ch)
    mix_heights[mix_col] = pdf.get_y() + pad

# ------------------
# Save & Download
# ------------------
# ------------------ & Download
# ------------------
# ------------------
fname = f"daily_production_report_{datetime.today().strftime('%d-%m-%Y')}.pdf"
pdf.output(fname)
with open(fname, "rb") as f:
    st.download_button(label="📄 Download Bulk Order PDF", data=f, file_name=fname, mime="application/pdf")
