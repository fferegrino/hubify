import io
import json
from zipfile import ZipFile

import matplotlib.pyplot as plt
import pandas as pd

import streamlit as st
from hubify import hubify

st.title("My streaming history")


uploaded_files = st.file_uploader("Upload your spotify data", type=[".zip", ".json"], accept_multiple_files=True)

if uploaded_files:
    # To read file as bytes:

    file_names = {
        file.name for file in uploaded_files
    }

    history = []
    if all([file_name.endswith('.json') for file_name in file_names]):
        for uploaded_file in uploaded_files:
            streaming_history = json.loads(uploaded_file.getvalue().decode("utf-8"))
            history.extend(streaming_history)
    elif all([file_name.endswith('.zip') for file_name in file_names]):
        bytes_data = uploaded_files[0].getvalue()
        archive = ZipFile(io.BytesIO(bytes_data), "r")
        streaming_history_files = [name for name in archive.namelist() if name.startswith("MyData/StreamingHistory")]
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
