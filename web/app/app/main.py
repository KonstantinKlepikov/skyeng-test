import streamlit as st
import requests, os
import streamlit_nested_layout


API_ROOT = os.environ.get('API_ROOT')
if not API_ROOT:
    raise RuntimeError('Api root uri not set')

API_VERSION: str = "api/v1"
st.set_page_config(page_title='Dashboard', layout="wide")


def main():

    st.text('Hello world!')


if __name__ == '__main__':
    main()
