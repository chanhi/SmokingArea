# app/main.py
from fastapi import FastAPI, Depends, HTTPException
import os
from sqlalchemy import create_engine, text
import pandas as pd
from contextlib import asynccontextmanager


DATABASE_URL = "postgresql://Team_ten:1234@db:5432/tabaco_retail"
CSV_PATH = "/app/data/address.csv"


# DB 연결은 다른 조원이 구현할 것이므로, 여기서는 더미 의존성을 사용
# 실제로는 여기에 DB 세션 생성 및 종료 로직이 들어갈 것입니다.
async def get_db():
    try:
        # DB 연결 로직 (예: asyncpg, SQLAlchemy 등)
        # yield db_session
        print("Database connection simulated.")
        yield {"message": "DB connection ready"}
    finally:
        print("Database connection closed simulated.")
        # db_session.close()


# -------------------------------
# ✅ address.csv → DB 로딩 함수
# -------------------------------
def initialize_address_table():
    try:
        print("🔍 address 테이블 상태 확인 중...")
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM address"))
            count = result.scalar()

            if count == 0:
                print("⚙️ address 테이블이 비어 있습니다. CSV 데이터를 삽입합니다...")
                df = pd.read_csv(CSV_PATH)
                ##비어있을 때 예외처리/ 비어 있는 문자열 값을 '비어있음'으로 채움
                df[['landlot_address', 'road_name_address']] = df[['landlot_address', 'road_name_address']].fillna("비어있음")
                # 좌표(x, y)가 비어 있으면 -1로 대체
                if 'x' in df.columns and 'y' in df.columns:
                    df['x'] = df['x'].apply(lambda v: v if pd.notna(v) and v != '' else -1)
                    df['y'] = df['y'].apply(lambda v: v if pd.notna(v) and v != '' else -1)
                ######### 좌표 변환 수행

                df.to_sql('address', con=engine, if_exists='append', index=False)
                print("✅ CSV 데이터가 성공적으로 삽입되었습니다.")
            else:
                print(f"✅ address 테이블에 {count}개의 레코드가 있습니다. 초기화 스킵.")
    except Exception as e:
        print(f"❌ 초기화 중 오류 발생: {e}")


# -------------------------------
# ✅ FastAPI 이벤트 훅 (앱 시작 시 실행)
# -------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 실행
    print("🔍 FastAPI 시작!")
    initialize_address_table()  # CSV 데이터 삽입 등
    yield
    # 앱 종료 시 실행
    print("🔒 FastAPI 종료!")

app = FastAPI(title="Tobacco Retailer Location API", lifespan=lifespan)






@app.get("/")
async def read_root():
    return {"message": "Welcome to Tobacco Retailer Location API!"}

@app.get("/check-location/{latitude}/{longitude}")
async def check_location_eligibility(
    latitude: float,
    longitude: float,
    db: dict = Depends(get_db) # DB 연결 의존성 예시
):
    # 이 부분에서 OSMnx/GeoPandas를 사용하여 입지 분석 로직 구현
    # 예시: 현재는 무조건 '입점 가능'으로 반환
    print(f"Checking location: Lat={latitude}, Lon={longitude}")
    print(f"DB connection status: {db['message']}")
    
    # 실제 로직:
    # 1. OSMnx로 도보 네트워크 로드
    # 2. 기존 업소 데이터를 DB에서 불러옴
    # 3. GeoPandas로 100m Isochrone 계산
    # 4. 해당 위치가 제한 구역에 속하는지 확인
    
    is_eligible = True # 실제 로직에 따라 변경
    
    if is_eligible:
        return {"status": "Access", "message": "해당 위치는 입점 가능합니다."}
    else:
        # 이 경우 제한 구역 표시를 위한 폴리곤 정보도 함께 반환 가능
        raise HTTPException(status_code=400, detail="해당 위치는 입점 제한 구역입니다.")

@app.get("/restricted-zones")
async def get_restricted_zones(db: dict = Depends(get_db)):
    # 이 부분에서 모든 제한 구역 폴리곤 데이터를 반환하는 로직 구현
    # 예시: 더미 데이터 반환
    return {
        "status": "success",
        "zones": [
            {"type": "Polygon", "coordinates": [...]}, # GeoJSON 형식
            # ... 실제 폴리곤 데이터
        ]
    }