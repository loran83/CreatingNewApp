import pandas as pd
import scipy.stats
import streamlit as st
import time

# Stateful variables preserved between runs
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('🪙 Tossing a Coin')

# Start with an empty DataFrame with a named column
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

        # Must pass a DataFrame to add_rows
        new_data = pd.DataFrame({'Mean': [mean]})
        chart.add_rows(new_data)

        time.sleep(0.05)

    return mean

# UI
number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experiment with {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1

    mean = toss_coin(number_of_trials)

    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(
    {
        'no': [int(st.session_state['experiment_no'])],
        'iterations': [int(number_of_trials)],
        'mean': [float(mean)]
    }
)

    ], axis=0).reset_index(drop=True)

# Display results
st.subheader("📊 Experiment Results")
st.write(st.session_state['df_experiment_results'])
