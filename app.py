import streamlit as st

st.title("Debugging Streamlit App")
st.write("If you see this, the main file is fine.")

# Now try import one section at a time below here
try:
    from bulk_section import draw_bulk_section
    st.success("bulk_section loaded")
except Exception as e:
    st.error(f"bulk_section failed: {e}")

try:
    from recipes_section import draw_recipes_section
    st.success("recipes_section loaded")
except Exception as e:
    st.error(f"recipes_section failed: {e}")

try:
    from sauces_section import draw_sauces_section
    st.success("sauces_section loaded")
except Exception as e:
    st.error(f"sauces_section failed: {e}")

try:
    from fridge_section import draw_fridge_section
    st.success("fridge_section loaded")
except Exception as e:
    st.error(f"fridge_section failed: {e}")

try:
    from chicken_mixing_section import draw_chicken_mixing_section
    st.success("chicken_mixing_section loaded")
except Exception as e:
    st.error(f"chicken_mixing_section failed: {e}")

try:
    from meat_veg_section import draw_meat_veg_section
    st.success("meat_veg_section loaded")
except Exception as e:
    st.error(f"meat_veg_section failed: {e}")
