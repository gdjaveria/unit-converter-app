import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# Add custom CSS to style the app
st.title("🔄 Unit Converter")
st.write("Convert between different units")

st.markdown("""
    <style>
        .main {
            background-color: #f0f4f7;
        }
        .stButton>button {
            background-color: #2F4F4F;
            color: white;
            font-size: 22px;
            padding: 12px 26px;
            border-radius: 7px;
            border: none;
        }
        .stSelectbox>label {
            font-size: 18px;
            color: #333;
        }
        .stNumberInput>label {
            font-size: 18px;
            color: #333;
        }
        .stTextInput>label {
            font-size: 18px;
            color: #333;
        }
        .stTitle {
            color: #4CAF50;
        }
        .stAlert {
            background-color: #f8d7da;
            color: #721c24;
        }
    </style>
""", unsafe_allow_html=True)

# Function to perform the conversion
def convert_units(value, from_unit, to_unit, category):
    if category not in conversion_factors:
        st.error("Invalid category")
        return None
    
    factors = conversion_factors[category]
    
    if from_unit not in factors or to_unit not in factors:
        st.error("Invalid units for conversion")
        return None

# Special handling for temperature conversions
    if category == "Temperature":
        # Convert to Celsius first
        if from_unit == "Fahrenheit":
            value = (value - 32) * 5/9
        elif from_unit == "Kelvin":
            value = value - 273.15
        
 # Then convert to target unit
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
        return value
    
# For all other conversions, use the conversion factors
    converted_value = value * factors[to_unit] / factors[from_unit]
    return converted_value

# Conversion factors
conversion_factors = {
    'Length': {
        'meters': 1, 'kilometers': 0.001, 'centimeters': 100, 'millimeters': 1000,
        'miles': 0.000621371, 'yards': 1.09361, 'inches': 39.3701
    },
    'Weight': {
        'grams': 1, 'kilograms': 0.001, 'milligrams': 1000, 'pounds': 0.00220462,
        'ounces': 0.035274
    },
    'Temperature': {
        'Celsius': 1, 'Fahrenheit': 9/5, 'Kelvin': 1
    },
    'Time': {
        'seconds': 1, 'minutes': 1/60, 'hours': 1/3600, 'days': 1/86400, 'weeks': 1/604800
    },
    'Volume': {
        'liters': 1, 'milliliters': 1000, 'cubic meters': 0.001, 'gallons': 0.264172, 'cups': 4.22675
    },
    'Area': {
        'square_meters': 1, 'square_kilometers': 0.000001, 'square_feet': 10.7639,
        'square_yards': 1.19599, 'hectares': 0.0001, 'acres': 0.000247105
    },
    'Digital Storage': {
        'bytes': 1, 'kilobytes': 0.001, 'megabytes': 1e-6, 'gigabytes': 1e-9,
        'terabytes': 1e-12
    },
    'Energy': {
        'joules': 1, 'calories': 0.239006, 'kilocalories': 0.000239006,
        'kilowatt_hours': 2.777778e-7
    },
    'Pressure': {
        'pascal': 1, 'kilopascal': 0.001, 'bar': 0.00001, 'psi': 0.000145038,
        'atmosphere': 9.86923e-6
    }
}


# Move category selection and color picker to sidebar
with st.sidebar:
    st.header("Settings")
    category = st.selectbox("Select category", list(conversion_factors.keys()))
    
    st.subheader("Chart Colors")
    bar_color_from = st.color_picker("'From' value color", "#4CAF50")
    bar_color_to = st.color_picker("'To' value color", "#FFC107")

# Get units based on selected category
units = list(conversion_factors[category].keys())

# Main conversion interface
col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox(f"Convert from ({category})", units)
    value = st.number_input(f"Enter value in {from_unit}", min_value=0.0, format="%.6f")

with col2:
    to_unit = st.selectbox(f"Convert to ({category})", units)

# Convert when the button is pressed
if st.button("Convert"):
    result = convert_units(value, from_unit, to_unit, category)
    if result is not None:
        # Show the main result prominently
        st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")
        
        # Create tabs for detailed view
        tab1, tab2 = st.tabs(["Conversion Details", "Visualization"])
        
        with tab1:
            st.subheader("Conversion Details")
            details_col1, details_col2 = st.columns(2)
            
            with details_col1:
                st.write("**Input Details:**")
                st.write(f"- Category: {category}")
                st.write(f"- Input Value: {value}")
                st.write(f"- From Unit: {from_unit}")
            
            with details_col2:
                st.write("**Output Details:**")
                st.write(f"- Converted Value: {result:.6f}")
                st.write(f"- To Unit: {to_unit}")
        
        with tab2:
            # Show bar chart for comparison
            conversion_values = [value, result]
            units = [f"{from_unit}", f"{to_unit}"]
            df = pd.DataFrame(conversion_values, units, columns=["Value"])

            fig, ax = plt.subplots()
            df.plot(kind="bar", ax=ax, color=[bar_color_from, bar_color_to])
            ax.set_title(f"Conversion Visualization")
            ax.set_ylabel("Value")
            ax.set_xlabel("Units")
            st.pyplot(fig)

 