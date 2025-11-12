Отчёт по ЛР2 - ЛР2.docx
Отчёт по ЛР3 - ЛР3.docx

Для запуска кода 3-ей лабораторной необходимо:
1) клонировать репозиторий
2) в корне проекта прописать команду <b>docker compose up</b> для того, чтобы поднять контейнер с БД
3) создать виртуальное окружение, прописав <b>python -m venv .venv</b>
4) активировать созданное окружение командой <b>.\.venv\Scripts\activate</b> для Windows или <b>source .venv/bin/activate</b> для MacOS и Linux
5) прописать <b>pip install -r requirements.txt</b> для установки зависимостей
6) прописать <b>uvicorn app.main:app --reload </b>
7) прописать <b>alembic upgrade head</b> для применения миграций к БД  
8) Перейти по ссылке http://127.0.0.1:8000/schema/swagger/ будет доступна Swagger-документация
