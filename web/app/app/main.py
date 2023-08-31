import os
import requests
from requests import Response
import streamlit_nested_layout
import streamlit as st
from streamlit.delta_generator import DeltaGenerator


API_ROOT = os.environ.get('API_ROOT')
if not API_ROOT:
    raise RuntimeError('Api root uri not set')

API_VERSION: str = "api/v1"
st.set_page_config(page_title='Dashboard', layout="wide")


def show_api_error(r: Response) -> None:
    """Write error from response

    Args:
        r (Response): response object
    """
    detail = r.json()['detail']
    if isinstance(detail, list):
        st.write('Data validation error. Insert correct data.')
    else:
        st.write(r.json()['detail'])
    st.stop()


def get_files() -> None:
    """_summary_
    """
    token = st.session_state.get('access_token')
    url = os.path.join(API_ROOT, API_VERSION, 'files')
    r = requests.get(
        url,
        headers={
            'Authorization': f'Bearer {token}'
                }
            )
    if r.status_code == 200:
        st.session_state['files'] = r.json()['files']
    else:
        show_api_error(r)


def upload_file() -> None:
    """Upload new file
    """
    token = st.session_state.get('access_token')
    url = os.path.join(API_ROOT, API_VERSION, 'files/file')

    with st.form("upload_new", clear_on_submit=True):
        uploaded_file = st.file_uploader("Upload new file")
        submitted = st.form_submit_button("Upload")

        if submitted and uploaded_file is not None:
            file = {'file': (uploaded_file.name, uploaded_file.getvalue())}
            r = requests.post(
                url,
                files=file,
                headers={
                    'Authorization': f'Bearer {token}'
                        }
                )
            if r.status_code == 201:
                get_files()
            else:
                show_api_error(r)


def upload_file_for_change(file_id: str) -> None:
    """Upload changed file and refresh data
    """
    token = st.session_state.get('access_token')
    url = os.path.join(API_ROOT, API_VERSION, 'files/file')

    with st.form(file_id, clear_on_submit=True):
        uploaded_file = st.file_uploader("Upload changed file")
        submitted = st.form_submit_button("Upload")

        if submitted and uploaded_file is not None:
            file = {'file': (uploaded_file.name, uploaded_file.getvalue())}
            r = requests.put(
                url,
                files=file,
                params={"id": file_id},
                headers={
                    'Authorization': f'Bearer {token}'
                        }
                    )
            if r.status_code == 201:
                get_files()
                st.session_state['reload'] = True
            else:
                show_api_error(r)


def show_log_in(holder: DeltaGenerator) -> None:
    """Right side log in scenario

    Args:
        holder (DeltaGenerator): holder for change and clear displayed data
    """
    st.write('Log in:')

    with st.form("login_form"):
        email = st.text_input(label='email:')
        password = st.text_input(label='password:')
        submit = st.form_submit_button(label='login')
        st.write('or')
        create = st.form_submit_button(label='create account')

        if submit:
            url = os.path.join(API_ROOT, API_VERSION, 'users/login')
            r = requests.post(
                url,
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                        },
                data={"username": f"{email}", "password": f"{password}"}
                )

            if r.status_code == 200:
                st.session_state['access_token'] = r.json()['access_token']
                st.session_state['email'] = email
                holder.empty()
            else:
                show_api_error(r)

        if create:
            url = os.path.join(API_ROOT, API_VERSION, 'users/create')
            r = requests.post(
                url,
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                        },
                json={"email": f"{email}", "password": f"{password}"}
                )

            if r.status_code == 201:
                st.write('Success!')
            else:
                show_api_error(r)


def show_autorized() -> None:
    """Right side autorized scenario
    """
    st.caption('Login as:')
    st.subheader(f"**{st.session_state['email']}**")
    logout = st.button("logout")

    get_files()

    if logout:
        st.session_state['access_token'] = None
        st.session_state['email'] = None
        st.session_state['files'] = None
        st.experimental_rerun()


def main():

    left, _ = st.columns([1, 2], gap='medium')

    with left:
        holder1 = st.empty()
        with holder1.container():
            if st.session_state.get('access_token') is None:
                show_log_in(holder1)

        if st.session_state.get('access_token'):
            show_autorized()

        st.markdown('---')

        if st.session_state.get('files') is not None:
            st.subheader('Upload new file')
            upload_file()

            st.header('Your uploaded files')
            st.markdown('---')

            with st.container():

                for k, v in st.session_state['files'].items():
                    st.write(f'{v}'+'.py')

                    if st.button(label="Download", key=f"download{k}"):
                        st.write('Downloaded!')

                    if st.button(label="Delete", key=f"delete{k}"):
                        st.write('Delened!')

                    upload_file_for_change(file_id=k)

                if st.session_state.get('reload'):
                    st.session_state['reload'] = False
                    st.experimental_rerun()


if __name__ == '__main__':
    main()
