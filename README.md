### Хакатон AI Риски

version: indev_1.0

#### Описание
В этом репозитории находится код для AI бота на основе `streamlit`

#### Создание виртуального окружения
Для запуска приложения необходимо создать виртуальное окружение `.venv` \
При запуске через `start.sh` нужно выбрать нужный `python` в блоке `initialize venv`

#### Cache и секрет
При развертывании приложения у вас появится папка `.streamlit` и папка `data`
В папке `.streamlit` необходимо заполнить файлы `config.toml`, `secrets.toml` \
Более подробно о них тут: [секреты](https://docs.streamlit.io/develop/api-reference/connections/secrets.toml),
[конфигурационные файлы](https://docs.streamlit.io/develop/api-reference/configuration/config.toml)

Пример секретов: [secrets.toml](examples/secrets.toml) \
Пример конфига: [config.toml](examples/config.toml)


В папке `data` будет папка `cache` в которую складываются данные переписок по пользователям в формате `.pkl` \
В папке `db` нужно положить тестовую базу данных `local.db` в которой лежат таблицы в соответствии с `ddl` скриптами