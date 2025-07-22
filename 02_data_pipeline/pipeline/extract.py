from loguru import logger
import pandas as pd

def extractor(db_conn, table_name):
    """
    MySQL 데이터베이스에서 데이터를 추출하여 dataframe으로 변환하는 함수
    """
    try:
        logger.info(f"EXTRACT 단계 시작! : MYSQL에서 {table_name} 데이터 추출")
        df = pd.read_sql_table(
            table_name = table_name,
            con = db_conn
        )
        logger.success(f"EXTRACT 작업 완료 : {df.shape} 형상의 데이터 추출")
        
        return df
    
    except Exception as e:
        logger.error(f"EXTRACT 단계 오류 발생! : {e}")
        
        return False