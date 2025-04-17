from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime

app = FastAPI()

# Модель данных пользователя
class User(BaseModel):
    username: str
    email: str
    password: str

# Модель для ответа с ID и датой создания
class UserResponse(User):
    id: int
    created_at: str

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  email TEXT UNIQUE,
                  password TEXT,
                  created_at TEXT)''')
    conn.commit()
    conn.close()

# Вызываем инициализацию при запуске
init_db()

# Создание пользователя (Create)
@app.post("/users/", response_model=UserResponse)
async def create_user(user: User):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    try:
        created_at = datetime.now().isoformat()
        c.execute(
            "INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)",
            (user.username, user.email, user.password, created_at)
        )
        conn.commit()
        
        user_id = c.lastrowid
        return {**user.dict(), "id": user_id, "created_at": created_at}
    
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        conn.close()

# Получение всех пользователей (Read)
@app.get("/users/", response_model=List[UserResponse])
async def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT id, username, email, password, created_at FROM users")
    users = [{"id": row[0], "username": row[1], "email": row[2], 
              "password": row[3], "created_at": row[4]} for row in c.fetchall()]
    
    conn.close()
    return users

# Получение пользователя по ID (Read)
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT id, username, email, password, created_at FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    
    conn.close()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"id": user[0], "username": user[1], "email": user[2], 
            "password": user[3], "created_at": user[4]}

# Обновление пользователя (Update)
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if c.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        c.execute(
            "UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?",
            (user.username, user.email, user.password, user_id)
        )
        conn.commit()
        
        c.execute("SELECT created_at FROM users WHERE id = ?", (user_id,))
        created_at = c.fetchone()[0]
        
        conn.close()
        return {**user.dict(), "id": user_id, "created_at": created_at}
    
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")

# Удаление пользователя (Delete)
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if c.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return {"message": "User deleted successfully"}

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)