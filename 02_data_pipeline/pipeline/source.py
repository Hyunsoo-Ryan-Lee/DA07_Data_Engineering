from loguru import logger
import pandas as pd

def source_to_db(db_conn, source_path, file_name, batch_date):
    """
    source data에 저장된 parquet 파일을 추출하여 MySQL에 저장하는 함수
    """
    try:
        logger.info(f"SOURCE 단계 시작! : {file_name} 파일 데이터를 MYSQL에 저장")
        
        df = pd.read_parquet(f'{source_path}/{file_name}.parquet')

        batch_df = df[df['credate'] == batch_date]

        batch_df.to_sql(
            name=file_name,
            con=db_conn, 
            if_exists='append',
            index=False
        )
        
        logger.success(f"SOURCE 작업 완료 : {batch_df.shape} 형상의 데이터 MYSQL에 저장")
        
        return True
        
    except Exception as e:
        logger.error(f"SOURCE 단계 오류 발생! : {e}")
        return False
    
    