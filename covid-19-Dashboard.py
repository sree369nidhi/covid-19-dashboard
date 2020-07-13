import streamlit as st  
import requests
import pandas as pd
import numpy as np
from datetime import datetime

from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
import plotly.graph_objects as go

from stylizeUI import stylize

stylize()
st.sidebar.markdown("<h2 style='text-align: center ; color: black;'>Options</h2>", unsafe_allow_html=True)
st.sidebar.subheader('Global Time Range')

time_span = st.sidebar.selectbox(
    label="Choose any time range for granular visualization...", options=['1 Week', '2 Weeks', '1 Month', '2 Months', 'From Beginning'])

def month_slicer(data, n):
	df = data
	range_max = df['Date'].max()
	range_min = range_max - pd.DateOffset(months=n)
	# take slice with final data
	df = df[(df['Date'] >= range_min) & (df['Date'] <= range_max)]
	return df

st.markdown("<h1 style='text-align: center ; color: black;'>Covid-19 Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center ; color: black;'>Developed by M S Sreenidhi Iyengar</h6>", unsafe_allow_html=True)
#cases_time_series
@st.cache()
def data_cases_time_series(time_span='1 Week'):
	df = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
	currentYear = datetime.now().year
	df['Date'] = df['Date'].apply(lambda x: x+str(currentYear))
	df['Date'] =  pd.to_datetime(df['Date'])
	
	#df.set_index('Date', inplace=True)
	#dtm = lambda x: datetime.strftime('%d %b')
	
	#dtm = lambda x: x.strftime('%m/%d/%Y')
	#df["Date"] = df["Date"].apply(dtm)
	#data = {'January':'Jan', 'February':'Feb', 'March':'Mar', 'April':'Apr', 'May':'May', 'June':'Jun', 'July':'Jul'}
	#df['Date'] = df['Date'].map(data)
	df['Daily Active'] = df['Daily Confirmed'] - df['Daily Deceased'] - df['Daily Recovered']
	df['Total Active'] = df['Total Confirmed'] - df['Total Deceased'] - df['Total Recovered']
	
	if time_span == '1 Week':
		return df.tail(7)
	elif time_span == '2 Weeks':
		return df.tail(14)
	elif time_span == '1 Month':
		return month_slicer(df, 1)
	elif time_span == '2 Months':
		return month_slicer(df, 2)
	#choosing time_span
	elif time_span == 'From Beginning':
		return df

cases_df = data_cases_time_series(time_span)

def timeformat(x):
	return x.strftime('%d/%m/%Y')	

st.markdown("<h3 style='text-align: center ; color: black;'>Across India </h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center ; color: black;'>Last Updated {}🕒</h5>".format(timeformat(cases_df.iloc[-1]['Date'])), unsafe_allow_html=True)
#st.write(cases_df.iloc[-1]['Date'].strftime('%m/%d/%Y'))

cnf, dth, rec, act = '#393e46', '#ff2e63', '#21bf73', '#fe9801' 

def another_total_fig():
	temp = cases_df[['Date', 'Total Confirmed', 'Total Deceased', 'Total Recovered', 'Total Active']].tail(1)
	temp = temp.melt(id_vars="Date", value_vars=['Total Confirmed', 'Total Deceased', 'Total Recovered', 'Total Active'])
	fig = px.treemap(temp, path=["variable"], values="value", height=225, 
	                 color_discrete_sequence=[cnf, dth, rec, act])
	fig.data[0].textinfo = 'label+value'
	fig.update_layout(autosize=False, width=200, height=225, uniformtext=dict(minsize=10, mode='hide'))
	fig.layout.hovermode = False
	st.plotly_chart(fig, use_container_width=True)


temp1 = cases_df[['Date', 'Total Confirmed', 'Total Deceased', 'Total Recovered', 'Total Active']].iloc[-1]
temp2 = cases_df[['Date', 'Total Confirmed', 'Total Deceased', 'Total Recovered', 'Total Active']].iloc[-2]

fig =go.Figure(go.Sunburst(
    labels=["Total Counts", "Confirmed", 'Recovered', 'Active', 'Deaths', timeformat(temp1[0]), timeformat(temp2[0]), timeformat(temp1[0]), timeformat(temp2[0]), timeformat(temp1[0]), timeformat(temp2[0]), timeformat(temp1[0]), timeformat(temp2[0])],
    parents=["", "Total Counts", "Total Counts", "Total Counts", "Total Counts", "Confirmed", "Confirmed", 'Recovered', 'Recovered', 'Active', 'Active', 'Deaths','Deaths'],
    values=[temp1[1:].sum(), temp1[1], temp1[3], temp1[4], temp1[2], temp1[1], temp2[1], temp1[3], temp2[3], temp2[4], temp2[4], temp1[2], temp2[2]],
    ))
fig.update_layout(autosize=False, margin = dict(t=9, l=0, r=0, b=0), width=800, height=400)
st.plotly_chart(fig, use_container_width=True)


fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = cases_df.iloc[-1]['Daily Confirmed'],
    domain = {'x': [0.01, 0.21], 'y': [0, 1]},
    title = {"text": "Confirmed<br><span style='font-size:0.8em;color:gray'>Today</span>"},
    delta = {'reference': cases_df.iloc[-2]['Daily Confirmed'], 'relative': True, 'position' : "top"}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = cases_df.iloc[-1]['Daily Recovered'],
    domain = {'x': [0.25, 0.49], 'y': [0, 1]},
    title = {"text": "Recovered<br><span style='font-size:0.8em;color:gray'>Today</span>"},
    delta = {'reference': cases_df.iloc[-2]['Daily Recovered'], 'relative': True, 'position' : "top"}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = cases_df.iloc[-1]['Daily Active'],
    domain = {'x': [0.51, 0.73], 'y': [0, 1]},
    title = {"text": "Active<br><span style='font-size:0.8em;color:gray'>Today</span>"},
    delta = {'reference': cases_df.iloc[-2]['Daily Active'], 'relative': True, 'position' : "top"}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = cases_df.iloc[-1]['Daily Deceased'],
    domain = {'x': [0.79, 0.93], 'y': [0, 1]},
    title = {"text": "Deceased<br><span style='font-size:0.8em;color:gray'>Today</span>"},
    delta = {'reference': cases_df.iloc[-2]['Daily Deceased'], 'relative': True, 'position' : "top"}))

fig.update_layout(autosize=False, width=800, height=250)
st.plotly_chart(fig, use_container_width=True)

if st.sidebar.checkbox("Show Cases Time Series Data"):
	st.dataframe(cases_df)

st.markdown("---")

st.markdown("<h3 style='text-align: center ; color: black;'>Coivd-19 Overview</h3>", unsafe_allow_html=True)	

st.sidebar.subheader('Overview')
overview_mode = st.sidebar.selectbox(
    label="Choose...", options=['lines+markers', 'lines', 'markers']
)

overview_radio = st.sidebar.radio("",('Total/Cummulative', 'Daily'))
if overview_radio == 'Total/Cummulative':
	overview_radio = 'Total'
#call Line charts and assign to fig_inc. Add traces to the same figure
fig_inc = go.Figure(go.Line(x=cases_df['Date'], y=cases_df[f'{overview_radio} Confirmed'],
					name='Confirmed', mode=overview_mode ,marker=dict(size=10,color='indianred')))
fig_inc.add_trace(go.Line(x=cases_df['Date'], y=cases_df[f'{overview_radio} Recovered'],
					name='Recovered', mode=overview_mode ,marker=dict(size=10,color='lightseagreen')))
fig_inc.add_trace(go.Line(x=cases_df['Date'], y=cases_df[f'{overview_radio} Deceased'],
					name='Deaths', mode=overview_mode ,marker=dict(size=10,color='gray')))
fig_inc.add_trace(go.Line(x=cases_df['Date'], y=cases_df[f'{overview_radio} Active'],
					name='Active', mode=overview_mode ,marker=dict(size=10,color='Orange')))
#here we define layout of the chart
fig_inc.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, plot_bgcolor='whitesmoke', 
        title={
        'text': 'Covid-19 Trend',
        'y':0.75,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},xaxis_type='date' )
fig_inc.update_xaxes(title= 'Timeline' ,showline=False)
fig_inc.update_yaxes(title= 'Frequency of Cases', showline=False)
fig_inc.update_layout(autosize=False, width=700, height=600)
st.plotly_chart(fig_inc)


st.sidebar.subheader('Bar Graph')
bar_graph = st.sidebar.selectbox(
    label="Choose...", options=['stack', 'group', 'overlay', 'relative']
)
bar_radio = st.sidebar.radio("",('Total', 'Daily'))

#call Bar charts and assign to fig_t. Add traces to the same figure
fig_t = go.Figure(go.Bar(x=cases_df['Date'], y=cases_df[f'{bar_radio} Confirmed'],
				name='Confirmed', marker_color='indianred', opacity=0.8))
fig_t.add_trace(go.Bar(x=cases_df['Date'], y=(cases_df[f'{bar_radio} Active']),
                name='Active', marker_color='mediumblue', opacity=0.7))
fig_t.add_trace(go.Bar(x=cases_df['Date'], y=cases_df[f'{bar_radio} Recovered'],
	            name='Recovered', marker_color='lightseagreen', opacity=0.8))
fig_t.add_trace(go.Bar(x=cases_df['Date'], y=cases_df[f'{bar_radio} Deceased'],
				name='Deaths', marker_color='gray', opacity=1))
#here we define layout of the chart
fig_t.update_layout(barmode=bar_graph, xaxis={'categoryorder':'total ascending'},xaxis_type='date',
                  title={
        'text': 'Covid-19 Trend',
        'y':0.79,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig_t.update_xaxes(title= 'Timeline' ,showline=True)
fig_t.update_yaxes(title= 'Frequency of cases', showline=True)
fig_t.update_layout(autosize=False, width=700, height=600)
st.plotly_chart(fig_t)

# Dropdown for Trends
selected_metrics = st.selectbox(
    label="Choose...", options=['Confirmed','Active','Recovered','Deaths']
)

# Create Trends Graph
#colors cnf, dth, rec, act
fig = go.Figure()
if selected_metrics == 'Confirmed':
	fig.add_trace(go.Scatter(x=cases_df['Date'], y=cases_df['Total Confirmed'],
                    mode='lines+markers',
                    name='Total Confirmed',
                    line=dict(color=cnf, width=4)))
if selected_metrics == 'Deaths':
	fig.add_trace(go.Scatter(x=cases_df['Date'], y=cases_df['Total Deceased'],
	                    mode='lines+markers', 
	                    name='Total Deaths',
	                    line=dict(color=dth, width=4)))
if selected_metrics == 'Recovered':
	fig.add_trace(go.Scatter(x=cases_df['Date'], y=cases_df['Total Recovered'],
	                    mode='lines+markers',
	                    name='Total Recovered',
	                    line=dict(color=rec, width=4)))
if selected_metrics == 'Active':
	fig.add_trace(go.Scatter(x=cases_df['Date'], y=cases_df['Total Active'],
	                    mode='lines+markers',
	                    name='Active',
	                    line=dict(color=act, width=4)))
#here we define layout of the chart
fig.update_layout(xaxis_type='date',
                  title={
        'text': f'Covid-19 {selected_metrics} Trend',
        'y':0.79,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.update_xaxes(title= 'Timeline' ,showline=True)
fig.update_yaxes(title= 'Number of cases', showline=True)
fig.update_layout(autosize=False, width=700, height=600)
st.plotly_chart(fig)

#statewise daily table
st.markdown("<h3 style='text-align: center ; color: black;'>State Wise Covid-19 Details</h3>", unsafe_allow_html=True)	

def get_state_data():
	#, header=None
	df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
	return df

state_df = get_state_data()
#state_df.set_index(0, inplace = True).reset_index(inplace=True)
#st.dataframe(state_df)
state_df = state_df.drop('Date', axis=1)
state_df = state_df.tail(3).T
#state_df.set_index(0, inplace = True) 
state_df.columns = state_df.iloc[0]
state_df.drop('Status', inplace=True, axis=0)
#state_df.index.name = 'States'
#state_df.columns.name = 'Status'

state_df['Active'] = state_df['Confirmed'] - state_df['Recovered'] - state_df['Deceased']
state_df.sort_values(by='Confirmed', inplace=True, ascending=False)

states_dict = {'UN': 'Unassigned', 'TT': 'India','TT': 'India', 'AP' :'Andhra Pradesh','AR' :'Arunachal Pradesh','AS' :'Assam','BR' :'Bihar','CT' :'Chhattisgarh','GA' :'Goa','GJ' :'Gujarat','HR' :'Haryana','HP' :'Himachal Pradesh','JH' :'Jharkhand','KA' :'Karnataka','KL' :'Kerala',
				'MP' :'Madhya Pradesh','MH' :'Maharashtra','MN' :'Manipur','ML' :'Meghalaya','MZ' :'Mizoram','NL' :'Nagaland','OR' :'Odisha','PB' :'Punjab','RJ' :'Rajasthan','SK' :'Sikkim','TN' :'Tamil Nadu','TG' :'Telangana','TR' :'Tripura','UT' :'Uttarakhand',
				'UP' :'Uttar Pradesh','WB' :'West Bengal','AN' :'Andaman & Nicobar Islands','CH' :'Chandigarh','DN' :'Dadra & Nagar Haveli','DD' :'Daman & Diu','DL' :'Delhi','JK' :'Jammu & Kashmir','LA' :'Ladakh','LD' :'Lakshadweep','PY' :'Puducherry'}

state_df.index = state_df.index.to_series().map(states_dict)
#st.dataframe(state_df)

colors = ['rgb(247, 148, 137)', 'rgb(247, 150, 140)', 'rgb(248, 153, 142)', 'rgb(248, 153, 142)', 'rgb(249, 158, 148)', 'rgb(249, 160, 150)', 'rgb(249, 163, 153)', 'rgb(250, 165, 155)', 'rgb(250, 168, 158)', 'rgb(250, 170, 161)',
			'rgb(250, 173, 163)', 'rgb(251, 175, 166)', 'rgb(251, 178, 169)', 'rgb(251, 180, 171)', 'rgb(251, 183, 174)', 'rgb(251, 185, 177)', 'rgb(252, 187, 180)', 'rgb(252, 190, 182)', 'rgb(252, 192, 185)', 'rgb(252, 195, 188)',
			  'rgb(252, 197, 190)', 'rgb(252, 200, 193)', 'rgb(252, 202, 196)', 'rgb(252, 205, 199)', 'rgb(252, 207, 201)', 'rgb(252, 209, 204)', 'rgb(252, 212, 207)', 'rgb(252, 214, 210)', 'rgb(252, 217, 212)', 'rgb(251, 219, 215)',
			    'rgb(251, 222, 218)', 'rgb(251, 224, 221)', 'rgb(251, 226, 223)', 'rgb(251, 229, 226)', 'rgb(250, 231, 229)', 'rgb(250, 234, 232)', 'rgb(250, 236, 234)', 'rgb(249, 239, 237)', 'rgb(249, 241, 240)']

fig = go.Figure(data=[go.Table(
  header=dict(
    values=["<b>State</b>", "<b>Confirmed</b>", "<b>Recovered</b>", "<b>Active</b>", "<b>Deceased</b>"],
    line_color='white', fill_color='white',
    align='left', font=dict(color='black', size=12)
  ),
  cells=dict(
    values=[state_df.index, state_df.Confirmed, state_df.Recovered, state_df.Active, state_df.Deceased],
    line_color=[colors], fill_color=[colors],
    align='left', font=dict(color='black', size=11)
  ))
])
fig.update_layout(autosize=False, width=700, height=900)
st.plotly_chart(fig)

todo ="""
#state_wise https://api.covid19india.org/csv/latest/state_wise.csv	
#df = px.data.gapminder()
#st.dataframe(df)
"""

st.markdown("<h3 style='text-align: center ; color: black;'>To-Do</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center ; color: black;'>State-wise Analysis</h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center ; color: black;'>India wide Analysis</h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center ; color: black;'>World wide Analysis</h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center ; color: black;'>Prediction of cases</h5>", unsafe_allow_html=True)