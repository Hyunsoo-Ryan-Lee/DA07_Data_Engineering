# 데이터 파이프라인 프로젝트
![](https://velog.velcdn.com/images/newnew_daddy/post/4637f3ad-2f16-4134-859a-8cf7e94d1346/image.png)

## 개요
이 프로젝트는 데이터 원천(source)에서 데이터 웨어하우스(DW)를 거쳐 데이터 마트(DM)로 데이터를 이동시키는 ETL 파이프라인입니다.

## 데이터 흐름 (단순화)
```
파일 → MySQL → DataFrame → 변환 → PostgreSQL
```

## 프로젝트 구조
```
02_data_pipeline/
├── main.py               # 파라미터 설정 및 실행 (진입점)
├── controller.py         # 실제 파이프라인 실행 로직
├── settings.py           # 데이터베이스 설정
├── requirements.txt      # 필요한 패키지 목록
├── dashboard.py          # 시각화 대시보드
│
├── source_data/          # 원천 데이터 파일
│   └── user_data.parquet
│
├── db/
│   └── connector.py     # 데이터베이스 연결 클래스
│
└── pipeline/
    ├── source.py        # 파일 → MySQL 저장
    ├── extract.py       # MySQL → DataFrame 추출
    ├── transform.py     # 데이터 변환
    └── load.py          # DataFrame → PostgreSQL 저장
```