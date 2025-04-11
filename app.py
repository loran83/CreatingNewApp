import pandas as pd
import scipy.stats
import streamlit as st
import time

# Initialize session state variables
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('🪙 Tossing a Coin Simulation')

# Create initial chart with correct structure
chart = st.line_chart(pd.DataFrame({'Mean': [0.5]}))

# Define the experiment logic
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no

        # Append new mean as a DataFrame row
        chart.add_rows(pd.DataFrame({'Mean': [mean]}))

        time.sleep(0.02)  # adjust speed if needed

    return mean

# UI Elements
number_of_trials = st.slider('Number of trials?', 1, 1000, 10, key='trial_slider')
start_button = st.button('Run', key='run_button')

if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials...')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)

    # Add results to the DataFrame in session state
    new_result = pd.DataFrame([[st.session_state['experiment_no'], number_of_trials, mean]],
                              columns=['no', 'iterations', 'mean'])

    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        new_result
    ], ignore_index=True)

# Display results
st.subheader("Experiment Results")
st.dataframe(st.session_state['df_experiment_results'])
