import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import yfinance as yf
import matplotlib.pyplot as plt

with st.container():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #544B6A, #268AD6);
                    padding: 2.5rem;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                    margin-bottom: 20px;">
            <h1 style="margin: 0;">📊 Budget & Multi-Asset Investment Simulation</h1>
            <h3>🎓Education Investment Plan for Next Year</h3>
        </div>
    """, unsafe_allow_html=True)

st.divider()


current_budget = st.number_input("Enter the total education budget for 2025 ($):", min_value=0, value=5000000, step=10000)


st.write("📌 Enter student enrollment numbers for the last 5 years:")
years = ["2020", "2021", "2022", "2023", "2024"]
student_counts = [st.number_input(f"Students in {year}:", min_value=0, value=10000, step=100) for year in years]


df_students = pd.DataFrame({"Year": years, "Students": student_counts})


goal_per_student = st.number_input("Enter the goal funding per student for 2026 ($):", min_value=0, value=12000, step=500)


st.subheader("📈 Student Enrollment Projection")


df_students["Year"] = pd.to_numeric(df_students["Year"])


model = ExponentialSmoothing(df_students["Students"], trend="add", seasonal=None)
fit_model = model.fit()
forecast_result = fit_model.forecast(steps=1)
next_year_students = int(forecast_result.iloc[0]) if isinstance(forecast_result, pd.Series) else int(forecast_result[0])


st.write(f"📊 **Projected Student Count for 2026:** {next_year_students}")


st.subheader("💰 Budget Deficit Analysis")


required_budget = next_year_students * goal_per_student
deficit = required_budget - current_budget

st.write(f"✅ **Required Budget for 2026:** ${required_budget:,}")
st.write(f"❌ **Current Deficit:** ${deficit:,}" if deficit > 0 else "✅ No deficit! Your budget meets the goal.")


st.subheader("📈 Investment Plan to Bridge Budget Gap")

if deficit > 0:
    st.write("🔎 Finding an investment strategy to generate the required funds by next summer...")


    investment_choices = st.multiselect(
        "Choose investment assets:",
        ["Stocks", "Bonds", "ETFs", "REITs", "Cryptocurrency"],
        default=["Stocks", "ETFs"]
    )


    weights = {choice: st.slider(f"Allocation to {choice} (%)", 0, 100, 20, step=5) for choice in investment_choices}
    
    if sum(weights.values()) != 100:
        st.warning("⚠️ Allocations must sum to 100%. Adjust your selections.")


    asset_data = {
        "Stocks": {"return": 0.10, "volatility": 0.15},  # 10% annual return, 15% volatility
        "Bonds": {"return": 0.04, "volatility": 0.05},   # 4% annual return, 5% volatility
        "ETFs": {"return": 0.08, "volatility": 0.12},    # 8% annual return, 12% volatility
        "REITs": {"return": 0.07, "volatility": 0.14},   # 7% annual return, 14% volatility
        "Cryptocurrency": {"return": 0.30, "volatility": 0.60}  # 30% return, but high risk (60% vol)
    }


    expected_return = sum(weights[asset] / 100 * asset_data[asset]["return"] for asset in investment_choices)
    expected_volatility = sum(weights[asset] / 100 * asset_data[asset]["volatility"] for asset in investment_choices)


    required_investment = deficit / (1 + expected_return)
    st.write(f"💰 **Recommended Investment:** ${int(required_investment):,} into your selected assets.")


    st.subheader("📊 Monte Carlo Simulation: Investment Growth Over Time")

    months = 12  
    num_simulations = 1000 


    simulations = np.zeros((num_simulations, months + 1))
    simulations[:, 0] = required_investment 

  
    np.random.seed(42)  
    for i in range(num_simulations):
        for month in range(1, months + 1):
            random_shock = np.random.normal(loc=expected_return / 12, scale=expected_volatility / np.sqrt(12))
            simulations[i, month] = simulations[i, month - 1] * (1 + random_shock)


    median_projection = np.median(simulations, axis=0)
    lower_bound = np.percentile(simulations, 5, axis=0)  
    upper_bound = np.percentile(simulations, 95, axis=0)  


    fig, ax = plt.subplots()
    ax.plot(range(0, months + 1), median_projection, marker="o", linestyle="-", color="blue", label="Median Projection")
    ax.fill_between(range(0, months + 1), lower_bound, upper_bound, color="blue", alpha=0.2, label="5%-95% Confidence Interval")
    ax.set_xlabel("Months")
    ax.set_ylabel("Investment Value ($)")
    ax.set_title("Monte Carlo Simulated Investment Growth Over the Year")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)


    final_value = median_projection[-1]
    st.write(f"📈 **Projected Median Growth After 1 Year:** ${int(final_value):,}")
    if final_value >= deficit:
        st.success("✅ Your investment is likely to reach the required amount by next year!")
    else:
        st.error(f"⚠️ Your investment may fall short. Consider increasing allocation or risk exposure.")

else:
    st.write("🎉 Your current budget is sufficient! No investment needed.")
