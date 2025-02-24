import streamlit as st
import psutil
import plotly.express as px
from source.auth import get_authentication
from source.dbconnector import get_data_polars, get_data_pandas
from source.file_opener import sql_open


def get_user_data() -> list:
    client_df = get_data_pandas(dbname=st.secrets['local_db']['url'],
                                query=sql_open(st.secrets['queries']['client']).format(st.session_state['username']))
    client_loans_df = get_data_pandas(dbname=st.secrets['local_db']['url'],
                                query=sql_open(st.secrets['queries']['client_loans']).format(
                                    st.session_state['username']))
    client_offers_df = get_data_pandas(dbname=st.secrets['local_db']['url'],
                                query=sql_open(st.secrets['queries']['client_offers']).format(
                                    st.session_state['username']))
    response = [{"role": "system", "content": '''
                Нужно помочь твоему собеседнику с получением кредита в Сбербанке.
                Для этого ты должен ему порекомендовать некие действия для получения кредита.
                Рекомендации давать только людям которым больше 18 лет.
                Сначала поговори с собеседником и отвечай вежливо.
                
                Отвечать нужно только по поводу кредитования и данных собеседника, на остальные вопросы отвечай:
                    Не могу подсказать в данном вопросе.
                    
                --
                Твой собеседник: {}, возраст {}, категория клиента {}.
                У него есть: кредиты {}, просроченный платеж {}, ежемесячный платеж {} соответственно (в рублях).
                Его актуальные предложения от Сбербанка: продукт {}, одобренная сумма {}, рекомендации к действию {}.
                Чтобы получить кредит в Сбере ему нужно на основе рекомендаций выше, понять что делать
                '''.format(client_df.to_dict('records')[0]['name']
                           , client_df.to_dict('records')[0]['age']
                           , client_df.to_dict('records')[0]['group_info']
                           , ', '.join([x['loan_id'] for x in client_loans_df.to_dict('records')])
                           , ', '.join([str(x['current_overdue']) for x in client_loans_df.to_dict('records')])
                           , ', '.join([str(x['current_loan_payments']) for x in client_loans_df.to_dict('records')])
                           , ', '.join([str(x['product']) for x in client_offers_df.to_dict('records')])
                           , ', '.join([str(x['approved_sum']) for x in client_offers_df.to_dict('records')])
                           , ', '.join([x['recommendation'] for x in client_offers_df.to_dict('records')]))}]
    return response


if __name__ == '__main__':

    # pages config
    st.set_page_config(
        page_title="Welcome page",
        page_icon="Welcome",
    )

    # memory
    available_vmem = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 2)

    if 'st_started' not in st.session_state:
        with st.spinner("Starting"):
            st.session_state['st_started'] = True

    authenticator = get_authentication(st.secrets)
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)
    if st.session_state['authentication_status']:
        # st.write(st.session_state)
        st.header(f'Welcome, {st.session_state['username']}!', divider="rainbow")
        st.session_state['cache_loaded'] = False
        st.session_state['user_system_info'] = get_user_data()
        # st.write(st.session_state['user_system_info'])
        authenticator.logout()
        # start page
        st.write("# Welcome to the main page")
        st.plotly_chart(
            px.pie(values=[psutil.cpu_percent(), 100 - psutil.cpu_percent()],
                   names=["Used CPU", "Free CPU"],
                   color=["Used CPU", "Free CPU"],
                   color_discrete_map={"Used CPU": "orange", "Free CPU": "lightblue"},
                   hole=0.5)
        )
        st.plotly_chart(px.pie(values=[psutil.virtual_memory().percent, 100 - psutil.virtual_memory().percent],
                               names=["Used VMEM", "Free VMEM"],
                               color=["Used VMEM", "Free VMEM"],
                               color_discrete_map={"Used VMEM": "orange", "Free VMEM": "lightblue"},
                               hole=0.5))
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')
