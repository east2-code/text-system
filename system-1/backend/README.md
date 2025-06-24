# 授权管理系统后端（Flask API）

本目录为后端API服务，适用于前后端分离（Vue前端，Flask RESTful后端）场景。  
主要功能包括用户登录、授权管理、软件管理等，所有数据接口均返回JSON，前端通过HTTP请求获取和操作数据。

---

## 目录结构说明

- `server.py`            —— Flask主程序，只保留API接口，所有返回均为JSON
- `config.py`            —— 配置项（如数据库名、密钥等，推荐自行新建）
- `requirements.txt`     —— Python依赖包列表
- `database_setup.sql`   —— 数据库结构初始化脚本
- `fernet.key`           —— 对称加密用密钥文件
- `README.md`            —— 本文件

---

## 快速启动

### 1. 安装依赖

建议使用虚拟环境：

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 初始化数据库

如首次部署，`server.py` 会自动检测并创建数据库和数据表。也可以手动运行 `database_setup.sql`：

```bash
sqlite3 license.db < database_setup.sql
```

### 3. 启动服务

```bash
python server.py
```

默认监听本地5000端口，可通过 http://localhost:5000 访问API。

---

## 主要接口示例

- `POST   /api/login`                —— 登录接口
- `GET    /api/all-licenses`         —— 获取所有授权
- `POST   /api/licenses`             —— 新增授权
- `DELETE /api/licenses/<id>`        —— 删除授权
- `GET    /api/license-detail/<id>`  —— 获取授权详情
- `GET    /api/software`             —— 查询软件
- `POST   /api/software`             —— 新增软件
- `DELETE /api/software/<id>`        —— 删除软件
- `GET    /api/stats`                —— 获取授权统计

接口参数和返回结果请参考 `server.py` 代码内注释或配合前端文档。

---

## 配置说明

- `DATABASE`        —— 数据库存储文件名（默认 license.db）
- `FERNET_KEY_PATH` —— 对称加密密钥，可自行生成或由程序首次启动时自动生成

如需单独管理密钥和配置，建议使用 `config.py` 单独维护。

---

## 依赖包

基本依赖如下，详见 requirements.txt：

- Flask
- Flask-Cors
- cryptography
- sqlite3（Python自带）

---

## 前端对接

- 推荐使用 Vue3 + axios 调用后端API
- 支持跨域（CORS），本地开发和生产环境均可通过HTTP请求访问

---

## 其它

- 本项目仅为示例/教学用途，实际部署请完善用户认证、权限管理和安全细节
- 日志、运维、热部署等可根据生产需求扩展

---