# mem-api-minio
simple API written on FastAPI with Minio as image storage.


installation

1. git clone https://github.com/nikolay-may/mem-api-minio.git

2. docker-compose up

3. logon http://172.17.0.4:9001 or http://127.0.0.1:9001 with login and password from docker-copmpose.yml

4. create it in the admin panel Access key and Secret key: User -> Access keys press "Create access key"

5. create it in the admin panel bucket name: Administration -> Buckets and press "Create bucket"

6. Create .env file.

7. Use url http://127.0.0.1:8000/docs for for review and testing API