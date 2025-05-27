import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.stats import norm

st.title("Sample Size Calculator for Clinical Study")

# Section 1: User Input
st.header("Study Inputs")

effect_size = st.number_input("Expected Mean Difference", value=10.0)
std_dev = st.number_input("Standard Deviation", value=15.0)
alpha = st.number_input("Alpha (Type I error)", value=0.05, min_value=0.001, max_value=0.2)
power = st.number_input("Power (1 - Type II error)", value=0.8, min_value=0.5, max_value=0.99)

# Number and Names of Endpoints
endpoint_count = st.number_input("Number of Primary Endpoints", min_value=1, step=1)
endpoint_names = []

for i in range(int(endpoint_count)):
    endpoint_name = st.text_input(f"Name of Endpoint {i+1}", key=f"ep{i}")
    endpoint_names.append(endpoint_name)

# Endpoint relationship
dependency = st.radio("Are these endpoints statistically independent?", ["Yes", "No"])

# Section 2: Sample Size Calculation
z_beta = norm.ppf(power)
z_alpha = norm.ppf(1 - (alpha / endpoint_count if dependency == "Yes" else alpha / 2))

n = (2 * ((z_alpha + z_beta)**2) * std_dev**2) / effect_size**2
n_rounded = math.ceil(n)

st.subheader("Results")
st.write(f"**Sample size per group:** {n_rounded}")
st.write(f"**Total subjects required:** {n_rounded * 2}")
adjusted_alpha = alpha / endpoint_count if dependency == "Yes" else alpha
st.write(f"**Adjusted alpha per test:** {adjusted_alpha:.4f}")

# Section 3: Visualization
st.subheader("Power Curve Visualization")
effect_range = [i for i in range(5, 21)]
sample_sizes = [(2 * ((norm.ppf(1 - adjusted_alpha / 2) + z_beta)**2) * std_dev**2) / (d**2) for d in effect_range]

plt.figure()
plt.plot(effect_range, [math.ceil(n) for n in sample_sizes], marker='o')
plt.xlabel("Effect Size (Mean Difference)")
plt.ylabel("Sample Size per Group")
plt.title("Sample Size vs. Effect Size")
st.pyplot(plt)

# Section 4: CSV Export
st.subheader("Download Results")
df = pd.DataFrame({
    "Endpoint Name(s)": [", ".join(endpoint_names)],
    "Effect Size": [effect_size],
    "Standard Deviation": [std_dev],
    "Power": [power],
    "Alpha": [alpha],
    "Adjusted Alpha": [adjusted_alpha],
    "Sample Size per Group": [n_rounded],
    "Total Sample Size": [n_rounded * 2],
    "Independent Endpoints": [dependency]
})

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "sample_size_results.csv", "text/csv")
