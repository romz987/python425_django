# POSTGRES  

## DEPLOY IN DOKCER  

1. Скачать последнюю версию postgres:      

        docker pull postgres  

2. Создать директорию на сервере для монтирования файлов БД:    

        mkdir educational_db/  

3. Установить на нее права 700:    

        chmod -R 700 educational_db/  

4. Развернуть postgres:     

        docker run --name educational_db \  
            -e POSTGRES_PASSWORD='a123123bcc!' \  
            -d \  
            -p 5434:5434 \  
            -v /root/educational_db:/var/lib/postgresql/data postgres  


!!! Мы разворачиваем этот контейнер как ВТОРОЙ контейнер с postgresel,     
    Поэтому меняем стандартный порт 5432 на порт 5434.  
    Для того, чтобы по этому порту работало удаленное подключение,  
    в директории educational_db/ найти файл postgresql.conf,  
    раскомментировать "port" и установить значение в 5434  


5. Подключится к DB с помощью PSQL:      

        psql -h 194.190.152.45 -p 5434 -U postgres    


6. Просмотр списка существующих баз данных:   

        \l


7. Создать базу данных:  

        CREATE DATABASE educational_1;


8. Под  ключится к DB educational_1 с помощью PSQL:  

        psql -h 194.190.152.45 -p 5434 -U postgres -d educational_1
