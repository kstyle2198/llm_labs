import streamlit as st
import os
from stqdm import stqdm
import pandas as pd
import time

from utils import CustomDrawingParser
import sys
sys.path.append("../")
from style import make_title, make_gap, button_style, custom_page_config

custom_page_config(layout='wide')
button_style()



cdp = CustomDrawingParser()

from pathlib import Path
parent_dir = Path(__file__).parent.parent
base_dir = str(parent_dir) + "\images"
all_contents = os.listdir(base_dir)
folder_names = [folder for folder in all_contents if os.path.isdir(os.path.join(base_dir, folder))]


if "paths" not in st.session_state:
    st.session_state.df = pd.DataFrame()
    st.session_state.predictions = []
    st.session_state.paths = []

if __name__ == "__main__":
    make_title(emoji="🧪", title="Drawing Parser")
    make_gap(height=50)

    sel99 = st.selectbox("이미지폴더선택", folder_names, index=None)
    file_dir = base_dir + f"\{sel99}"
    

    file_names = os.listdir(file_dir)

    filenames = []
    pages = []
    orders = []
    st.session_state.paths = []
    word_list = []
    predictions = []
    image_paths= []

    length = len(file_names)
    increment = 1
    progress = stqdm(total=length)


    with st.spinner("Processing..."):
        if st.button("Drawing Parsing"):
            st.session_state.df = pd.DataFrame()
            index = 0
            index += increment
            
            
            for img in file_names:

                if index == length:
                    break

                splitted_img = img.split(".")
                page_num = splitted_img[0].split("_")[0]
                order_num = splitted_img[0].split("_")[-1]
                image_path = file_dir + f"\{img}"
                prediction = cdp.keras_ocr_extract_prediction(image_path)
                words = [pred[0] for pred in prediction]
                words = ",".join(words)
                
                pages.append(page_num)
                orders.append(order_num)
                st.session_state.paths.append(image_path)
                word_list.append(words)
                st.session_state.predictions.append(prediction)

                progress.update(increment)
                time.sleep(0.5)
        
            st.session_state.df["filenames"] = st.session_state.filenames
            st.session_state.df["pages"] = pages
            st.session_state.df["orders"] = orders
            st.session_state.df["paths"] = st.session_state.paths
            st.session_state.df["words"] = word_list


            
    st.session_state.df
    st.session_state.paths

      
    image_path99 = st.selectbox("Image_path", st.session_state.paths)
    sel9999 = st.number_input("number", min_value=0, step=1)
    prediction1 = st.session_state.predictions[sel9999]
    cdp.show_drawings(image_path99, prediction1)
    


