import streamlit as st

# Unit conversion dictionaries
length_units = {
    "Meter": 1,
    "Kilometer": 1000,
    "Centimeter": 0.01,
    "Millimeter": 0.001,
    "Mile": 1609.34,
    "Yard": 0.9144,
    "Foot": 0.3048,
    "Inch": 0.0254
}

mass_units = {
    "Kilogram": 1,
    "Gram": 0.001,
    "Milligram": 1e-6,
    "Pound": 0.453592,
    "Ounce": 0.0283495
}

temperature_units = ["Celsius", "Fahrenheit", "Kelvin"]

# Temperature conversion
def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32

# General conversion
def convert(value, from_unit, to_unit, unit_dict):
    return value * unit_dict[from_unit] / unit_dict[to_unit]

# Streamlit UI
st.title("Google-Style Unit Converter")

category = st.selectbox("Select Category", ["Length", "Mass", "Temperature"])
value = st.number_input("Enter value", format="%f")

if category == "Length":
    units = list(length_units.keys())
    from_unit = st.selectbox("From", units)
    to_unit = st.selectbox("To", units)
    result = convert(value, from_unit, to_unit, length_units)

elif category == "Mass":
    units = list(mass_units.keys())
    from_unit = st.selectbox("From", units)
    to_unit = st.selectbox("To", units)
    result = convert(value, from_unit, to_unit, mass_units)

elif category == "Temperature":
    from_unit = st.selectbox("From", temperature_units)
    to_unit = st.selectbox("To", temperature_units)
    result = convert_temperature(value, from_unit, to_unit)

st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")