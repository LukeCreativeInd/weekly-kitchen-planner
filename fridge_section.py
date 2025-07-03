parma_start_y = max(left_end_y, right_end_y) + pad
pdf.set_xy(left_x, parma_start_y)
pdf.set_font("Arial", "B", 11)
pdf.set_fill_color(230, 230, 230)
pdf.cell(col_w, ch, "Parma Mix", ln=1, fill=True)
pdf.set_x(left_x)
pdf.set_font("Arial", "B", 8)
for h, w in [("Ingredient", 0.4), ("Qty", 0.2), ("Amt", 0.2), ("Total", 0.2)]:
    pdf.cell(col_w * w, ch, h, 1)
pdf.ln(ch)
pdf.set_font("Arial", "", 8)
parma_amt = meal_totals.get("NAKED CHICKEN PARMA", 0)
for ing, qty in [("Napoli Sauce", 50), ("Mozzarella Cheese", 40)]:
    total = qty * parma_amt
    pdf.set_x(left_x)
    pdf.cell(col_w * 0.4, ch, ing, 1)
    pdf.cell(col_w * 0.2, ch, str(qty), 1)
    pdf.cell(col_w * 0.2, ch, str(parma_amt), 1)
    pdf.cell(col_w * 0.2, ch, str(total), 1)
    pdf.ln(ch)
