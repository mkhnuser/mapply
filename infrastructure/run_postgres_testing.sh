docker run --name mapply_postgresql_testing \
    -e POSTGRES_USER=mapply_testing \
    -e POSTGRES_PASSWORD=mapply_testing \
    -e POSTGRES_DB=mapply_testing \
    -p 5679:5432 -v /data/mapply:/var/lib/postgresql/data -d postgres
