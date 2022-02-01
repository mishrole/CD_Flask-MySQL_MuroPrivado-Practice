To run this project:
---

1. Install dependencies
   ```
   pipenv install Flask PyMySQL Flask-Bcrypt
   ```
2. Change MySQL Configuration on bcrypt_app/config/mysqlconnection.py
   ```
   ...
   connection = pymysql.connect(
            host = '127.0.0.1',
            user = YOUR_USER,
            password = YOUR_PASSWORD,
            db = database,
            port = YOUR_PORT (DEFAULT 3306),
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True
        )
    ...
   ```
3. Run shell
   ```
   pipenv shell
   ```
4. Run project
    ```
    python server.py
    ```
5. [Go to BCrypt Core](http://127.0.0.1:8091/)