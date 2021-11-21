import streamlit as st
import pandas as pd
import joblib
import time
import matplotlib.pyplot as plt
import numpy as np
import os,sys
from PP04_predict import predict
from streamlit_download_button import download_button
from PIL import Image
from biodl.dlxy import DLXY 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from biodl.mxy import MXY
import tensorflow as tf
os.environ["CUDA_VISIBLE_DEVICES"]='0'
config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.8
tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))

def pre_submit(_input):
    with st.spinner("wait for it..."):
        df = predict(_input,"PP04_predict")
        st.text("Output")
        st.dataframe(df)
        filename = 'result.csv'
        download_button_str = download_button(df, filename, f'Click here to download : {filename}', pickle_it=False)
        st.markdown(download_button_str, unsafe_allow_html=True)


def ad_submit(_input, desc):
    with st.spinner("wait for it..."):
        df = predict(_input,"PP04_predict_AD")
        if desc =="xmg":
            dlxmg = DLXY('dl_xmg')
            dlxmg.Reload('dl_xmg',"./PP04_predict_AD")

            l_a = []
            for i in range(len(list(dlxmg.d_x.values()))):
                l_a.append(pd.DataFrame(list(dlxmg.d_x.values())[i][0],columns=[i]))
            df_pre = pd.concat(l_a,axis=1).transpose()
            df_pre["type"]="Predict"
            
            df_train = pd.read_csv("./AD/AD_xmg.csv")
            df_train["type"]="None"
            df_train["type"] = "Train_Inhibitor"
            df_train["type"] = "Train_Non_Inhibitor"
            
            a = list(range(1792))
            a.append("type")
            df_pre.columns = a
            df_train.columns = a
            df_all_Kinase = pd.concat([df_train, df_pre])
            df_all_Kinase.reset_index(drop=True,inplace=True)
            
            pca = PCA(n_components=2) # 주성분을 몇개로 할지 결정
            printcipalComponents = pca.fit_transform(df_all_Kinase.iloc[:,0:1792])
            principalDf = pd.DataFrame(data=printcipalComponents, columns = ['principal component1', 'principal component2'])
            # 주성분으로 이루어진 데이터 프레임 구성
            
            finalDataFrame = pd.concat([principalDf,df_all_Kinase["type"]],axis=1)
            st.write("주성분 2개에서 각 퍼센트 :",pca.explained_variance_ratio_)
            st.write("주성분 2개 퍼센트 합 :", round(sum(pca.explained_variance_ratio_),3))
            labels = ["Train_Inhibitor","Train_NonInhibitor","Prediction"]
            fig = plt.figure(figsize = (12,12))
            ax = fig.add_subplot(1,1,1)
            ax.set_xlabel('Principal Component 1', fontsize = 15)
            ax.set_ylabel('Principal Component 2', fontsize = 15)
            ax.set_title('Applicability Domain', fontsize = 20)
            ax.scatter(principalDf["principal component1"][:105515], principalDf["principal component2"][:105515], c='r', s=0.1)
            ax.scatter(principalDf["principal component1"][105515:172132], principalDf["principal component2"][105515:172132], c='g', s=0.1)
            ax.scatter(principalDf["principal component1"][172132:], principalDf["principal component2"][172132:], c='b', s=10)
            ax.legend(labels)
            ax.grid()
            plt.savefig("./AD/AD_xmg.png")
            image = Image.open('./AD/AD_xmg.png')
            st.image(image, caption='AiGPro(PP04) Applicability Domain')

def chk_direct_input():
    in_data = st.text_input("Input data","ID,SMILES")
    if in_data is not None:
        st.text("Input")
        in_data1 = [in_data.split(',')]
        dir_input_data = pd.DataFrame(in_data1,columns=["ID","SMILES"])
        st.table(dir_input_data) 
        return dir_input_data   


def chk_upload_input():
    upfile = st.file_uploader("Select Input Data File for Prediction", type=["csv", "txt"])
    if upfile is not None:
        with st.spinner("wait for it..."):
            up_input_data = pd.read_csv(upfile)
            st.text("Input")
            st.table(up_input_data)   
        return up_input_data

def chk_direct(_input):
    # prediction
    if _input =="sub_pre":
        chk_input_data_0 = chk_direct_input()
        if st.button('submit'):
            pre_submit(chk_input_data_0)
    # Applicability Domain
    elif _input =="ad_pre":
        chk_input_data_1 = chk_direct_input()
        if st.button('xlx'):
            ad_submit(chk_input_data_1, "xlx")
        elif st.button('xmg'):
            ad_submit(chk_input_data_1, "xmg")
        elif st.button('x3d'):
            ad_submit(chk_input_data_1, "x3d")               


def chk_upload(_input):
    # prediction 
    if _input == "sub_pre":
        chk_input_data_2 = chk_upload_input()
        if st.button('submit'):
            pre_submit(chk_input_data_2)
    # Applicability Domain
    elif _input =="ad_pre":
        chk_input_data_3 = chk_upload_input()
        if st.button('xlx'):
            ad_submit(chk_input_data_3, "xlx")
        elif st.button('xmg'):
            ad_submit(chk_input_data_3, "xmg")
        elif st.button('x3d'):
            ad_submit(chk_input_data_3, "x3d")   


def chk_model():
    st.text('Datasets & Model description')
    st.write("1. Datasets")
    df_tab1 = pd.read_csv("./PP04_data.csv")
    df_tab1 = df_tab1.rename(index={0:'Datasets'})
    st.table(df_tab1)    
    st.write("2. Model Performance")
    image = Image.open('./model/PP04_train/0.png')
    st.image(image, caption='AiGPro(PP04) Model Performance')
    st.write("3. Validation test sets Performance") 
    df_tab = pd.read_csv("./PP04_perf.csv")
    df_tab = df_tab.rename(index={0:'Value'})
    st.table(df_tab)


def chk_pred():
    st.text('AiGPro(PP04) Prediction')
    check = st.checkbox("Direct Input")
    check1 = st.checkbox("Upload File")
    if check: #Direct Input
        chk_direct("sub_pre")
    elif check1: #Upload File
        chk_upload("sub_pre")


def chk_ad():
    st.text('Check Aplicability Domain')
    check = st.checkbox("Direct Input")
    check1 = st.checkbox("Upload File")
    if check: #Direct Input
        chk_direct("ad_pre")
    elif check1: #Upload File
        chk_upload("ad_pre")


def main():
    add_selectbox = st.sidebar.selectbox(
        "PP04_AiGPro",
        ("Model", "Prediction", "AD")
    )

    st.title("AiGPro(PP04) prediction : classification")
    st.subheader("Made by Azothbio")

    if add_selectbox == 'Model':
        chk_model()

    elif add_selectbox == 'Prediction':
        chk_pred()
        
    elif add_selectbox == 'AD':
        chk_ad()
        

if __name__ == '__main__':
    main()
