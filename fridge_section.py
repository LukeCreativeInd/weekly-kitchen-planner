def draw_fridge_section(pdf, meal_totals, xpos, col_w, ch, pad, bottom):
    y = max(pdf.get_y(), max(pdf.get_y() for _ in range(2)))
    pdf.set_xy(xpos[0], y)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"To Pack In Fridge", ln=1, align='C')
    pdf.ln(5)
    # Dual column tables for Fridge
    left_tables = [
        ("Sauces to Prepare", [("MONGOLIAN",70,"MONGOLIAN BEEF"),("
