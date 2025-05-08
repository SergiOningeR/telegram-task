from app.database import get_connection

def create_task(title, comment, phone, urgency, user_id, username, photo_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, comment, phone, urgency, status, creator_id, creator_name, photo_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (title, comment, phone, urgency, "новая", user_id, username, photo_id)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_user_tasks(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE creator_id = ?", (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task