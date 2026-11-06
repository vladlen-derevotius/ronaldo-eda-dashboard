# Cristiano Ronaldo: EDA & Interactive Dashboard

Учебный проект по анализу данных (EDA) и созданию интерактивного дашборда на основе датасета голов Криштиану Роналду (816 голов).

##  О проекте
Цель работы — провести глубокий разведочный анализ данных (EDA) карьеры футболиста и визуализировать результаты в виде интерактивного веб-приложения.

Что внутри:
- notebooks/eda_ronaldo.ipynb — Jupyter Notebook с полным исследованием: статистика по сезонам, турнирам, способам голов и минутам.
- app.py — интерактивный Streamlit-дашборд с фильтрами по турнирам и локации матчей.
- src/data_loader.py — модуль с функциями очистки и предобработки данных (используется и в ноутбуке, и в приложении).

##  Live Demo
 [Открыть дашборд на Streamlit Cloud](#)  
**

## 🛠 Технологии
- Язык: Python 3
- Анализ данных: Pandas, NumPy
- Визуализация: Matplotlib, Seaborn
- Веб-интерфейс: Streamlit

##  Структура проекта
- app.py — Точка входа для Streamlit
- requirements.txt — Зависимости проекта
- data/ — Исходный датасет (CSV)
- notebooks/ — Jupyter ноутбуки (EDA)
- src/ — Модули с Python-кодом (data_loader.py)
- assets/ — Графики и фото для презентации

##  Как запустить локально

1. Клонируйте репозиторий:
git clone https://github.com/ваш-username/ronaldo-eda-dashboard.git
cd ronaldo-eda-dashboard

2. Создайте виртуальное окружение и установите зависимости:
python -m venv .venv
source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
pip install -r requirements.txt

3. Запустите приложение:
streamlit run app.py
##  Авторы
- Валерий
- Сергей  
 Сяп