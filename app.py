import streamlit as st


# Utils
def calc_fib_price(base_price, mult, i_range, i_is_long=True):
    if i_is_long:
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
        
    for i, label in enumerate(label_ls):
        fib_lvl = fib_lvl_ls[i]
        
        anchor_price = swing_low if is_long else swing_high
        price = calc_fib_price(anchor_price, fib_lvl, swing_range, is_long)
        calc_price[label] = price
    
    st.write(f'Direction = {direction}')
    basic_table_html = f"""
    <style>
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    th, td {{
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }}
    </style>
    <table>
        <tr>
            <th>Type</th>
            <th>Fib Level</th>
            <th>Price</th>
            <th>Unit Ratio</th>
        </tr>
        <tr>
            <td>{label_ls[0]}</td>
            <td>{fib_lvl_ls[0]}</td>
            <td>{calc_price[label_ls[0]]}</td>
            <td>{unit_ratio_ls[0]}</td>
        </tr>
        <tr>
            <td>{label_ls[1]}</td>
            <td>{fib_lvl_ls[1]}</td>
            <td>{calc_price[label_ls[1]]}</td>
            <td>{unit_ratio_ls[1]}</td>
        </tr>
        <tr>
            <td>{label_ls[2]}</td>
            <td>{fib_lvl_ls[2]}</td>
            <td>{calc_price[label_ls[2]]}</td>
            <td>{unit_ratio_ls[2]}</td>
        </tr>
        <tr>
            <td>{label_ls[3]}</td>
            <td>{fib_lvl_ls[3]}</td>
            <td>{calc_price[label_ls[3]]}</td>
            <td>{unit_ratio_ls[3]}</td>
        </tr>
        <tr>
            <td>{label_ls[4]}</td>
            <td>{fib_lvl_ls[4]}</td>
            <td>{calc_price[label_ls[4]]}</td>
            <td>{unit_ratio_ls[4]}</td>
        </tr>
    </table>
    """
    st.markdown(basic_table_html, unsafe_allow_html=True)
    
    
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
    size_table_html = f"""
    <style>
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    th, td {{
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }}
    </style>
    <table>
        <tr>
            <th>Type</th>
            <th>Avg Cost Price</th>
            <th>Take Profit</th>
            <th>Expected Return (&#37;)</th>
            <th>Ammount to Risk</th>
            <th>Unit to Buy</th>
        </tr>
        <tr>
            <td>Entry 1</td>
            <td>{avg_cost_price_1:,.2f}</td>
            <td>{tp_1:,.2f}</td>
            <td>{exp_ret_1*100:.1f}&#37;</td>
            <td>{amt_risk_1:,.2f}</td>
            <td>{unit_buy_1:,.2f}</td>
        </tr>
        <tr>
            <td>Entry 2</td>
            <td>{avg_cost_price_2:,.2f}</td>
            <td>{tp_2:,.2f}</td>
            <td>{exp_ret_2*100:.1f}&#37;</td>
            <td>{amt_risk_2:,.2f}</td>
            <td>{unit_buy_2:,.2f}</td>
        </tr>
        <tr>
            <td>Entry 3</td>
            <td>{avg_cost_price_3:,.2f}</td>
            <td>{tp_3:,.2f}</td>
            <td>{exp_ret_3*100:.1f}&#37;</td>
            <td>{amt_risk_3:,.2f}</td>
            <td>{unit_buy_3:,.2f}</td>
        </tr>
    </table>
    """
    st.markdown(size_table_html, unsafe_allow_html=True)
