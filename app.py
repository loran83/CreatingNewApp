import streamlit as st
import scipy.stats
import pandas as pd
import time

st.header('🪙 Tossing a Coin')

# Create a placeholder chart with column name
initial_data = pd.DataFrame({'Mean': []})
chart = st.line_chart(initial_data)

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no

        # Add data to chart using a DataFrame with correct format
        chart.add_rows(pd.DataFrame({'Mean': [mean]}))

        time.sleep(0.05)

    return mean

# UI elements
number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials...')
    final_mean = toss_coin(number_of_trials)
    st.success(f'✅ Experiment complete! Final mean: {final_mean:.2f}')
