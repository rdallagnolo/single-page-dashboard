import streamlit as st
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
import pandas as pd
import pydeck as pdk


def app():
    # main header with report name
    st.markdown("<h2 style='text-align: center; color: #55D0CE '>Repay and Present by Center</h2>", unsafe_allow_html=True)


    ops6_df = pd.read_csv('data/fake_data_ops6.csv')
    fin008_df = pd.read_csv('data/fake_data_fin008.csv')

    ## Dashboard construction
    colorscale = [[0, '#00bbbb'], [.5, '#cccdce'], [1, '#b3b5b5']]

    st.sidebar.title("Menu")
    report_option = st.sidebar.selectbox('Choose a report:',
                                        ('Goal Tracker', 'Fin 8'))
    st.sidebar.write('Report selected:', report_option)

    map_reports = {'Goal Tracker': 'ops6', 'Fin 8': 'fin008'}
    report_mapped = map_reports[report_option]

    titles = {'ops6': 'Harlem Goal Tracker', 'fin008': 'Repayments by Branch'}

    if str(f"{report_mapped}_df") in locals():
        data = eval(f"{report_mapped}_df")

        st.title(titles[report_mapped])
        st.text('This is placeholder text.')

        if 'lat' and 'lon' in list(data.columns):
            filtered_data = data[['Repayments in $', 'lat', 'lon']]
            st.pydeck_chart(
                pdk.Deck(
                    map_style='mapbox://styles/mapbox/light-v9',
                    initial_view_state=pdk.ViewState(
                        latitude=40.755684,
                        longitude=-73.883072,
                        zoom=10,
                        pitch=50,
                    ),
                    layers=[
                        pdk.Layer(
                            'GridLayer',
                            data=filtered_data,
                            get_position='[lon, lat]',
                            cell_size=200,
                            elevation_scale=4,
                            elevation_range=[0, 100],
                            pickable=True,
                            extruded=True,
                        ),
                    ],
                ))
            data = data.drop(['lat', 'lon'], axis=1)

        data = data.applymap(str)
        #fig = ff.create_table(data, colorscale=colorscale)
        #st.plotly_chart(fig, use_container_width=True)
        grid = AgGrid(data)

