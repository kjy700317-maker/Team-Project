import sqlite3

# 1. 데이터베이스 연결 (파일이 없으면 자동으로 생성됩니다)
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

# 2. 테이블 생성 (이미 존재하면 만들지 않음)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT
)
""")

# 3. 데이터 추가 (INSERT)
cursor.execute("INSERT INTO users (name, email) VALUES ('홍길동', 'gildong@example.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('김철수', 'chulsoo@example.com')")

# 변경사항 저장 (Commit)
conn.commit()

# 4. 데이터 조회 (SELECT)
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

print("--- 저장된 사용자 목록 ---")
for row in rows:
    print(row)

# 5. 연결 종료
conn.close()