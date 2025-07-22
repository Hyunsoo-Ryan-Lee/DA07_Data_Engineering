from loguru import logger

def loader(pandas_df, db_conn, table_name):
    """
    가공된 dataframe을 PostgreSQl 데이터베이스에 저장하는 함수
    """
    try:
        logger.info(f"LOAD 단계 시작! : Postgres 데이터베이스의 {table_name} 테이블로 저장")
        
        pandas_df.to_sql(
            name = table_name,
            con = db_conn,
            if_exists='replace',
            index=False
        )
        
        logger.success(f"LOAD 작업 완료 : {pandas_df.shape} 형상의 데이터 저장 완료")
        return True

    except Exception as e:
        logger.error(f"LOAD 단계 오류 발생! : {e}")
        
        return False