import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

# --- 1. データモデル定義 ---
class Employee(BaseModel):
    id: int
    name: str
    department: str
    email: str

# --- 2. ダミーデータ (事前に登録されているデータ) ---
MOCK_DATA: list[Employee] = [
    Employee(id=1, name="山田 太郎", department="開発部", email="taro@example.com"),
    Employee(id=2, name="鈴木 花子", department="営業部", email="hanako@example.com"),
    Employee(id=3, name="佐藤 次郎", department="人事部", email="jiro@example.com"),
]

# --- 3. アプリケーション設定 ---
app = FastAPI(title="Employee System API")

# フロントエンド(Vite等)からのアクセスを許可
origins = [
    "http://localhost:5173",  # 一般的なViteのポート
    "http://localhost:3000",  # 一般的なReactのポート
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

# --- 4. 認証ロジック ---
def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
    """Basic認証を行い、ユーザー名を返す。失敗時は401エラー。"""
    # ユーザー名: admin, パスワード: password で固定
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "password")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- 5. APIエンドポイント ---
@app.get("/api/employees", response_model=list[Employee])
def get_employees(username: Annotated[str, Depends(get_current_username)]) -> list[Employee]:
    """
    社員一覧を取得する。Basic認証が必要。
    Args:
        username: Basic認証を通過したユーザー名 (Dependency Injection)
    Returns:
        list[Employee]: 社員データのリスト
    """
    return MOCK_DATA

# 起動コマンドメモ: uvicorn main:app --reload