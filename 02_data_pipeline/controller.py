from settings import DB_SETTINGS
from db.connector import DBconnector
from pipeline.source import source_to_db
from pipeline.extract import extractor
from pipeline.transform import transformer
from pipeline.load import loader
from loguru import logger

def run_pipeline(batch_date):
    
    logger.info("="*50)
    logger.info(f"{batch_date} 일자 데이터에 대한 파이프라인 시작")
    logger.info("="*50)

    ## 1. 관련 변수 선언 & 데이터베이스 연결
    mysql_conn = DBconnector(**DB_SETTINGS['mysql_params']).sql_conn
    postgres_conn = DBconnector(**DB_SETTINGS['postgres_params']).sql_conn
    source_path = 'source_data'
    file_name = 'user_data'

    ## 2. SOURCE
    source_res = source_to_db(
        db_conn=mysql_conn,
        source_path=source_path,
        file_name=file_name,
        batch_date=batch_date
        )
    if not source_res:
        return False

    ## 3. EXTRACT
    table_name = 'user_data'
    
    df = extractor(
        db_conn=mysql_conn,
        table_name=table_name
    )

    ## 4. TRANSFORM
    tdf = transformer(df)

    ## 5. LOAD
    load_res = loader(
        pandas_df = tdf,
        db_conn = postgres_conn,
        table_name = 'user_data_summary'
    )
    if not load_res:
        return False
    
    logger.success("="*50)
    logger.success(f"파이프라인 작동 완료!")
    logger.success("="*50)