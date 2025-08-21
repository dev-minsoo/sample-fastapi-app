import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost:27017")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
DATABASE_NAME = os.getenv("MONGODB_DATABASE", "sample_db")

# MongoDB URI 생성 (특수문자 URL 인코딩)
if MONGODB_USERNAME and MONGODB_PASSWORD:
    username = quote_plus(MONGODB_USERNAME)
    password = quote_plus(MONGODB_PASSWORD)
    MONGODB_URI = f"mongodb://{username}:{password}@{MONGODB_HOST}/{DATABASE_NAME}"
else:
    MONGODB_URI = f"mongodb://{MONGODB_HOST}/{DATABASE_NAME}"

class Database:
    client: MongoClient = None
    
database = Database()

async def connect_to_mongo():
    try:
        database.client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # 연결 테스트
        database.client.admin.command('ping')
        print(f"✅ MongoDB 연결 성공: {MONGODB_URI}")
    except Exception as e:
        print(f"⚠️ MongoDB 연결 실패: {e}")
        print("로컬 개발 모드로 실행됩니다 (MongoDB 없음)")
        database.client = None

async def close_mongo_connection():
    if database.client:
        database.client.close()

def get_database():
    if database.client:
        return database.client[DATABASE_NAME]
    return None