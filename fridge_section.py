import math

def draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom, start_y=None):
    y = start_y or pdf.get_y()
    pdf.set_y(y)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "To Pack In Fridge", ln=1, align="C")
    pdf.ln(2)

    left_x, right_x = xpos
    start_y = pdf.get_y()

    # Table 1: Sauces to Prepare (left col)
    pdf.set_xy(left_x, start_y)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Sauces to Prepare", ln=1, fill=True)
    pdf.set_x(left_x)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Sauce", 0.35), ("Qty", 0.18), ("Amt", 0.18), ("Total", 0.25)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    sauces = [
        ("MONGOLIAN", 70, "MONGOLIAN BEEF"),
        ("MEATBALLS", 120, "BEEF MEATBALLS"),
        ("LEMON", 50, "ROASTED LEMON CHICKEN"),
        ("MUSHROOM", 100, "STEAK WITH MUSHROOM SAUCE"),
        ("FAJITA SAUCE", 33, "CHICKEN FAJITA BOWL"),
        ("BURRITO SAUCE", 43, "BEEF BURRITO BOWL"),
    ]
    for sauce, qty, meal_key in sauces:
        amt = meal_totals.get(meal_key.upper(), 0)
        tot = qty * amt
        pdf.set_x(left_x)
        pdf.cell(col_w * 0.35, ch, sauce, 1)
        pdf.cell(col_w * 0.18, ch, str(qty), 1)
        pdf.cell(col_w * 0.18, ch, str(amt), 1)
        pdf.cell(col_w * 0.25, ch, str(tot), 1)
        pdf.ln(ch)
    left_end_y = pdf.get_y()

    # Table 2: Beef Burrito Mix (right col)
    pdf.set_xy(right_x, start_y)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(col_w, ch, "Beef Burrito Mix", ln=1, fill=True)
    pdf.set_x(right_x)
    pdf.set_font("Arial", "B", 8)
    for h, w in [("Ingredient", 0.35), ("Qty", 0.18), ("Amt", 0.18), ("Total", 0.25)]:
        pdf.cell(col_w * w, ch, h, 1)
    pdf.ln(ch)
    pdf.set_font("Arial", "", 8)

    beef_burrito = [
        ("Salsa", 43),
        ("Black Beans", 50),
        ("Corn", 50),
        ("Rice", 130),
    ]
    amt = meal_totals.get("BEEF BURRITO BOWL", 0)
    for ing, qty in beef_burrito:
        tot = (qty * amt) / 60 if amt else 0
        pdf.set_x(right_x)
        pdf.cell(col_w * 0.35, ch, ing, 1)
        pdf.cell(col_w * 0.18, ch, str(qty), 1)
        pdf.cell(col_w * 0.18, ch, str(amt), 1)
        pdf.cell(col_w * 0.25, ch, str(round(tot, 2)), 1)
        pdf.ln(ch)
    right_end_y = pdf.get_y()

    # Table 3: Parma Mix (place below the *lower* of the two tables above, in left col)
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

    # Return next Y value
    return max(pdf.get_y(), right_end_y, parma_start_y + ch * 3)
