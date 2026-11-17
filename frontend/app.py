
import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Page title
st.title("SuperKart System")
st.write(
    "Enter the product and store details below to predict "
    "the total sales revenue."
)

# Input fields for product and store data
Product_Weight = st.number_input(
    "Product Weight", min_value=0.0, value=12.66
)

Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

Product_Allocated_Area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    max_value=1.0,
    value=0.027,
    step=0.001,
    format="%.3f"
)

Product_MRP = st.number_input(
    "Product MRP", min_value=0.0, value=117.08
)

Store_Size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"],
    index=1
)

Store_Location_City_Type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"],
    index=1
)

Store_Type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Departmental Store",
        "Food Mart"
    ],
    index=1
)

Product_Id_char = st.selectbox(
    "Product ID Character",
    ["FD", "DR", "NC"]
)

Store_Age_Years = st.number_input(
    "Store Age (Years)",
    min_value=0,
    value=16
)

Product_Type_Category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"],
    index=1
)

st.caption(
    "Store age follows the 2025 reference year used "
    "during model training."
)

# Create JSON payload
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

# Single Prediction
st.subheader("Single Prediction")

if st.button("Predict", type="primary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=product_data,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()
        predicted_sales = float(result["Sales"])

        st.success(
            f"Predicted Product Store Sales Total: "
            f"{predicted_sales:,.2f}"
        )

    except requests.exceptions.RequestException as e:
        st.error(f"Unable to connect to the prediction API: {e}")

    except (KeyError, TypeError, ValueError) as e:
        st.error(f"Unable to process prediction response: {e}")


# Batch Prediction
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Predict for Batch", type="primary"):

        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/predictbatch",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/csv"
                    )
                },
                timeout=60
            )

            response.raise_for_status()

            results = response.json()

            if isinstance(results, dict):

                # Display each prediction as a separate row
                df = pd.DataFrame(
                    list(results.items()),
                    columns=[
                        "Row Index (0-based)",
                        "Predicted Sales"
                    ]
                )

                st.success(
                    "Batch predictions completed successfully!"
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

                # Download prediction results
                csv = df.to_csv(index=False)

                st.download_button(
                    label="Download Predictions CSV",
                    data=csv,
                    file_name="superkart_predictions.csv",
                    mime="text/csv"
                )

            else:
                st.error("Unexpected batch prediction response.")
                st.json(results)

        except requests.exceptions.RequestException as e:
            st.error(f"Unable to connect to the prediction API: {e}")

        except (TypeError, ValueError) as e:
            st.error(f"Unable to process batch results: {e}")
