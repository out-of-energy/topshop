#!/bin/bash

echo "🚀 启动 TopShopE 开发环境..."

# 检查虚拟环境
if [ ! -d "topshope_env" ]; then
    echo "❌ 虚拟环境不存在，正在创建..."
    python3 -m venv topshope_env
fi

# 激活虚拟环境
echo "🐍 激活虚拟环境..."
source topshope_env/bin/activate

# 安装/更新依赖
echo "📦 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

# 启动数据库和Redis
echo "🗄️ 启动数据库和缓存..."
docker-compose up -d postgres redis

# 等待数据库启动
echo "⏳ 等待数据库启动..."
sleep 10

# 创建数据库表
echo "📊 创建数据库表..."
cd backend
python -c "
from app.core.database import create_tables
create_tables()
print('✅ 数据库表创建完成')
"

# 启动后端服务
echo "🔧 启动后端服务..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 5

# 启动前端服务
echo "🌐 启动前端服务..."
cd ../frontend
npm install
npm start &
FRONTEND_PID=$!

echo "✅ 开发环境启动完成！"
echo ""
echo "🌐 前端: http://localhost:3000"
echo "🔧 后端: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo '🛑 停止服务...'; kill $BACKEND_PID $FRONTEND_PID; docker-compose down; exit" INT
wait 