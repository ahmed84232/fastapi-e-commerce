docker run -dit ^
           -e POSTGRES_USER=postgres ^
           -e POSTGRES_PASSWORD=postgres ^
           -e PGDATA=/var/lib/postgresql/data/pgdata ^
           -p 5432:5432 ^
           -v postgres:/var/lib/postgresql/data ^
           --network private ^
           --hostname postgres ^
           --restart always ^
           --name PostgreSQL ^
           postgres

  docker run -dit ^
           -e POSTGRES_USER=postgres ^
           -e POSTGRES_PASSWORD=postgres ^
           -e PGDATA=/var/lib/postgresql/data/pgdata ^
           -p 5432:5432 ^
           -v postgres:/var/lib/postgresql/data ^
           --hostname postgres ^
           --restart always ^
           --name PostgreSQL ^
           postgres