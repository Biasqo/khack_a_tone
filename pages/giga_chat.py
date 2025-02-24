import streamlit as st
import datetime
import json
from source.api_methods import get_model_data
from source.api_methods import get_uuid
from source.cacher import cache_messages, load_cache, create_cache, remove_cache


def read_cache() -> None:
    '''
    Method read cache
    :return: None
    '''
    create_cache(system_data=st.session_state['user_system_info']
                 , path=st.secrets['cache_path']['path']
                 , user_id=st.session_state['username'])
    st.session_state['messages'] = load_cache(path=st.secrets['cache_path']['path'],
                                              user_id=st.session_state['username'])
    st.toast('Cache loaded')


def get_token(uuid: str) -> dict:
    '''
    Method returns token for Gigachat API
    :param uuid: random generated uuid
    :return: dict
    '''
    # get token
    token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': uuid,
        'Authorization': f'Basic {st.secrets['gigachat_data']['auth_key']}'
    }

    response, status = get_model_data(
        url=st.secrets['model_auth']['url']
        , payload=st.secrets['model_auth']['payload']
        , headers=token_headers
        , method="POST"
    )
    if status == 200:
        st.toast('Got a token!')
        return response.json()
    else:
        st.warning(f"Oops, status code {status}")
        st.stop()


def get_model_types(token: str) -> dict:
    '''
    Method returns list of available models
    :param token: token
    :return: dict
    '''
    # get models
    model_headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response, status = get_model_data(
        url=st.secrets['model_api']['url']
        , payload=st.secrets['model_api']['payload']
        , headers=model_headers
        , method="GET"
    )
    if status == 200:
        return response.json()
    else:
        st.warning(f"Oops, status code {status}")
        st.stop()


def get_response_from_model(model: str) -> str:
    '''
    Method returns user input and model result
    :param model: model type
    :return: model response
    '''
    prompt_payload = json.dumps({
        "model": model,
        "messages": st.session_state['messages'],
        "stream": False,
        "update_interval": 0
    })
    prompt_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {st.session_state['token_data']['access_token']}'
    }

    response, status = get_model_data(
        url=st.secrets['model_answer_api']['url']
        , payload=prompt_payload
        , headers=prompt_headers
        , method="POST"
    )

    return './/.'.join([x['message']['content'] for x in response.json()['choices']])


if __name__ == '__main__':
    if {'authentication_status', 'cache_loaded', 'user_system_info'} - set(st.session_state):
        st.switch_page("main.py")
    elif st.session_state['authentication_status']:
        if not st.session_state['cache_loaded']:
            read_cache()
            st.session_state['cache_loaded'] = True

        st.session_state['user_uuid'] = get_uuid()

        st.header('Click `Get token` to acquire a token!', divider='rainbow')
        # get token
        token_button = st.button("Get token")
        if token_button:
            st.session_state['token_data'] = get_token(uuid=st.session_state['user_uuid'])
            st.session_state['token_expire'] = datetime.datetime.fromtimestamp(
                st.session_state['token_data']['expires_at'] / 1000)
        if 'token_data' in st.session_state.keys():
            # expiration date
            st.caption(f"Token expires at: {st.session_state['token_expire']}")

            # model types
            prompt_disabled = True
            model_types = get_model_types(token=st.session_state['token_data']['access_token'])
            model_selection = st.pills('Choose available model: ', [x['id'] for x in model_types['data']],
                                       selection_mode='single')

            if model_selection:
                prompt_disabled = False

            if "messages" not in st.session_state:
                st.session_state['messages'] = []

            with st.sidebar:
                clear_chat = st.button('Clear chat')
                if clear_chat:
                    st.session_state['messages'] = st.session_state['user_system_info']
                    remove_cache(system_data=st.session_state['user_system_info']
                                 , path=st.secrets['cache_path']['path']
                                 , user_id=st.session_state['username'])

            # history
            for message in st.session_state['messages']:
                # if message['role'] != 'system':
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # react to user input
            if prompt := st.chat_input("Ask AI", disabled=prompt_disabled):
                # display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)
                # add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                model_message = get_response_from_model(model=model_selection)
                # display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(model_message)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": model_message})
                cache_messages(data=st.session_state['messages'], path=st.secrets['cache_path']['path'],
                               user_id=st.session_state['username'])

    else:
        st.warning('Please enter your username and password on main page')
