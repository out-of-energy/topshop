# TopShopE 项目结构

```
topshope/
├── 📁 backend/                    # 后端服务
│   ├── 📁 app/
│   │   ├── 📁 api/               # API路由
│   │   │   ├── 📁 endpoints/
│   │   │   │   └── shops.py      # 商店API端点
│   │   │   └── api.py            # API路由配置
│   │   ├── 📁 core/              # 核心配置
│   │   │   ├── config.py         # 应用配置
│   │   │   └── database.py       # 数据库连接
│   │   ├── 📁 models/            # 数据模型
│   │   │   └── shop.py           # 商店模型
│   │   ├── 📁 schemas/           # Pydantic schemas
│   │   │   └── shop.py           # 商店数据验证
│   │   ├── 📁 services/          # 业务逻辑服务
│   │   │   ├── shopify_detector.py    # Shopify检测
│   │   │   ├── fashion_classifier.py  # 女装分类
│   │   │   └── domain_discovery.py    # 域名发现
│   │   └── 📁 utils/             # 工具函数
│   ├── main.py                   # FastAPI应用入口
│   ├── requirements.txt          # Python依赖
│   └── Dockerfile                # 后端Docker配置
│
├── 📁 frontend/                   # 前端应用
│   ├── 📁 public/                # 静态资源
│   │   └── index.html            # HTML模板
│   ├── 📁 src/
│   │   ├── 📁 components/        # React组件
│   │   │   └── ShopCard.tsx      # 商店卡片组件
│   │   ├── 📁 pages/             # 页面组件
│   │   │   └── Dashboard.tsx     # 主仪表板
│   │   ├── 📁 services/          # API服务
│   │   │   └── api.ts            # API客户端
│   │   ├── 📁 types/             # TypeScript类型
│   │   │   └── shop.ts           # 商店类型定义
│   │   ├── 📁 utils/             # 工具函数
│   │   ├── App.tsx               # 主应用组件
│   │   └── index.tsx             # React入口
│   ├── package.json              # Node.js依赖
│   └── Dockerfile                # 前端Docker配置
│
├── 📄 docker-compose.yml         # 容器编排配置
├── 📄 requirements.txt           # 根目录依赖
├── 📄 README.md                  # 项目说明
├── 📄 PROJECT_STRUCTURE.md       # 项目结构说明
├── 📄 start.sh                   # 启动脚本
└── 📄 test_mvp.py                # MVP测试脚本
```

## 🏗️ 架构说明

### 后端架构 (FastAPI)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Layer     │    │  Service Layer  │    │  Data Layer     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • FastAPI       │    │ • Shopify       │    │ • PostgreSQL    │
│ • Pydantic      │    │   Detector      │    │ • SQLAlchemy    │
│ • CORS          │    │ • Fashion       │    │ • Redis         │
│ • Validation    │    │   Classifier    │    │ • Celery        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP/REST     │    │  Business Logic │    │  Data Storage   │
│   Endpoints     │    │  & Algorithms   │    │  & Caching      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 前端架构 (React)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  State Layer    │    │  API Layer      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Material-UI   │    │ • React Hooks   │    │ • Axios         │
│ • Components    │    │ • Context       │    │ • TypeScript    │
│ • Pages         │    │ • Local State   │    │ • API Client    │
│ • Routing       │    │ • Props         │    │ • Error Handling│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Interface│    │  State Management│    │  Backend API    │
│   & UX          │    │  & Logic        │    │  Communication  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 数据流

```
1. 域名发现
   └── DomainDiscovery Service
       └── 返回潜在域名列表

2. Shopify验证
   └── ShopifyDetector Service
       └── 技术指纹检测
       └── 更新数据库

3. 女装分类
   └── FashionClassifier Service
       └── 内容分析
       └── 关键词匹配
       └── 更新数据库

4. 排名计算
   └── 综合评分算法
       └── 流量指标
       └── 社交媒体热度
       └── SEO排名

5. 数据展示
   └── React Frontend
       └── API调用
       └── 数据渲染
       └── 用户交互
```

## 🚀 部署架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Infrastructure│
│   (React)       │    │   (FastAPI)     │    │                 │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Port 3000     │    │ • Port 8000     │    │ • PostgreSQL    │
│ • Nginx         │    │ • Uvicorn       │    │ • Redis         │
│ • Static Files  │    │ • Celery        │    │ • Docker        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │   Docker Compose│
                    │   Orchestration │
                    └─────────────────┘
```

## 📊 核心功能模块

### 1. Shopify验证中心
- **文件**: `backend/app/services/shopify_detector.py`
- **功能**: 检测网站是否使用Shopify框架
- **方法**: 技术指纹识别、API端点检测

### 2. 女装分类引擎
- **文件**: `backend/app/services/fashion_classifier.py`
- **功能**: 判断网站是否销售女装
- **方法**: 关键词分析、内容分类

### 3. 域名发现服务
- **文件**: `backend/app/services/domain_discovery.py`
- **功能**: 发现潜在的Shopify商店
- **方法**: 搜索引擎、目录爬取

### 4. 数据管理
- **文件**: `backend/app/models/shop.py`
- **功能**: 商店数据模型和数据库操作
- **方法**: SQLAlchemy ORM

### 5. API接口
- **文件**: `backend/app/api/endpoints/shops.py`
- **功能**: RESTful API端点
- **方法**: FastAPI路由

### 6. 前端展示
- **文件**: `frontend/src/pages/Dashboard.tsx`
- **功能**: 用户界面和数据展示
- **方法**: React + Material-UI

## 🔧 技术栈详情

### 后端技术栈
- **Web框架**: FastAPI (高性能异步框架)
- **数据库**: PostgreSQL (关系型数据库)
- **ORM**: SQLAlchemy (数据库操作)
- **缓存**: Redis (数据缓存)
- **任务队列**: Celery (异步任务)
- **爬虫**: Selenium + Playwright (网页自动化)
- **AI/ML**: scikit-learn + transformers (机器学习)
- **验证**: Pydantic (数据验证)

### 前端技术栈
- **框架**: React 18 (用户界面)
- **语言**: TypeScript (类型安全)
- **UI库**: Material-UI (组件库)
- **HTTP**: Axios (API调用)
- **图表**: Recharts (数据可视化)
- **构建**: Create React App (开发工具)

### 基础设施
- **容器化**: Docker + Docker Compose
- **数据库**: PostgreSQL 15
- **缓存**: Redis 7
- **反向代理**: Nginx (生产环境)
- **监控**: Prometheus + Grafana (计划中)

## 🎯 MVP功能清单

### ✅ 已完成
- [x] 基础项目架构搭建
- [x] 数据库模型设计
- [x] API接口开发
- [x] Shopify检测算法
- [x] 女装分类算法
- [x] 前端基础界面
- [x] Docker容器化
- [x] 自动化测试脚本

### 🚧 进行中
- [ ] 数据爬取优化
- [ ] 机器学习模型训练
- [ ] 实时更新机制
- [ ] 用户权限系统

### 📋 计划中
- [ ] 高级分析功能
- [ ] 移动端适配
- [ ] 性能优化
- [ ] 监控告警系统 