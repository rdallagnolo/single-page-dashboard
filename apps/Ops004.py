import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

def app():
    # main header with report name
    st.markdown("<h2 style='text-align: center; color: #55D0CE '>Center Discipline Report</h2>", unsafe_allow_html=True)

    # data
    group = pd.read_csv("data/fake_groups.csv").drop("Unnamed: 0", axis=1)
    people = pd.read_csv("data/fake_people.csv").drop("Unnamed: 0", axis=1)

    # callback to set data
    def data_change():
        global df
        global time_data
        date_string = datetime.datetime(selected_date.year, selected_date.month, selected_date.day).strftime("%Y/%m/%d")
        df = group.loc[(group["Branch"] == branch) & (group["Center"] == center) & (group["Date"] == date_string)].reset_index()
        time_data = group.loc[(group["Branch"] == branch) & (group["Center"] == center) & (group["Date"] <= date_string)]

    # selectors
    branch = st.selectbox(label="Select a branch:", options=np.unique(group["Branch"]), on_change=data_change)
    center = st.selectbox(label="Select a center:", options=np.unique(group.loc[(group["Branch"] == branch)]["Center"]), on_change=data_change)
    selected_date = st.slider(label="Select a date:", min_value=datetime.date(2022, 2, 1), max_value=datetime.date(2022, 2, 28), on_change=data_change)

    # initialize data based on default selections
    data_change()

    # header
    components.html(
        f"""
        <h1 class="main-header text">Discipline Report</h1>
        <h2 class="sub-header text">Center: {center}</h2>
        """
    )

    # attendance graph
    fig = go.Figure(data=[
        go.Bar(name="Present", x=df["Group"], y=df["attendance_6_mo"])
        , go.Bar(name="Other", x=df["Group"], y=np.subtract(1, df["attendance_6_mo"]))
    ])
    fig.update_layout(barmode="stack", title="Center attendance, last 6 months")
    fig.update_xaxes(title_text="Group")
    fig.update_yaxes(title_text="Attendance")

    # plot graph
    st.plotly_chart(fig)

    # group status section
    components.html(
        """
        <h2 class="sub-header text">Group and Center Completion</h2>
        """
    )

    # group selector
    selected_group = st.selectbox(label="Select a group:", options=np.unique(df["Group"]))
    group_index = df.loc[(df["Group"] == selected_group)].index.values[0]

    # completion data table
    completion = pd.DataFrame.from_dict({
        "Groups": [df.iloc[group_index]["Group"], len(df)]
        , "Members": [df.iloc[group_index]["group_size"], df["group_size"].sum()]
        , "Borrowers": [df.iloc[group_index]["n_borrowers"], df["n_borrowers"].sum()]
        , "Balance": [df.iloc[group_index]["outstanding_$"], df["outstanding_$"].sum()]
    }).set_index(np.array(["Group Total", "Center Total"]))

    st.write(completion.astype(str))

    # time trend
    time_data_group = time_data.loc[(time_data["Group"] == selected_group)]

    fig_2 = go.Figure(data=[
        go.Scatter(x=time_data_group["Date"], y=time_data_group["repayment_$"], name='Repayment, $')
    ])
    fig_2.update_layout(title=f"Repayments, 2022/02, {selected_group}")
    fig_2.update_xaxes(title_text="Date")
    fig_2.update_yaxes(title_text="Repayment, $")

    st.plotly_chart(fig_2)