import dotenv
import os

env_path = dotenv.find_dotenv()

dotenv.load_dotenv(
    dotenv_path=env_path,
    override=True
)

DB_SETTINGS = dict(
    mysql_params = dict(
        engine_name = os.getenv('MYSQL_ENGINE_NAME', ""),
        user = os.getenv('MYSQL_USER', ""),
        password = os.getenv('MYSQL_PASSWORD', ""),
        host = os.getenv('MYSQL_HOST', ""),
        port = os.getenv('MYSQL_PORT', ""),
        database = os.getenv('MYSQL_DATABASE', "")
    ),
    postgres_params = dict(
        engine_name = os.getenv('POSTGRES_ENGINE_NAME', ""),
        user = os.getenv('POSTGRES_USER', ""),
        password = os.getenv('POSTGRES_PASSWORD', ""),
        host = os.getenv('POSTGRES_HOST', ""),
        port = os.getenv('POSTGRES_PORT', ""),
        database = os.getenv('POSTGRES_DATABASE', "")
    )
)