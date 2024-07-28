import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Utils
def calc_fib_price(base_price, mult, i_range, is_long=True):
    if is_long:
        return base_price + i_range * mult
    else:
        return base_price - i_range * mult


# Parameters
label_ls = ['Take Profit', 'Entry 1', 'Entry 2', 'Entry 3', 'Stop Loss']
fib_lvl_ls = [1.272, 0.618, 0.382, 0.17, -0.05]
unit_ratio_ls = [None, 1, 2, 6, None]
calc_price = {}

st.set_page_config(layout="wide")
st.title("Position Sizing Calculator")

# User input
st.header('Input')

with st.form(key='user_form'):
    risk_amount = st.number_input('Risk Amount ($)')
    swing_high = st.number_input('Swing High')
    swing_low = st.number_input('Swing Low')
    direction = st.selectbox('Direction', ['LONG', 'SHORT'], index=0)
    tp_range = st.number_input('TP Range', value=0.9)
    commission = st.number_input('Commission', value=0.01)
    
    submitted = st.form_submit_button('Submit')

if submitted:
    # Calculated
    swing_range = swing_high - swing_low
    swing_pct = swing_high / swing_low - 1.0
    is_long = direction == 'LONG'
    
    # Account for commission
    risk_amount = risk_amount * (1 - commission)
    
    # Basic Info
    st.markdown('<hr>', unsafe_allow_html=True)
    st.header('Basic Info')
    
    st.write(f'Direction = {direction}')
    cols = st.columns(4)
    cols[0].write('**Type**')
    cols[1].write('**Fib Lvl**')
    cols[2].write('**Price**')
    cols[3].write('**Unit Ratio**')
    
    for i, label in enumerate(label_ls):
        fib_lvl = fib_lvl_ls[i]
        unit_ratio = unit_ratio_ls[i]
        
        
        anchor_price = swing_low if is_long else swing_high
        
        price = calc_fib_price(anchor_price, fib_lvl, swing_range, is_long)
        cols[0].write(label)
        cols[1].write(fib_lvl)
        cols[2].write(price)
        cols[3].write(unit_ratio)
        
        calc_price[label] = price
        
    # Sizing
    entry_1 = calc_price['Entry 1']
    entry_2 = calc_price['Entry 2']
    entry_3 = calc_price['Entry 3']
    
    tp_1 = calc_price['Take Profit']
    tp_2 = calc_price['Entry 2'] + (calc_price['Entry 1'] - calc_price['Entry 2']) * tp_range
    tp_3 = calc_price['Entry 3'] + (calc_price['Entry 2'] - calc_price['Entry 3']) * tp_range
    
    avg_cost_price_1 = entry_1
    avg_cost_price_2 = (entry_1 + 2 * entry_2) / 3
    avg_cost_price_3 = (entry_1 + 2 * entry_2 + 6 * entry_3) / 9
    tot_avg_cost_price = entry_1 + 2 * avg_cost_price_2 + 6 * avg_cost_price_3
    
    mult_dir = 1 if is_long else -1
    exp_ret_1 = mult_dir * (tp_1 / entry_1 - 1)
    exp_ret_2 = mult_dir * (tp_2 / entry_2 - 1)
    exp_ret_3 = mult_dir * (tp_3 / entry_3 - 1)
        
    amt_risk_1 = (avg_cost_price_1 * 1 / tot_avg_cost_price) * risk_amount
    amt_risk_2 = (avg_cost_price_2 * 2 / tot_avg_cost_price) * risk_amount
    amt_risk_3 = (avg_cost_price_3 * 6 / tot_avg_cost_price) * risk_amount
    
    unit_buy_1 = amt_risk_1 / avg_cost_price_1
    unit_buy_2 = amt_risk_2 / avg_cost_price_2
    unit_buy_3 = amt_risk_3 / avg_cost_price_3
        
    st.markdown('<hr>', unsafe_allow_html=True)
    st.header('Sizing')
    
    st.write(f'Direction = {direction}')
    cols = st.columns(6)
    
    cols[0].write('**Type**')
    cols[0].write('Entry 1')
    cols[0].write('Entry 2')
    cols[0].write('Entry 3')
    
    cols[1].write('**Avg Cost Price**')
    cols[1].write(f'{avg_cost_price_1:,.2f}')
    cols[1].write(f'{avg_cost_price_2:,.2f}')
    cols[1].write(f'{avg_cost_price_3:,.2f}')
    
    cols[2].write('**Take Profit**')
    cols[2].write(f'{tp_1:,.2f}')
    cols[2].write(f'{tp_2:,.2f}')
    cols[2].write(f'{tp_3:,.2f}')
    
    cols[3].write('**Expected Return (%)**')
    cols[3].write(f'{exp_ret_1*100:.1f}%')
    cols[3].write(f'{exp_ret_2*100:.1f}%')
    cols[3].write(f'{exp_ret_3*100:.1f}%')
    
    cols[4].write('**Amount to Risk**')
    cols[4].write(f'{amt_risk_1:,.2f}')
    cols[4].write(f'{amt_risk_2:,.2f}')
    cols[4].write(f'{amt_risk_3:,.2f}')
    
    cols[5].write('**Unit to Buy**')
    cols[5].write(f'{unit_buy_1:,.2f}')
    cols[5].write(f'{unit_buy_2:,.2f}')
    cols[5].write(f'{unit_buy_3:,.2f}')
