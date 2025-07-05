# TopShopE 项目设置指南

## 🚀 快速开始

### 1. 环境准备

确保您的系统已安装：
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### 2. 克隆项目

```bash
git clone <repository-url>
cd topshope
```

### 3. 设置虚拟环境

```bash
# 方法1: 使用自动脚本
./activate_env.sh

# 方法2: 手动设置
python3 -m venv topshope_env
source topshope_env/bin/activate
pip install -r requirements.txt
```

### 4. 启动服务

```bash
# 方法1: 开发环境（推荐）
./dev_start.sh

# 方法2: 生产环境
./start.sh

# 方法3: 手动启动
docker-compose up -d postgres redis
cd backend && uvicorn main:app --reload
cd frontend && npm install && npm start
```

## 🔧 代码质量检查

### 语法检查
```bash
python check_code.py
```

### 运行测试
```bash
python test_mvp.py
```

## 📁 项目结构

```
topshope/
├── 📁 backend/                    # FastAPI后端
│   ├── 📁 app/
│   │   ├── 📁 api/               # API路由
│   │   ├── 📁 core/              # 核心配置
│   │   ├── 📁 models/            # 数据模型
│   │   ├── 📁 schemas/           # 数据验证
│   │   ├── 📁 services/          # 业务逻辑
│   │   └── 📁 utils/             # 工具函数
│   ├── main.py                   # 应用入口
│   └── requirements.txt          # Python依赖
├── 📁 frontend/                   # React前端
│   ├── 📁 src/
│   │   ├── 📁 components/        # React组件
│   │   ├── 📁 pages/             # 页面组件
│   │   ├── 📁 services/          # API服务
│   │   ├── 📁 types/             # TypeScript类型
│   │   └── 📁 utils/             # 工具函数
│   └── package.json              # Node.js依赖
├── 📁 topshope_env/              # Python虚拟环境
├── docker-compose.yml            # 容器编排
├── requirements.txt              # 根目录依赖
├── start.sh                      # 生产启动脚本
├── dev_start.sh                  # 开发启动脚本
├── activate_env.sh               # 环境激活脚本
├── check_code.py                 # 代码检查脚本
└── test_mvp.py                   # 功能测试脚本
```

## 🐍 虚拟环境管理

### 激活环境
```bash
source topshope_env/bin/activate
```

### 退出环境
```bash
deactivate
```

### 安装依赖
```bash
pip install -r requirements.txt
```

### 更新依赖
```bash
pip install --upgrade -r requirements.txt
```

## 🗄️ 数据库管理

### 启动数据库
```bash
docker-compose up -d postgres redis
```

### 创建表
```bash
cd backend
python -c "from app.core.database import create_tables; create_tables()"
```

### 数据库连接信息
- **主机**: localhost
- **端口**: 5432
- **数据库**: topshope
- **用户名**: topshope
- **密码**: topshope123

## 🔧 API开发

### 启动后端服务
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要端点
- `GET /api/v1/shops` - 获取商店列表
- `POST /api/v1/shops` - 创建商店
- `POST /api/v1/shops/{id}/verify-shopify` - 验证Shopify
- `POST /api/v1/shops/{id}/classify-fashion` - 分类女装
- `GET /api/v1/shops/rankings/{region}` - 获取排名

## 🌐 前端开发

### 启动前端服务
```bash
cd frontend
npm install
npm start
```

### 访问地址
- 开发服务器: http://localhost:3000
- 生产构建: `npm run build`

## 🐳 Docker部署

### 构建镜像
```bash
docker-compose build
```

### 启动所有服务
```bash
docker-compose up -d
```

### 查看日志
```bash
docker-compose logs -f
```

### 停止服务
```bash
docker-compose down
```

## 🧪 测试

### 功能测试
```bash
python test_mvp.py
```

### 代码质量检查
```bash
python check_code.py
```

### 单元测试（计划中）
```bash
pytest backend/tests/
```

## 🔍 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 检查端口占用
   lsof -i :8000
   lsof -i :3000
   ```

2. **数据库连接失败**
   ```bash
   # 重启数据库
   docker-compose restart postgres
   ```

3. **依赖安装失败**
   ```bash
   # 清理缓存
   pip cache purge
   npm cache clean --force
   ```

4. **虚拟环境问题**
   ```bash
   # 重新创建环境
   rm -rf topshope_env
   python3 -m venv topshope_env
   source topshope_env/bin/activate
   pip install -r requirements.txt
   ```

### 日志查看

```bash
# 后端日志
docker-compose logs backend

# 前端日志
docker-compose logs frontend

# 数据库日志
docker-compose logs postgres
```

## 📊 监控和性能

### 健康检查
```bash
curl http://localhost:8000/health
```

### 性能监控（计划中）
- Prometheus + Grafana
- APM工具集成
- 日志聚合

## 🔐 安全配置

### 环境变量
复制 `env.example` 到 `.env` 并修改配置：
```bash
cp env.example .env
```

### 生产环境
- 修改默认密码
- 配置SSL证书
- 设置防火墙规则
- 启用日志审计

## 📈 扩展计划

### 第二阶段
- [ ] 机器学习模型训练
- [ ] 实时数据更新
- [ ] 用户权限系统
- [ ] 高级分析功能

### 第三阶段
- [ ] 移动端适配
- [ ] 性能优化
- [ ] 监控告警
- [ ] 国际化支持

## 📞 支持

如有问题，请：
1. 查看本文档
2. 检查日志文件
3. 运行测试脚本
4. 提交Issue

---

**TopShopE** - 让女装电商数据更透明 🛍️ 