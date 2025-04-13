# Основные понятия


DTL (Django Template Language)
____
Template expression & template variable 


view (представление)    
----  
Функция или класс принимающая HTTP-запрос и вовзращающая HTTP-ответ.

Содержит:  
-Логику обработки запроса  
-Логику извлечения данных 
-Логику выбора способа их представления (HTML, JSON, etc.)

Задача: 
Вернуть соотвествующий ответ в зависимости от запроса.  
Чаще всего это данные полученные из модели переданные в шаблон или сериализованные

Классический пример:
```python  
# View для страницы пользователя
def user_profile_view(request):

    # получаем данные пользователя 
    user_object = request.user

    # проверяем полученные данные на содержимое 
    if user_object.first_name and user_object.last_name:
        user_name = user_object.first_name + ' ' + user_object.last_name
    else:
        user_name = "anonymous"

    # 
    context = {
        'title': f'ваш профиль {user_name}'
    }
    
    return render(request, 'users/user_profile_read_only.html', context=context)
```

context  - это словарь с данными, который передается в шаблон для отображения.  
В шаблоне эти данные можно использовать например так: {{ title }}

render - это функция которая принимает объект запроса, файл шаблона и словарь context в качестве аргументов 
и возвращает готовый html-ответ c подставленными данными
