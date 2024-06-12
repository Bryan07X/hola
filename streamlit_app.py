import streamlit as st
import pandas as pd
import numpy as np
import base64


#from pulse_sound import play_beep
from ecg_info import theo_data, gif_data

#teo_df = pd.

def read_gif(local_url):
    file_ = open(local_url, "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    return data_url

ans_map = {"Yes":'Sí',"No":"No"}
temp_df = pd.read_csv("./data_theo.csv")

def include_theo():#index_slider):

    ans_all  = [ans_map[c] for c in [c1,c2,c3,c4,c5,c6,c7,c8,c9]]
    
    ans_c1 = temp_df['Ausencia de Onda P'].str.contains(ans_all[0])
    ans_c2 = temp_df['QRS Ancho (>120 ms)'].str.contains(ans_all[1])
    ans_c3 = temp_df['QRS Estrecho (<120 ms)'].str.contains(ans_all[2])
    ans_c4 = temp_df['Frecuencia Cardíaca Alta (>100 bpm)'].str.contains(ans_all[3])
    ans_c5 = temp_df['Frecuencia Cardíaca Baja (<60 bpm)'].str.contains(ans_all[4])
    ans_c6 = temp_df['Intervalo PR Prolongado (>200 ms)'].str.contains(ans_all[5])
    ans_c7 = temp_df['Ondas Fibrilatorias'].str.contains(ans_all[6])
    ans_c8 = temp_df['Mareos/Debilidad'].str.contains(ans_all[7])
    ans_c9 = temp_df['Dolor Torácico'].str.contains(ans_all[8])
    
    ans = temp_df[ans_c1 & ans_c2 & ans_c3 & ans_c4 & ans_c5 & ans_c6 & ans_c7 & ans_c8  & ans_c9]

    index_slider = None if len(ans)==0 else ans.iloc[0]['index']

    if index_slider is not None:
        temp = theo_data[index_slider]
        gif_temp = gif_data[index_slider]
        #st.write(temp['title'])
        st.markdown(f"## {temp['title']}")
        st.write(temp['content'])

        data_url = read_gif(gif_temp)
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="prueba_4" width="700" align="center">',
            unsafe_allow_html=True,
        )

    else:
        st.markdown("## No ECG satisfies these conditions")
        data_url = read_gif("prueba_5.gif")
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="prueba_4" width="700" align="center">',
            unsafe_allow_html=True,
        )
        #st.image(r"prueba_1-5.gif")
        #st.write(f"{temp['content']}")


st.write("""
# ECG Data Explorer  
$\\\\$

## Select the configuration
""")

# Three columns with different widths
col1, col2, col3 = st.columns([2,1,1])

with col1:
    c4 = st.radio("High Heart Rate (>100 bpm)", ["Yes", "No"])
    c5 = st.radio("Low Heart Rate (<60 bpm)", ["Yes", "No"])
    c6 = st.radio("Extended PR Interval (>200 ms)", ["Yes", "No"])

with col2:
    c1 = st.radio("Absence of P Wave", ["Yes", "No"])
    c2 = st.radio("Wide QRS (>120 ms)", ["Yes", "No"])
    c3 = st.radio("Narrow QRS (<120 ms)", ["Yes", "No"])

with col3:
    c7 = st.radio("Fibrilatory Waves", ["Yes", "No"])
    c8 = st.radio("Dizziness/Weakness", ["Yes", "No"])
    c9 = st.radio("Chest Pain", ["Yes", "No"])

#option = st.selectbox("Select a ECG Type: ", range(0,27,1),
#   index=None,
#   placeholder="Select type...",
#)
#select_type = st.slider("Select a ECG Type: ", min_value=1, max_value=27, step=1)
#st.write(option)
#include_theo(option)

#bpm = st.slider("BPM: ",min_value=1, max_value=200)
#rep = st.slider("Pulses: ",min_value=1, max_value=10)

# Button to display the graph
# Check if 'show_graph' is in the session state
if 'show_graph' not in st.session_state:
    st.session_state.show_graph = False

if st.button('Search ECG!'):
    st.session_state.show_graph = True

# Conditionally display the principal title and graph
if st.session_state.show_graph:
    include_theo()


#if button_audio:
#    play_beep(bpm, continuous=False, n_pulses=3)
