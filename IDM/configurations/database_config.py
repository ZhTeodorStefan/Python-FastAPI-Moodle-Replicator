from peewee import PostgresqlDatabase
from IDM.private_keys.keys import DATABASE_CONNECTION_STRING, REDIS_DB_PASSWORD_STRING

import redis

database = PostgresqlDatabase(None)
database.init(DATABASE_CONNECTION_STRING)

redis_client = redis.Redis(
    host='redis-13740.c135.eu-central-1-1.ec2.redns.redis-cloud.com',
    port=13740,
    decode_responses=True,
    username="default",
    password=REDIS_DB_PASSWORD_STRING,
)
