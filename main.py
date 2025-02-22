import streamlit as st
import psutil
import plotly.express as px
from source.auth import get_authentication

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
        st.session_state['cache_loaded'] = False
        st.session_state['user_system_info'] = [{"role": "system", "content": '''
                Представь что ты разговариваешь с Ивановым Иваном Ивановичем.
                У него 3 потребительских кредита на сумму 350000 рублей в Альфа банке
                    , 2 ипотеки на сумму 3000000 рублей в ВТБ и кредитная карта в Сбере с лимитом 100000 рублей.
                Он не является клиентом Сбера.
                Чтобы получить кредит в Сбере ему нужно: обязательно принести справку о доходе 2НДФЛ
                    , по желанию закрыть ипотеку в ВТБ
                Отвечать нужно только по поводу кредитования и данных собеседника, на остальные вопросы отвечай:
                    Не могу подсказать в данном вопросе
                '''}]
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
