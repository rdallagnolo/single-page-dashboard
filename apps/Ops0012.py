#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 15:19:15 2022

@author: fubao
"""
import pandas as pd
import numpy as np
import streamlit as st

import datetime
from datetime import timedelta, date

import matplotlib.pyplot as plt
import plotly.graph_objects as go

def app():
    # main header with report name
    st.markdown("<h2 style='text-align: center; color: #55D0CE '>Daily Email Report to CEO</h2>", unsafe_allow_html=True)

    All_BRANCH_SELECTION = "Select All Branches"
    All_CENTER_SELECTION = "Select All Centers"
    All_GROUP_SELECTION = "Select All Groups"
    All_METRIC_SELECTION = "Select All metrics"

    def visualize ():
        
        # set the style
        # set_style()
            
        # initialization
        #st.markdown('<p class="big-font">Daily Email Report to CEO </p>', unsafe_allow_html=True)
        #st.markdown("***")

        df_ops002 = read_data()
        all_branches = df_ops002['Branch'].unique()   #.tolist()
        all_branches = np.insert(all_branches, 0, All_BRANCH_SELECTION)

        option_branch = st.sidebar.selectbox(
            'Select A Branch:',
            all_branches)
        

        if option_branch == All_BRANCH_SELECTION:
            df_current_bcg = df_ops002
            
        else:
            all_centers = df_ops002[df_ops002['Branch'] == option_branch]['Center'].unique()  
            all_centers = np.insert(all_centers,0, All_CENTER_SELECTION)
        
            option_center = st.sidebar.selectbox(
                'Select A Center:',
                all_centers)
            
            if option_center == All_CENTER_SELECTION:
                df_current_bcg = df_ops002[(df_ops002['Branch'] == option_branch)]
            else:
                df_current_bcg = df_ops002[(df_ops002['Branch'] == option_branch)  & (df_ops002['Center'] == option_center)]
                all_groups = df_current_bcg['Group'].unique()  
                all_groups = np.insert(all_groups, 0, All_GROUP_SELECTION)
                
                option_group = st.sidebar.selectbox(
                        'Select A Group:',
                        all_groups)
                    
                if option_group != All_GROUP_SELECTION:

                    all_metrics = df_ops002.columns[5:].tolist()# .union([])
                    all_metrics.insert(0, All_METRIC_SELECTION)
                    
                    option_metric = st.sidebar.selectbox(
                        'Select A Metric to Display:',
                        all_metrics)
        
        #print("df_current_bcg, ", df_current_bcg)    
        min_start_period = min(df_current_bcg['Date'])
        max_end_period = max(df_current_bcg['Date'])
        
        #print("min_start_period: ", min_start_period)
        #print("min_start_period, ",  type(min_start_period), max_end_period) 
        min_start_date_obj = datetime.datetime.strptime(min_start_period,'%Y/%m/%d').date() 
        max_enddate_obj = datetime.datetime.strptime(max_end_period,'%Y/%m/%d').date() 
        
        # slide bar show period
        select_start_date = st.sidebar.date_input(
        "Select the Start Datetime",
        min_start_date_obj)  # datetime.date(y, m, d)
        select_start_date = select_start_date.strftime("%Y/%m/%d")

        # slide bar show period
        select_end_date = st.sidebar.date_input(
        "Select the End Datetime",
        min_start_date_obj +  timedelta(days=20))  
        select_end_date = select_end_date.strftime("%Y/%m/%d")
        
        #print("option_branchssssssssss: ", option_branch, option_center, option_group, option_metric, type(select_end_date))
        
        # assert(select_start_date <= select_end_date)
        if select_start_date > select_end_date:
            st.title("Start date must be not bigger than end date")
        
        #df_ops002 = df_ops002.rename(columns={'Date':'index'}).set_index('index')
        
        if option_branch == All_BRANCH_SELECTION:
            selected_times_rows = df_ops002[(df_ops002['Date'] >= select_start_date) & (df_ops002['Date'] <= select_end_date)]
            selected_times_rows = selected_times_rows.rename(columns={'Date':'index'}).set_index('index')
            show_all_branches_period(df_ops002, select_start_date, select_end_date)

        
        elif option_center == All_CENTER_SELECTION:
            selected_times_rows = df_ops002[(df_ops002['Branch'] == option_branch) & (df_ops002['Date'] >= select_start_date) & (df_ops002['Date'] <= select_end_date)]
            selected_times_rows = selected_times_rows.rename(columns={'Date':'index'}).set_index('index')
            show_all_centers_period(df_ops002, option_branch, select_start_date, select_end_date)
    

        elif option_group == All_GROUP_SELECTION:
            selected_times_rows = df_ops002[(df_ops002['Branch'] == option_branch)  & (df_ops002['Center'] == option_center)
                                        & (df_ops002['Date'] >= select_start_date) & (df_ops002['Date'] <= select_end_date)]
            selected_times_rows = selected_times_rows.rename(columns={'Date':'index'}).set_index('index')
        
            show_all_groups_period(df_ops002, option_branch, option_center, select_start_date, select_end_date)

        elif option_metric == All_METRIC_SELECTION:
            selected_times_rows = df_ops002[(df_ops002['Branch'] == option_branch)  & (df_ops002['Center'] == option_center)
                                        & (df_ops002['Group'] == option_group) & (df_ops002['Date'] >= select_start_date) & (df_ops002['Date'] <= select_end_date)]
            selected_times_rows = selected_times_rows.rename(columns={'Date':'index'}).set_index('index')
        
            show_all_metrics_period(df_ops002, option_branch, option_center, option_group, select_start_date, select_end_date)
            
        else:
            selected_times_rows = df_ops002[(df_ops002['Branch'] == option_branch)  & (df_ops002['Center'] == option_center)
                                        & (df_ops002['Group'] == option_group) & (df_ops002['Date'] >= select_start_date) & (df_ops002['Date'] <= select_end_date)]
            selected_times_rows = selected_times_rows.rename(columns={'Date':'index'}).set_index('index')
        
            show_metrics_statistics(selected_times_rows, option_metric)
    


        
    def show_all_branches_period(df_ops002, select_start_date, select_end_date):
        #print("show_all_centers_period here")

        selected_times_rows = df_ops002[(df_ops002['Date'] >= select_start_date) & (df_ops002['Date'] <= select_end_date)]
        
        # show all the metrics's statistics
        
        all_metrics = df_ops002.columns[5:].tolist()
        
        list_sum_metrics = []
        for i, metric in enumerate(all_metrics):
            sum_option_metric_value = selected_times_rows[metric].sum()   #.tolist()
            
            # print("sum_option_metric_value: ", type(sum_option_metric_value), sum_option_metric_value)
            
            list_sum_metrics.append(sum_option_metric_value)
    
        
        # make two columns as dataframe
        data_tuples = list(zip(all_metrics,list_sum_metrics))
        data_written = pd.DataFrame(data_tuples, columns=['Metric','Aggregated sum in the selected periods'])

        #print("data_tuples: ", data_tuples)
        
        
        # Plot
        col1, col2 = st.columns(2)

        fig, ax = plt.subplots()
        ax.bar(range(len(all_metrics)), list_sum_metrics)
        
        col1.pyplot(fig)    
        col2.write(data_written)
        
        
    def show_all_centers_period(df_ops002, option_branch, select_start_date, select_end_date):
        #print("show_all_centers_period here")

        selected_times_rows = df_ops002[(df_ops002['Branch'] == option_branch)
                                        & (df_ops002['Date'] >= select_start_date) & (df_ops002['Date'] <= select_end_date)]
        
        
        # show all the metrics's statistics
        all_metrics = df_ops002.columns[5:].tolist()
        
        list_sum_metrics = []
        for i, metric in enumerate(all_metrics):
            sum_option_metric_value = selected_times_rows[metric].sum()   #.tolist()
            
            # print("sum_option_metric_value: ", type(sum_option_metric_value), sum_option_metric_value)
            
            list_sum_metrics.append(sum_option_metric_value)
            
            html_str = f"""
            <style>
            p.a {{
            font: bold 25px Courier;
            }}
            </style>
            <p class="a">{i+1}: {metric} -- {sum_option_metric_value}</p>
            """
        
            #with st.container():
            #    st.markdown(html_str, unsafe_allow_html=True)
        
        # make two columns as dataframe
        data_tuples = list(zip(all_metrics,list_sum_metrics))
        data_written = pd.DataFrame(data_tuples, columns=['Metric','Aggregated sum in the selected periods'])

        #print("data_tuples: ", data_tuples)
        
        
        # Plot
        col1, col2 = st.columns(2)

        fig, ax = plt.subplots()
        ax.bar(range(len(all_metrics)), list_sum_metrics)
        
        col1.pyplot(fig)    
        col2.write(data_written)

    def show_all_groups_period(df_ops002, option_branch, option_center, select_start_date, select_end_date):
        #print("show_all_groups_period here")

        selected_times_rows = df_ops002[(df_ops002['Branch'] == option_branch)  & (df_ops002['Center'] == option_center)
                                        & (df_ops002['Date'] >= select_start_date) & (df_ops002['Date'] <= select_end_date)]
        
        
        # show all the metrics's statistics
        
        all_metrics = df_ops002.columns[5:].tolist()
        
        list_sum_metrics = []
        for i, metric in enumerate(all_metrics):
            sum_option_metric_value = selected_times_rows[metric].sum()   #.tolist()
            
            # print("sum_option_metric_value: ", type(sum_option_metric_value), sum_option_metric_value)
            
            list_sum_metrics.append(sum_option_metric_value)
            
            html_str = f"""
            <style>
            p.a {{
            font: bold 25px Courier;
            }}
            </style>
            <p class="a">{i+1}: {metric} -- {sum_option_metric_value}</p>
            """
        
            #with st.container():
            #    st.markdown(html_str, unsafe_allow_html=True)
        
        # make two columns as dataframe
        data_tuples = list(zip(all_metrics,list_sum_metrics))
        data_written = pd.DataFrame(data_tuples, columns=['Metric','Aggregated sum in the selected periods'])

        #print("data_tuples: ", data_tuples)
        
        
        # Plot
        col1, col2 = st.columns(2)

        fig, ax = plt.subplots()
        ax.bar(range(len(all_metrics)), list_sum_metrics)
        
        col1.pyplot(fig)    
        col2.write(data_written)
        
    def show_all_metrics_period(df_ops002, option_branch, option_center, option_group, select_start_date, select_end_date):
        
        # option_metric is All, center is not "All" and branch is not "All"
        #print("show_all_metrics_period here")

        selected_times_rows = df_ops002[(df_ops002['Branch'] == option_branch)  & (df_ops002['Center'] == option_center)
                                        & (df_ops002['Group'] == option_group) & (df_ops002['Date'] >= select_start_date) & (df_ops002['Date'] <= select_end_date)]
        
        
        # show all the metrics's statistics
        
        all_metrics = df_ops002.columns[5:].tolist()
        
        list_sum_metrics = []
        for i, metric in enumerate(all_metrics):
            sum_option_metric_value = selected_times_rows[metric].sum()   #.tolist()
            
            # print("sum_option_metric_value: ", type(sum_option_metric_value), sum_option_metric_value)
            
            list_sum_metrics.append(sum_option_metric_value)

        # make two columns as dataframe
        data_tuples = list(zip(all_metrics,list_sum_metrics))
        data_written = pd.DataFrame(data_tuples, columns=['Metric','Aggregated sum in the selected periods'])

        #print("data_tuples: ", data_tuples)
        
        
        # Plot
        col1, col2 = st.columns(2)

        fig, ax = plt.subplots()
        ax.bar(range(len(all_metrics)), list_sum_metrics)
        
        col1.pyplot(fig)    
        col2.write(data_written)
        


        
    def show_metrics_statistics(selected_times_rows, option_metric):
        
        # show the specific metrics' statistics
        
        sum_option_metric_value = selected_times_rows[option_metric].sum()

        html_str = f"""
        <style>
        p.a {{
        font: bold 25px Courier;
        }}
        </style>
        <p class="a">Aggregated {option_metric} in the selected period: {sum_option_metric_value}</p>
        """

        with st.container():
            st.markdown(html_str, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("")


        # show the plot
        with st.container():
            st.markdown('<p class="mid-font"> Metric Trending by Date </p>', unsafe_allow_html=True)
        
            st.line_chart(selected_times_rows[option_metric])


        #st.title('Metric Trending by Date')

#    def set_style():
#    #    st.set_page_config(layout="wide")

#        st.markdown("""
#        <style>
#        .big-font {
#            font-size:50px !important;
#            color:Red;
#        }
#        
#        .mid-font {
#            font-size:30px !important;
#            color:Blue;
#        }
#        
#        </style>
#        """, unsafe_allow_html=True)
        
    #    with open('style.css') as f:
    #        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
            

    def read_data():
        
        data_ops002_path = 'data/fake_groups.csv'
        
        
        df_ops002 = pd.read_csv(data_ops002_path, index_col = None)
        return df_ops002
        
    visualize()