Кратко о том как работает авториазация в Django:  

    1. Пользователь логинится — через authenticate() → login().  

    2. Django сохраняет ID пользователя в сессии (cookie).  

    3. В каждом запросе Django извлекает пользователя и помещает в request.user.  

    4. Для проверки используется @login_required или request.user.is_authenticated.  

Для API (DRF) — используется токен/сессия/JWT вместо cookie.  
