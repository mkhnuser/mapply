docker run --name mapply_postgresql \
    -e POSTGRES_USER=mapply \
    -e POSTGRES_PASSWORD=mapply \
    -e POSTGRES_DB=mapply \
    -p 5678:5432 -v /data/mapply:/var/lib/postgresql/data -d postgres
