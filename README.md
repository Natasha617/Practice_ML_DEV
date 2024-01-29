<h1><b>Мониторинг безопасности одиноких пожилых людей</b></h1>
<h1>Описание задачи</h1>
<p>Задача - создать модель машинного обучения для мониторинга безопасности одиноких пожилых людей на основе данных от датчиков газа, температуры и инфракрасных датчиков движения. Модель должна способна определять аномалии и необычное поведение, которые могут потребовать вмешательства или помощи.</p>

<h2>ML задачи</h2>
* провести входной анализ данных (EDA) <br>
* определить метрики для оценки эффективности модели<br>
* сформировть baseline-модель<br>
* предложить улучшенную модель и вывести ее в продакшн<br>

<h2>Описание датасета</h2>

Датасет содержит данные от датчиков газа и температуры, а также инфракрасных датчиков движения, установленных для мониторинга пожилого человека, проживающего один в собственном доме с 2019-11-06 по 2020-02-13. Измерения проводились с временным разрешением в 20 секунд. Датчики воздуха и газа измеряют температуру, влажность, уровень CO2, CO и MOX. Данные от датчиков позиции бинарны: для каждой комнаты 1 означает обнаружение движения в комнате, в то время как 0 означает возврат сенсора к базовому состоянию. Датасет также включает в себя 19 дней измерений (с 2020-01-25 по 2020-02-13), когда никто не находился в помещении (за исключением случайного посещения 2020-01-29 в 15:00) и используется в качестве эталонных данных. Разрешается использовать не весь набор признаков.

Сначала требовалось разметить данные опираясь на датасет с эталонными данными <br> 
В качестве baseline модели использовалась логистическая регрессия.<br>
А лучший результат показали <b>RandomForest</b> и <b>CatBoost</b>

Далее был разработан сервис на основе FastAPI (back) и Streamlit(front), где пользователь мог пройти авторизацию, ввести показания с датчиков, выбрать модель и получить предсказание.
<br>

<img src = https://github.com/Natasha617/Practice_ML_DEV/assets/57916950/739dd389-9fae-443f-9a3c-240a341ef153>
<hr>

Для того, чтобы запустить это приложение вы можете скачать файлы из репозитория и запустить FastAPI и Streamlit в разных терминалах c помощью команд:
<br>

<code> streamlit run ml_app.py</code>

<code> uvicorn fastapi_app:app --reload</code>

