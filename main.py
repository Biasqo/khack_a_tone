import streamlit as st
import psutil
import plotly.express as px
from source.auth import get_authentication
from source.dbconnector import get_data_polars, get_data_pandas
from source.file_opener import sql_open
from source.agent import Agent


def get_user_data() -> str:
    client_df = get_data_pandas(dbname=st.secrets['local_db']['url'],
                                query=sql_open(st.secrets['queries']['client']).format(st.session_state['username']))
    client_loans_df = get_data_pandas(dbname=st.secrets['local_db']['url'],
                                      query=sql_open(st.secrets['queries']['client_loans']).format(
                                          st.session_state['username']))
    client_offers_df = get_data_pandas(dbname=st.secrets['local_db']['url'],
                                       query=sql_open(st.secrets['queries']['client_offers']).format(
                                           st.session_state['username']))
    preprocessed_db_data_loans = '; '.join([f'Кредит с номером договора: {x['loan_id']},'
                                            f' Продукт кредита: {x['product_name']},'
                                            f' Просроченный платеж по продукту: {x['current_overdue']} рублей,'
                                            f' Ежемесячный платеж по продукту: {x['current_loan_payments']} рублей,\n'
                                            for x in client_loans_df.to_dict('records')])

    preprocessed_db_data_offers = '; '.join([f'Предложение по кредитному продукту: {x['product_name']},'
                                             f' Одобренная сумма по продукту: {x['approved_sum']} рублей,'
                                             f' Рекомендации к действию: {x['recommendation']}\n'
                                             for x in client_offers_df.to_dict('records')])

    response = '''
    --
    Твой клиент: {}, возраст {}, категория клиента {}.
    У него есть: {};
    Его актуальные кредитные предложения от Сбербанка: {}'''.format(
        client_df.to_dict('records')[0]['name']
        , client_df.to_dict('records')[0]['age']
        , client_df.to_dict('records')[0]['group_info']
        , preprocessed_db_data_loans
        , preprocessed_db_data_offers)
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
        st.session_state.agent_creditor = Agent(
            secrets=st.secrets
            , agent_type=[{'role': 'system', 'content': '''
                                            Представь что ты опытный кредитор банка с 30 летним стажем в банке Сбербанк
                                            Твоя задача выслушать клиента и собрать с него максимум информации для получения кредита
                                            Твой клиент: {}
                                            '''.format(st.session_state['user_system_info'])}]
        )

        st.session_state.agent_validator = Agent(
            secrets=st.secrets
            , agent_type=[{'role': 'system', 'content': '''
                                            Представь что ты опытный аудитор банка с 30 летним стажем в банке Сбербанк.
                                            Твоя задача проверить диалог с клиентом и понять адекватно ли сотрудник банка отвечает клиенту
                                            с комментариями. Есть ли связность текста в ответах сотрудника.
                                            '''}]
        )
        st.session_state.agent_recommendation = Agent(
            secrets=st.secrets
            , agent_type=[{'role': 'system', 'content': '''
                                                Представь что ты лицо принимающее решение в банке с опытом работы 30 лет в банке Сбербанк.
                                                Твоя задача проанализировать диалог и сказать что кредитору делать дальше.
                                                Отвечай ему так: кредитор, вот новая информация: 
                                                '''}]
        )
        st.session_state['msg_cnt'] = 0
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
