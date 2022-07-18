import io
import json
from zipfile import ZipFile

import matplotlib.pyplot as plt
import pandas as pd

import streamlit as st
from hubify import hubify

st.title("My streaming history")


uploaded_file = st.file_uploader("Upload your spotify data", type=[".zip"], accept_multiple_files=False)

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    archive = ZipFile(io.BytesIO(bytes_data), "r")
    streaming_history_files = [name for name in archive.namelist() if name.startswith("MyData/StreamingHistory")]

    history = []
    for streaming_file in streaming_history_files:
        streaming_history = json.load(archive.open(streaming_file))
        history.extend(streaming_history)

    full_history = pd.DataFrame(history)
    end_times = pd.to_datetime(full_history["endTime"])
    fig = plt.figure(figsize=(10, 3), dpi=250)
    ax = hubify(end_times)

    title = st.text_input("Plot title")

    ax.set_title(title)
    st.pyplot(fig)
