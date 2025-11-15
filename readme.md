# 🧪 QA Automation Portfolio (Python + Pytest + Playwright)

### 📌 О проекте
Учебный проект для демонстрации навыков автоматизации API и UI тестирования.

### 🛠 Используемые технологии
- Python 3.12  
- Pytest  
- Requests  
- Playwright  
- Allure Report  
- GitHub Actions  

### 🚀 Как запустить
```bash
pip install -r requirements.txt
pytest -v --alluredir=allure-results
allure serve allure-results
```

### API
https://reqres.in/ - CRUD-эндпоинты для пользователей 
https://restful-booker.herokuapp.com/ - CRUD бронирования
https://dummyjson.com/ - товары, пользователи, корзины
https://petstore.swagger.io/ - стандартный Swagger-проект
https://jsonplaceholder.typicode.com/ - посты, комментарии


### UI
https://the-internet.herokuapp.com/ - куча демо-страниц (логин, алерты, загрузки и т.д.)
https://demoqa.com/ - формы, таблицы, модальные окна
https://automationexercise.com/ - реальный e-commerce сайт
https://saucedemo.com/ - демо интернет-магазин

## CI Status
![API CI](https://github.com/<user>/<repo>/actions/workflows/api-ci.yml/badge.svg)
![UI CI](https://github.com/<user>/<repo>/actions/workflows/ui-ci.yml/badge.svg)