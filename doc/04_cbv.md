# Class Based Views  
  
----
## Основные методы в CBV:  
  
get()                           Обрабатывает GET-запрос (открытие страницы).  
post()                          Обрабатывает POST-запрос (отправка формы).  
form_valid(form)	            Что делать, если форма прошла валидацию.  
form_invalid(form)	            Что делать, если форма не прошла валидацию.  
get_queryset()	                Каким QuerySet'ом заполнять список объектов (ListView).  
get_object()	                Как получить конкретный объект (DetailView, UpdateView, DeleteView).  
get_context_data(**kwargs)	    Дополнить контекст шаблона своими данными.  
get_success_url()	            Куда перенаправлять пользователя после успешной операции. 


----
## Набор стандартных базовых CBV

### Базовые классы:
View	                        Самый базовый класс. Просто принимает HTTP-запрос и вызывает dispatch(). Всё остальное нужно писать вручную.  
TemplateView	                Просто отдает шаблон (template_name) и контекст (get_context_data).  
RedirectView	                Делает только редирект на другой URL.  
  
### Генерики для объектов (одного или списка):  
ListView	                    Показ списка объектов.  
DetailView	                    Показ детальной страницы одного объекта.  
  
### Генерики для работы с формами:  
CreateView	                    Создание объекта через форму.  
UpdateView	                    Обновление (редактирование) объекта через форму.  
DeleteView	                    Удаление объекта через форму (с подтверждением).  
FormView	                    Любая форма, не привязанная напрямую к модели.  
  
### Миксины (дополнительные поведения):   
SingleObjectMixin	            Работа с одним объектом (DetailView и т.п.).  
MultipleObjectMixin	            Работа со списком объектов (ListView и т.п.).  
FormMixin	                    Работа с формой в любых вьюшках.  
ModelFormMixin	                Работа с ModelForm (сохраняет объект модели).  
ProcessFormView	                Обработка форм внутри Create/UpdateView.  
ContextMixin	                Просто работа с контекстом (get_context_data).  
TemplateResponseMixin	        Рендер шаблона (render_to_response). 

### Как итог
TemplateView                    → отдает просто шаблон  

ListView                        → список объектов  

DetailView                      → детальная страница объекта  

CreateView                      → создать объект  

UpdateView                      → изменить объект  

DeleteView                      → удалить объект  

FormView                        → просто форма (например, "Напишите нам")  
