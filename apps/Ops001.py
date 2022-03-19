import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
from PIL import Image


def app():
    ##################################################################
    # The dashboard
    ##################################################################
    
    # add some css style to the page
    with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # main header with report name
    st.markdown("<h2 style='text-align: center; color: #55D0CE '>Branch Daily Update</h2>", unsafe_allow_html=True)
    
    ###########
    # side bar
    ###########
    # calendar 
    day=st.sidebar.date_input(
        label="Select the day",
        value=datetime.date(2021,12,10))
    # dropdown
    branch = st.sidebar.selectbox(
        'Select the branch',
        ('Dallas', 'Memphis'))

    # week day
    wd = day.strftime('%A')
    # converting the selected from datetime to string so it can be used to slice the dataset
    day=day.strftime("%Y-%m-%d")                                              
    day=str(day)                                                              


    ##################################################################
    # The dummy dataset
    ##################################################################
    df = pd.read_csv("Ops001.csv",parse_dates=["Date"])

    # slicing the dataset to show only the selected day
    df =  df[(df['Date']==day) & (df['Branch Name']==branch)]
    # reseting and droping index                    
    df.reset_index(drop=True,inplace=True)



    ##################################################################
    # Loan quality graph
    ##################################################################
    loan_quality = df.iloc[0:3:,0:6]

    fig1 = go.Figure(data=[go.Bar(name = '# Drops',x = loan_quality['Staff Name'],y = loan_quality['# Drops']),
                        go.Bar(name = '# Partials',x = loan_quality['Staff Name'],y = loan_quality['# Partials']),
                        go.Bar(name = '# Irregular Borrower', x = loan_quality['Staff Name'],y = loan_quality['# Irregular Borrower'])
                        ]
                    )

    fig1.update_layout(template="plotly_white",
        width=840,height=420,
        title="Loan Quality",
        xaxis_title="Staff Name",
        yaxis_title="Count"
        #legend_title="Legend Title",
        #font=dict(
        #    family="Courier New, monospace",
        #    size=18,
        #    color="RebeccaPurple"
        #)
    )

    # legend position
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=0))


    ##################################################################
    # Renewal trend graph
    ##################################################################
    renewal_trend = df.loc[0:2,['Date','Branch Name','Staff Name','# Paid Off Yesterday','# Today Disbursed','# Today Paid off']]

    fig2 = go.Figure(data=[go.Bar(name = '# Paid Off Yesterday',x = renewal_trend['Staff Name'],y = renewal_trend['# Paid Off Yesterday']),
                        go.Bar(name = '# Today Disbursed',x = renewal_trend['Staff Name'],y = renewal_trend['# Today Disbursed']),
                        go.Bar(name = '# Today Paid off', x = renewal_trend['Staff Name'],y = renewal_trend['# Today Paid off'])
                        ]
                    )

    fig2.update_layout(template="plotly_white",
        width=840,height=420,
        title="Renewal trend",
        xaxis_title="Staff Name",
        yaxis_title="Count")

    # legend position
    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1 ,
        xanchor="left",
        x=0))


    ##################################################################
    # Recruitment graph
    ##################################################################
    recruitment = df.loc[0:2,['Date','Branch Name','Staff Name','# Virtual New Borrower (Disbursed)','# Returning Borrowers (Disbursed)','# CGT Trainings',
                        '# Recognized New Members','# Recognized Return Members']]

    fig3 = go.Figure(data=[go.Bar(name = '# Virtual New Borrower (Disbursed)',x = recruitment['Staff Name'],y = recruitment['# Virtual New Borrower (Disbursed)']),
                        go.Bar(name = '# Returning Borrowers (Disbursed)',x = recruitment['Staff Name'],y = recruitment['# Returning Borrowers (Disbursed)']),
                        go.Bar(name = '# CGT Trainings', x = recruitment['Staff Name'],y = recruitment['# CGT Trainings']),
                        go.Bar(name = '# Recognized New Members', x = recruitment['Staff Name'],y = recruitment['# Recognized New Members']),
                        go.Bar(name = '# Recognized Return Members', x = recruitment['Staff Name'],y = recruitment['# Recognized Return Members'])
                        ]
                    )

    fig3.update_layout(template="plotly_white",
        width=840,height=420,
        title="Recruitment",
        xaxis_title="Staff Name",
        yaxis_title="Count")

    # legend position
    fig3.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1 ,
        xanchor="left",
        x=0))

    ##################################################################
    # Portfolio
    ##################################################################
    portfolio = df.loc[0:2,['Date','Branch Name','Staff Name','$ Portfolio Outstanding']]

    fig4 = go.Figure(data=[go.Pie(labels=portfolio['Staff Name'], values=portfolio['$ Portfolio Outstanding'])])

    fig4.update_layout(template="plotly_white",
        width=840,height=630,
        title="$ Portfolio Outstanding"
    )

    fig4.update_traces(hoverinfo='label+value+percent', textinfo='value',texttemplate = "%{label} <br>%{value:$,s} <br>(%{percent})", textfont_size=20)

    ##################################################################
    # Grand total
    ##################################################################
    total = df.iloc[3,:]

    n_of_drops = total['# Drops']
    n_of_partial = total['# Partials']
    irreg_borrower = total['# Irregular Borrower']
    payed_yesterday = total['# Paid Off Yesterday']
    today_disbursed = total['# Today Disbursed']
    today_paid_off = total['# Today Paid off']

    virtual_new_borrower = total['# Virtual New Borrower (Disbursed)']
    return_borrowers = total['# Returning Borrowers (Disbursed)']
    cgt_trainings = total['# CGT Trainings']
    recognized_new_members = total['# Recognized New Members']
    recognized_return_members = total['# Recognized Return Members']
    portfolio_outstanding = total['$ Portfolio Outstanding']

    ##################################################################
    ## Ploting the graphs in the dashboard
    ##################################################################

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric(label='# of drops',value=n_of_drops)
    col2.metric(label='# Partials',value=n_of_partial)
    col3.metric(label='# Irregular Borrower',value=irreg_borrower)
    col4.metric(label='# Paid Off Yesterday',value=payed_yesterday)
    col5.metric(label='# Today Disbursed',value=today_disbursed)
    col6.metric(label='# Today Paid off',value=today_paid_off)
    col1.metric(label='# Virtual New Borrower (Disbursed)',value=virtual_new_borrower)
    col2.metric(label='# Returning Borrowers (Disbursed)',value=return_borrowers)
    col3.metric(label='# CGT Trainings',value=cgt_trainings)
    col4.metric(label='# Recognized New Members',value=recognized_new_members)
    col5.metric(label='# Recognized Return Members',value=recognized_return_members)

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)

    #df2 = df.drop('Date',axis=1)
    #st.table(df2)