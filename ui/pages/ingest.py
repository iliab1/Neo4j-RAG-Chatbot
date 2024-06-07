import streamlit as st
import requests


st.title('Document Loader')

uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, type=["pdf"])
upload_button = st.button("Upload Files")

upload_url = "http://api:8080/file/upload"
if upload_button and uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f'Uploading and processing {uploaded_file.name}...'):
            file = {"uploaded_file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(upload_url, files=file)
        if response.status_code == 200:
            response_json = response.json()
            st.success(response_json["INFO"])
        else:
            st.error(f"Failed to upload {uploaded_file.name}. Please try again.")

list_files_url = "http://api:8080/files"
st.header('Uploaded Files')
response = requests.get(list_files_url)
if response.status_code == 200:
    files = response.json().get("files", [])
    for file in files:
        file_url = f"http://api:8080/files/{file}"
        st.markdown(f"[{file}]({file_url})")
else:
    st.write("Failed to retrieve files")
