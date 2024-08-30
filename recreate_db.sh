export POSTGRES_PASSWORD=secret
psql --host 127.0.0.1 -p 5439 -U app_fast_api_2  -d postgres -c "drop database app_fast_api_2"
psql --host 127.0.0.1 -p 5439 -U app_fast_api_2  -d postgres -c "create database app_fast_api_2"

