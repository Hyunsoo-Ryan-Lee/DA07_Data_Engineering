from controller import run_pipeline
from loguru import logger

logger.add(
        "log_file/pipeline.log", # 로그 파일 저장 경로
        level="DEBUG", # DEBUG 이상 수준의 로그를 모두 기록
    )

def main(batch_date):
    
    run_pipeline(batch_date)
    

if __name__ == '__main__':
    batch_date = '2025-03-08'
    main(batch_date)