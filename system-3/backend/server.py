from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from pathlib import Path
from cryptography.fernet import Fernet

DATABASE = "license.db"
FERNET_KEY_PATH = "fernet.key"

def load_fernet_key():
    if not os.path.exists(FERNET_KEY_PATH):
        key = Fernet.generate_key()
        with open(FERNET_KEY_PATH, "wb") as f:
            f.write(key)
    else:
        with open(FERNET_KEY_PATH, "rb") as f:
            key = f.read()
    return key

fernet = Fernet(load_fernet_key())

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row):
    return {k: row[k] for k in row.keys()}

def _get_status(lic):
    import datetime
    now = datetime.datetime.now()
    expires_at = datetime.datetime.strptime(lic['expires_at'], "%Y-%m-%d %H:%M:%S")
    if not lic['is_active']:
        return "已停用"
    if now > expires_at:
        return "已过期"
    elif (expires_at - now).days < 30:
        return "即将到期"
    else:
        return "激活"

app = Flask(__name__)
CORS(app)

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == "admin" and password == "admin":
        return jsonify({"code": 0, "token": "test-token"})
    else:
        return jsonify({"code": 1, "error": "用户名或密码错误"}), 401

@app.route("/api/all-licenses", methods=["GET"])
def api_all_licenses():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM licenses WHERE deleted=0")
    rows = cur.fetchall()
    licenses = []
    for row in rows:
        lic = row_to_dict(row)
        lic['status'] = _get_status(lic)
        licenses.append(lic)
    conn.close()
    return jsonify({"code": 0, "licenses": licenses})

@app.route("/api/licenses", methods=["POST"])
def api_add_license():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email", "")
    company = data.get("company", "")
    software = data.get("software_name")
    hardware_id = data.get("hardware_id")
    expiry_days = int(data.get("expiry_days", 365))
    license_key = fernet.encrypt(hardware_id.encode()).decode()
    import datetime
    now = datetime.datetime.now()
    expires_at = now + datetime.timedelta(days=expiry_days)
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO licenses (username, email, company, software, license_key, hardware_id, expires_at, is_active, deleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)",
        (username, email, company, software, license_key, hardware_id, expires_at.strftime("%Y-%m-%d %H:%M:%S"), 1),
    )
    conn.commit()
    conn.close()
    return jsonify({"code": 0, "license_key": license_key})

@app.route("/api/licenses/<int:license_id>", methods=["DELETE"])
def api_delete_license(license_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE licenses SET deleted=1 WHERE id = ?", (license_id,))
    conn.commit()
    conn.close()
    return jsonify({"code": 0, "message": "已删除"})

@app.route("/api/licenses/undo-delete", methods=["POST"])
def api_undo_delete_licenses():
    data = request.get_json()
    ids = data.get("ids", [])
    if not ids:
        return jsonify({"code": 1, "error": "参数缺失"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"UPDATE licenses SET deleted=0 WHERE id IN ({','.join(['?']*len(ids))})", ids)
    conn.commit()
    conn.close()
    return jsonify({"code": 0, "message": f"已恢复{len(ids)}条数据"})

@app.route("/api/license-detail/<int:license_id>", methods=["GET"])
def api_license_detail(license_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM licenses WHERE id = ? AND deleted=0", (license_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"code": 1, "error": "未找到"}), 404
    license_data = row_to_dict(row)
    license_data['status'] = _get_status(license_data)
    conn.close()
    return jsonify(license_data)

@app.route("/api/licenses/<int:license_id>/toggle", methods=["PATCH"])
def api_toggle_license(license_id):
    data = request.get_json()
    is_active = int(data.get("is_active", 0))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE licenses SET is_active=? WHERE id=?", (is_active, license_id))
    conn.commit()
    conn.close()
    return jsonify({"code": 0, "message": "状态已更新"})

@app.route("/api/licenses/<int:license_id>/renew", methods=["PATCH"])
def api_renew_license(license_id):
    data = request.get_json()
    add_days = int(data.get("add_days", 30))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT expires_at FROM licenses WHERE id=?", (license_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"code": 1, "error": "未找到"}), 404
    import datetime
    expires_at = datetime.datetime.strptime(row['expires_at'], "%Y-%m-%d %H:%M:%S")
    new_expires = expires_at + datetime.timedelta(days=add_days)
    cur.execute("UPDATE licenses SET expires_at=? WHERE id=?", (new_expires.strftime("%Y-%m-%d %H:%M:%S"), license_id))
    conn.commit()
    conn.close()
    return jsonify({"code": 0, "message": f"续期成功, 新到期时间: {new_expires.strftime('%Y-%m-%d %H:%M:%S')}"})

@app.route("/api/licenses/<int:license_id>", methods=["PATCH"])
def api_edit_license(license_id):
    data = request.get_json()
    email = data.get("email", "")
    company = data.get("company", "")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE licenses SET email=?, company=? WHERE id=?", (email, company, license_id))
    conn.commit()
    conn.close()
    return jsonify({"code": 0, "message": "修改成功"})

@app.route("/api/software", methods=["GET", "POST"])
def api_software():
    if request.method == "GET":
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM software")
        rows = cur.fetchall()
        software = [row_to_dict(row) for row in rows]
        conn.close()
        return jsonify({"code": 0, "software": software})
    else:
        data = request.get_json()
        name = data.get("name")
        version = data.get("version")
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO software (name, version) VALUES (?, ?)", (name, version))
        conn.commit()
        conn.close()
        return jsonify({"code": 0, "message": "新增成功"})

@app.route("/api/software/<int:software_id>", methods=["DELETE"])
def api_delete_software(software_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM software WHERE id = ?", (software_id,))
    conn.commit()
    conn.close()
    return jsonify({"code": 0, "message": "删除成功"})

@app.route("/api/stats", methods=["GET"])
def api_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM licenses WHERE deleted=0")
    total = cur.fetchone()[0]
    import datetime
    now = datetime.datetime.now()
    cur.execute("SELECT COUNT(*) FROM licenses WHERE expires_at <= ? AND deleted=0", (now.strftime("%Y-%m-%d %H:%M:%S"),))
    expired = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM licenses WHERE expires_at > ? AND expires_at <= ? AND deleted=0", (
        now.strftime("%Y-%m-%d %H:%M:%S"),
        (now + datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    ))
    expiring = cur.fetchone()[0]
    conn.close()
    return jsonify({"code": 0, "data": {"total": total, "expired": expired, "expiring": expiring}})

@app.route("/api/validate", methods=["POST"])
def api_validate():
    data = request.get_json()
    hardware_id = data.get("hardware_id")
    license_key = data.get("license_key")
    if not hardware_id or not license_key:
        return jsonify({"valid": False, "error": "参数缺失"}), 400
    try:
        decrypted = fernet.decrypt(license_key.encode()).decode()
    except Exception:
        return jsonify({"valid": False, "error": "授权码无效"}), 400
    if decrypted != hardware_id:
        return jsonify({"valid": False, "error": "硬件ID与授权码不匹配"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM licenses WHERE license_key=? AND hardware_id=? AND deleted=0", (license_key, hardware_id))
    row = cur.fetchone()
    if not row:
        return jsonify({"valid": False, "error": "授权不存在"}), 404
    license_info = row_to_dict(row)
    conn.close()
    import datetime
    now = datetime.datetime.now()
    expires_at = datetime.datetime.strptime(license_info['expires_at'], "%Y-%m-%d %H:%M:%S")
    if now > expires_at:
        return jsonify({"valid": False, "error": "授权已过期"}), 403
    if not license_info['is_active']:
        return jsonify({"valid": False, "error": "授权已停用"}), 403
    return jsonify({
        "valid": True,
        "username": license_info.get("username"),
        "software": license_info.get("software"),
        "expires_at": license_info.get("expires_at")
    })

if __name__ == "__main__":
    if not Path(DATABASE).exists():
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE software (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                version TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                company TEXT,
                software TEXT,
                license_key TEXT,
                hardware_id TEXT,
                expires_at TEXT,
                is_active INTEGER,
                deleted INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()
        print("已初始化数据库")
    else:
        # 自动升级表，兼容旧库
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        try:
            cur.execute("ALTER TABLE licenses ADD COLUMN deleted INTEGER DEFAULT 0")
            conn.commit()
        except Exception:
            pass
        conn.close()
    app.run(host="0.0.0.0", port=5000, debug=True)