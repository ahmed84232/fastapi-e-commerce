docker run -dit ^
           --rm ^
           -e POSTGRES_USER=postgres ^
           -e POSTGRES_PASSWORD=postgres ^
           -e PGDATA=/var/lib/postgresql/data/pgdata ^
           -p 5432:5432 ^
           -v postgres:/var/lib/postgresql/data ^
           --name PostgreSQL ^
           postgres