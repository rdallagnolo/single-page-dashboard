import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
from PIL import Image

def app():
       ##################################################################
       # The dashboard
       ##################################################################

       # wide layout
       #st.set_page_config(layout="wide")
       # side bar
       # calendar 
       d=st.sidebar.date_input(label="Select the day",value=datetime.date(2021,10,25))     # starting date

       # week day
       wd = d.strftime('%A')
       # converting the selected from datetime to string so it can be used to slice the dataset
       d=d.strftime("%Y-%m-%d")                                              
       d=str(d)                                                              

       # add some css style to the page
       #with open('style.css') as f:
       #       st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

       # main header with report name
       st.markdown("<h1 style='text-align: center; color: #55D0CE '>Area and Branch Wise Daily Updates</h1>", unsafe_allow_html=True)
     
       ##################################################################
       # The dummy dataset
       ##################################################################
       df = pd.read_csv("Ops001-1_data.csv",parse_dates=["Date"])

       # condition check: no data on weekends
       if wd != 'Saturday' and wd != 'Sunday':

              # slicing the dataset to show only the selected day
              df = df[df['Date']==d]
              # reseting and droping index                    
              df.reset_index(drop=True,inplace=True)

              ## Splicing the dummy dataset by graphs 
              # droping 'Grand Total' and Regions
              branch = df.drop(labels=[6,13,18,25,27,33,34],axis=0)

              # only regions
              region = df.iloc[[6,13,18,25,27,33]]

              # grand total
              total = df.iloc[[34]]

              ##################################################################
              # By branch graph
              ##################################################################
              fig = go.Figure(data=[
              go.Bar(name='# of drop', y=branch['Branch Name'], x=branch['# of drop'],
                     orientation='h',text=branch['# of drop'],
                     marker_color='rgb(45, 139, 186)'),
              go.Bar(name='# of partial', y=branch['Branch Name'], x=branch['# of partial'],
                     orientation='h',text=branch['# of partial'],
                     marker_color='rgb(108, 230, 232)'),
              go.Bar(name='Yesterday paid off #', y=branch['Branch Name'], x=branch['Yesterday paid off #'],
                     orientation='h',text=branch['Yesterday paid off #'],
                     marker_color='rgb(47, 94, 152)'),
              go.Bar(name='Today disbursed #', y=branch['Branch Name'], x=branch['Today disbursed #'],
                     orientation='h',text=branch['Today disbursed #'],
                     marker_color='rgb(49, 53, 110)'),
              go.Bar(name='# of irregular borrower', y=branch['Branch Name'], x=branch['# of irregular borrower'],
                     orientation='h',text=branch['# of irregular borrower'],
                     marker_color='rgb(5, 183, 213)'),
              go.Bar(name='Virtual new borrower', y=branch['Branch Name'], x=branch['Virtual new borrower'],
                     orientation='h',text=branch['Virtual new borrower'],
                     marker_color='rgb(150, 108, 152)'),
              go.Bar(name='Returning', y=branch['Branch Name'], x=branch['Returning'],
                     orientation='h',text=branch['Returning'],)
              ])

              # chart layout
              fig.update_layout(barmode='stack',height=840, width=840,
                            paper_bgcolor='#FFFFFF',
                            plot_bgcolor='#FFFFFF',
                            #font_color='rgb(199, 208, 216)',
                            margin=dict(l=50, r=20, t=20, b=20,pad=20),
                            xaxis = dict(tickfont = dict(size=15)),
                            yaxis = dict(tickfont = dict(size=15)))

              # axes updates
              fig.update_xaxes(categoryorder='category ascending', gridcolor='#EFEBEB',type='linear')
              fig.update_yaxes(autorange="reversed",showline=False)
              fig.update_traces(marker_line_width=0, textposition='inside')

              # legend position
              fig.update_layout(legend=dict(
                     orientation="h",
                     yanchor="bottom",
                     y=1.05,
                     xanchor="left",
                     x=0,
                     font_size=15))

              ##################################################################
              # By region graph
              ##################################################################
              fig2 = go.Figure(data=[
              go.Bar(name='# of drop', x=region['Branch Name'], y=region['# of drop'],
                     marker_color='rgb(45, 139, 186)',text=region['# of drop']),
              
              go.Bar(name='# of partial', x=region['Branch Name'], y=region['# of partial'],
                     marker_color='rgb(108, 230, 232)',text=region['# of partial']),
              
              go.Bar(name='Yesterday paid off #', x=region['Branch Name'], y=region['Yesterday paid off #'],
                     marker_color='rgb(47, 94, 152)',text=region['Yesterday paid off #']),
              
              go.Bar(name='Today disbursed #', x=region['Branch Name'], y=region['Today disbursed #'],
                     marker_color='rgb(49, 53, 110)',text=region['Today disbursed #']),
              
              go.Bar(name='# of irregular borrower', x=region['Branch Name'], y=region['# of irregular borrower'],
                     marker_color='rgb(5, 183, 213)',text=region['# of irregular borrower']),
              
              go.Bar(name='Virtual new borrower', x=region['Branch Name'], y=region['Virtual new borrower'],
                     marker_color='rgb(150, 108, 152)',text=region['Virtual new borrower']),
              
              go.Bar(name='Returning', x=region['Branch Name'], y=region['Returning'],
                     text=region['Returning'])
              ])

              # chart layout
              fig2.update_layout(barmode='stack',height=840, width=840,
                            paper_bgcolor='#FFFFFF',
                            plot_bgcolor='#FFFFFF',
                            #font_color='#c7d0d8',
                            margin=dict(l=20, r=20, t=20, b=20, pad=20),
                            xaxis = dict(tickfont = dict(size=15),tickangle=45),
                            yaxis = dict(tickfont = dict(size=15)))

              # axis updates
              fig2.update_yaxes(gridcolor='#EFEBEB',type='linear')

              # legend position
              fig2.update_layout(legend=dict(
                     orientation="h",
                     yanchor="bottom",
                     y=1.05,
                     xanchor="left",
                     x=0.0,
                     font_size=15))

              # line with set to 0
              fig2.update_traces(marker_line_width=0)

              ##################################################################
              # Grand Total Metrics
              ##################################################################
              # variables
              n_of_drops = total.loc[34,'# of drop']
              n_of_partial = total.loc[34,'# of partial']
              yesterday_paid = total.loc[34,'Yesterday paid off #']
              today_disbursed = total.loc[34,'Today disbursed #']
              n_irregulars_borrower = total.loc[34,'# of irregular borrower'] 
              virtual_new_borrower = total.loc[34,'Virtual new borrower']
              returning = total.loc[34,'Returning']

              ##################################################################
              ## Ploting the graphs in the dashboard
              ##################################################################

              col1, col2, col3, col4, col5, col6, col7 = st.columns(7) 
              col1.metric(label='# of drops',value=n_of_drops)
              col2.metric(label='# of partial',value=n_of_partial)
              col3.metric(label='Yesterday paid off',value=yesterday_paid)
              col4.metric(label='Today disbursed',value=today_disbursed)
              col5.metric(label='# of irregular borrowes',value=n_irregulars_borrower)
              col6.metric(label='virtual new borrowers',value=virtual_new_borrower)
              col7.metric(label='Returning',value=returning)
              st.plotly_chart(fig)
              st.plotly_chart(fig2)

              ##################################################################
              # Add the data table to the dashboard
              ##################################################################
              df2 = df.drop(["Date"],axis=1)
              st.table(data=df2)

       # if weekends
       else:
              image = Image.open('weekend.jpg')
              st.image(image, caption='it is weekend')
              st.markdown("<a href='https://www.freepik.com/vectors/background' style='text-align: center; color: white'>Background vector created by freepik</a>", unsafe_allow_html=True)