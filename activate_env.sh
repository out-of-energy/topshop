#!/bin/bash

echo "🐍 激活 TopShopE 虚拟环境..."

# 检查虚拟环境是否存在
if [ ! -d "topshope_env" ]; then
    echo "❌ 虚拟环境不存在，正在创建..."
    python3 -m venv topshope_env
fi

# 激活虚拟环境
source topshope_env/bin/activate

echo "✅ 虚拟环境已激活: $(which python)"
echo "📦 Python版本: $(python --version)"
echo "📦 Pip版本: $(pip --version)"

# 安装依赖
echo "📦 安装项目依赖..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎉 环境设置完成！"
echo ""
echo "💡 使用提示："
echo "   - 激活环境: source topshope_env/bin/activate"
echo "   - 退出环境: deactivate"
echo "   - 运行后端: cd backend && uvicorn main:app --reload"
echo "   - 运行测试: python test_mvp.py" 