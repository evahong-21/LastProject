import streamlit as st
import pandas as pd
import joblib
import time
import matplotlib.pyplot as plt
import numpy as np
import os
from herg_predict import predict
from streamlit_download_button import download_button

def predict_herg(data):
    vect = predict(data)
    y_predict_label = cf.predict(des_list)
    y_predict_proba = cf.predict_proba(des_list)

    l_y_pre = []
    for i in range(len(y_predict_label)):
        l_y_pre.append(y_predict_label[i])
    d_y_pre = pd.DataFrame(l_y_pre)
    return d_y_pre

def main():
    ### side bar : hERG, ADMET, ETC, ...
    add_selectbox = st.sidebar.selectbox(
        "Select Model",
        ("hERG", "ADMET", "ETC")
    )


    st.title("hERG-Block prediction (classification)")
    st.subheader("With Streamlit")

    if add_selectbox == 'hERG':
        st.text('hERG Prediction')
        check = st.checkbox("Direct Input")
        check1 = st.checkbox("Upload File")
     
        if check:
            in_data = st.text_input("Input data","ID,SMILES")

            if in_data is not None:
                st.text("Input")
                in_data1 = [in_data.split(',')]
                input_data = pd.DataFrame(in_data1,columns=["ID","SMILES"])
                st.table(input_data)

            if st.button('submit'):
                df = predict(input_data,"hERG_stream")
                st.text("Output")
                st.table(df)
                df1= df.sort_values(by=["Fx"])
                st.line_chart(df1["Fx"], width=0, height=0)
                fig, ax = plt.subplots()
                ax.hist(df["Fx"], bins=20)
                st.pyplot(fig,clear_figure=True)
                filename = 'result.csv'

                download_button_str = download_button(df, filename, f'Click here to download : {filename}', pickle_it=False)
                st.markdown(download_button_str, unsafe_allow_html=True)


        if check1:
            upfile = st.file_uploader("Select Input Data File for Prediction", type=["csv", "txt"])
            if upfile is not None:
                with st.spinner("wait for it..."):
                    input_data = pd.read_csv(upfile)
                    st.text("Input")
                    st.table(input_data)

            if st.button('submit'):
                df = predict(input_data,"hERG_stream")
                st.text("Output")
                st.table(df)
                df1= df.sort_values(by=["Fx"])
                st.line_chart(df1["Fx"], width=0, height=0)
                fig, ax = plt.subplots()
                ax.hist(df["Fx"], bins=20)
                st.pyplot(fig,clear_figure=True)
                filename = 'result.csv'

                download_button_str = download_button(df, filename, f'Click here to download : {filename}', pickle_it=False)
                st.markdown(download_button_str, unsafe_allow_html=True)


    elif add_selectbox == 'ADMET':
        st.text('ADMET Prediction')
        name = st.text_input("Enter smiles","Type here")
    
        upfile = st.file_uploader("Select Input Data File for Prediction", type=["csv", "txt"])
   
        if upfile is not None:
            with st.spinner("wait for it..."):
                input_data = pd.read_csv(upfile)
                st.table(input_data)

        if st.button('submit'):
            st.text("SMILE code : {}".format(name.title()))

            result = predict_herg(name)
            st.write(result)

    
        st.text("***Unmatched streamlit python version with ADMET herg Model,,, Need to Modify***")

if __name__=='__main__':
    main()
