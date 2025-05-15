:: docker build . -t ahmedyassereg/fastapi-practic
docker run -dit ^
           -p 8000:8000 ^
           --network private ^
           --restart always ^
           --name FastapiPractice ^
           ahmedyassereg/fastapi-practice