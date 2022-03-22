import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
from PIL import Image

def app():
       ##################################################################
       # The dashboard
       ##################################################################

       ###########
       # side bar
       ############ 
       # calendar
       d=st.sidebar.date_input(label="Select the day",
                            value=datetime.date(2021,12,6))
       d=d.strftime("%Y-%m-%d")                                              
       d=str(d)                                                              

       # dropdown 
       area = st.sidebar.selectbox(
              "Select the Area",
              ('New York', 'Northeast', 'Central & Southeast','California','Texas','Elevate'))

       # main header with report name
       st.markdown("<h1 style='text-align: center; color: #55D0CE '>Area and Branch Wise Daily Updates</h1>", unsafe_allow_html=True)
     
       ##################################################################
       # The dummy dataset
       ##################################################################
       df = pd.read_csv("data/Ops001-1_data.csv",parse_dates=["Date"])

       # slicing the dataset to show only the selected day
       df = df[df['Date']==d]
       # reseting and droping index                    
       df.reset_index(drop=True,inplace=True)

       if area == 'New York':
              df=df.iloc[0:7,:]
              plot_rows = 2
              plot_cols = 3
       elif area == 'Northeast':
              df=df.iloc[7:14,:]
              plot_rows = 2
              plot_cols = 3
       elif area == 'Central & Southeast':
              df=df.iloc[14:19,:]
              plot_rows = 2
              plot_cols = 2
       elif area == 'California':
              df=df.iloc[19:26,:]
              plot_rows = 2
              plot_cols = 3
       elif area == 'Texas':
              df=df.iloc[26:30,:]
              plot_rows = 1
              plot_cols = 3
       elif area == 'Elevate':
              df=df.iloc[30:34,:]
              plot_rows = 1
              plot_cols = 3

       df = df.drop('Date',axis=1).set_index('Branch Name').T.reset_index().rename(columns = {'index':'metrics'})
       branches = list(df.columns[1:-1])

       fig = make_subplots(rows=plot_rows, cols=plot_cols,
                     shared_xaxes=True,
                     vertical_spacing=0.08,
                     subplot_titles=(branches))
       x = 1
       for i in range(1, plot_rows + 1):
              for j in range(1, plot_cols + 1):
                     fig.add_trace(go.Bar(x=df['metrics'],y=df[df.columns[x]].values,
                                   name = df.columns[x],
                                   ),
                            row=i,
                            col=j)

                     x=x+1
       fig.update_layout(template="ggplot2",
                     height=704, width=704, 
                     title_text=area,showlegend=False,plot_bgcolor='white')
       
       fig.update_traces(marker=dict(color=['#9EE3CA','#9BD7F2','#AEAEE4','#855AAC','#92AFE7','#30CAC0','#327F5F']))

       fig.update_yaxes(range=[0, 50])

       ##################################################################
       # Grand Total Metrics
       ##################################################################
       # variables
       n_of_drops = df.iloc[0:1,-1]
       n_of_partial = df.iloc[1:2,-1]
       yesterday_paid_off = df.iloc[2:3,-1]
       today_disbursed = df.iloc[3:4,-1]
       n_irreg_borrowers = df.iloc[4:5,-1]
       virtual_new_borrowers = df.iloc[5:6,-1]
       returning = df.iloc[6:7,-1]
       ##################################################################
       ## Ploting the graphs in the dashboard
       ##################################################################

       col1, col2, col3, col4, col5, col6, col7 = st.columns(7) 
       col1.metric(label='# of drops',value=n_of_drops)
       col2.metric(label='# of partial',value=n_of_partial)
       col3.metric(label='Yesterday paid off',value=yesterday_paid_off)
       col4.metric(label='Today disbursed',value=today_disbursed)
       col5.metric(label='# of irregular borrowes',value=n_irreg_borrowers)
       col6.metric(label='virtual new borrowers',value=virtual_new_borrowers)
       col7.metric(label='Returning',value=returning)
       st.plotly_chart(fig)