import streamlit as st
from streamlit_option_menu import option_menu
import webbrowser
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import numpy as np
import pandas as pd
import re

st.set_page_config(page_title="TOPSIS", page_icon=":tada:", layout="wide")
st.title("TOPSIS")
st.write("Please upload your dataset (in .csv format only)")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write('Here is the sample of the data you provided')
    st.write(data)

    collect_numbers = lambda x : [int(i) for i in re.split("[^0-9]", x) if i != ""]
    numbers = st.text_input("Enter the weights (Please input the numbers separated with a single comma)")
    string = st.text_input("Enter the impacts (Please input + or - separeated with a single comma)")
    impact = string.split(",")
    weights = collect_numbers(numbers)

    go = st.button('Analyze')
    if go:
        df = data.drop(data.columns[[0]], axis=1)

        sos = []
        for i in range(df.shape[1]):
            sum = 0
            for j in range(df.shape[0]):
                sum = sum + df.iloc[j,i]**2
            sos.append(sum)

        rosos = np.sqrt(sos)

        for i in range(df.shape[1]):
            for j in range(df.shape[0]):
                df.iloc[j,i] = df.iloc[j,i] / rosos[i]

        for i in range(df.shape[1]):
            for j in range(df.shape[0]):
                df.iloc[j,i] = df.iloc[j,i] * weights[i]

        idbest = []
        idworst = []

        for i in range(df.shape[1]):
            if impact[i] == '+':
                idbest.append(df.iloc[:,1].max(axis=0))
                idworst.append(df.iloc[:,1].min(axis=0))

            elif impact[i] == '-':
                idbest.append(df.iloc[:,1].min(axis=0))
                idworst.append(df.iloc[:,1].max(axis=0))

        sp = []
        sn = []
        for i in range(df.shape[0]):
            sump = 0
            sumn = 0
            for j in range(df.shape[1]):
                sump = sump + (df.iloc[i,j] - idbest[j])**2
                sumn = sumn + (df.iloc[i,j] - idworst[j])**2

            sp.append(sump)
            sn.append(sumn)

        sp = np.sqrt(sp)
        sn = np.sqrt(sn)

        p = []
        for i in range(df.shape[0]):
            p.append(sn[i] / (sp[i]+sn[i]))

        data['P'] = p
        data['Rank'] = data['P'].rank()
        st.write(data)
