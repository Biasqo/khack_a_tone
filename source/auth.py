import streamlit_authenticator as stauth

def get_authentication(secrets_dict: dict) -> stauth.Authenticate:
    '''
    Method to auth user into app
    :param secrets_dict: dict of server secrets
    :return: authenticator
    '''
    authenticator = stauth.Authenticate(
        secrets_dict['credentials'].to_dict(),
        secrets_dict['cookie']['name'],
        secrets_dict['cookie']['key'],
        secrets_dict['cookie']['expiry_days'],
        secrets_dict['preauthorized']
    )
    return authenticator