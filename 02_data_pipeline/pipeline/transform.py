from loguru import logger

def transformer(pandas_df):
    """
    MySQL에서 추출한 dataframe을 가공하는 함수
    """
    current_year = 2025

    try:
        logger.info(f"TRANSFORM 단계 시작! : MYSQL 데이터 변환")
        # 도시 이름 컬럼 생성
        pandas_df["city"] = pandas_df["residence"].str.split().str[0]

        # 출생년도 컬럼 생성
        pandas_df['birthdate'] = pandas_df['birthdate'].astype(str)
        pandas_df["birthyear"] = pandas_df["birthdate"].str.slice(0, 4)

        # 혈액형 컬럼 생성
        pandas_df["blood"] = pandas_df["blood_group"].str.slice(0, -1)

        # 나이 컬럼 생성
        pandas_df["age"] = current_year - pandas_df["birthyear"].astype(int)

        # 나이가 0 이하인 데이터 제거
        pandas_df = pandas_df[pandas_df["age"] > 0].copy()

        # 나이대 컬럼 생성
        pandas_df["age_category"] = pandas_df["age"].apply(categorize_age)
        
        # 컬럼 순서 세팅
        df = pandas_df[["name", 'job', "sex", "city", "birthyear", "age", "blood", "age_category"]]
        
        logger.success(f"TRANSFORM 작업 완료 : {df.shape} 형상의 데이터 변환")
        return df

    except Exception as e:
        logger.error(f"TRANSFORM 단계 오류 발생! : {e}")
        
        return False


def categorize_age(age):
    if age >= 100:
        return "90대 이상"
    else:
        return str(age // 10 * 10) + "대"