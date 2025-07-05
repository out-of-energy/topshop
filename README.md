我需要做一个功能 你先别考虑实现， 先给出最可行的技术方案 这是我的具体需求：1. 核心目标

建立一个自动化系统，持续发现并展示全球三大区域（北美/欧洲/中东）女装类目下，使用Shopify框架搭建的独立站中，销量排名前10的网站。每日自动更新榜单。

2. 关键功能模块

| 功能模块 | 服务对象 | 实现效果 |
|---------|----------|---------|
| Shopify验证中心 | 系统自身 | 100%准确识别有效Shopify商店自动淘汰非Shopify或无效网站 |
| 女装分类引擎 | 商家/运营人员 | 精准筛选女装类目商店自动过滤其他品类站点 |
| 地区销量榜单 | 市场分析师 | 实时获取三大区域Top10榜单支持北美/欧洲/中东切换 |
| 数据更新中枢 | 系统管理员 | 每日UTC时间自动全量更新异常站点自动标记 |
| 集中展示平台 | 所有用户 | 动态iframe列表实时预览地区导航+状态指示 |

3. 用户角色与权限

访客

可查看：

✓ 实时榜单列表

✓ 网站预览iframe

✗ 无操作权限

分析师

可查看：

✓ 完整数据分析

✓ 历史排名趋势

✓ 区域对比分析

管理员

可操作：

✓ 手动触发更新

✓ 异常站点处理

✓ API密钥管理

4. 预期输出效果

数据准确性

Shopify商店验证准确率 ≥99.9%
女装分类准确率 ≥98%
地区定位准确率 ≥99%
时效性

每日UTC 00:00自动更新
更新完成时间 ≤2小时
异常检测响应时间 ≤5分钟    ｜｜｜｜｜。5. 关键成功指标

每日成功获取 ≥30个有效女装Shopify站点
区域榜单更新成功率 ≥95%
系统年可用性 ≥99.9%.

## 快速开始

### 使用 Docker Compose（推荐）

1. **启动所有服务**
   ```bash
   docker-compose up -d
   ```
   这将自动：
   - 启动 PostgreSQL 数据库
   - 启动 Redis 缓存
   - 初始化数据库（如果为空）
   - 启动后端 API 服务
   - 启动前端应用
   - 启动 Celery 工作队列

2. **访问应用**
   - 前端: http://localhost:3000
   - 后端 API: http://localhost:8000
   - API 文档: http://localhost:8000/docs

### 数据库管理

#### 自动初始化
Docker Compose 会自动在首次启动时初始化数据库，包括：
- 创建所有必要的表
- 添加示例数据（欧洲、中东、北美的女装商店）

#### 手动重置数据库（开发环境）
如果需要完全重置数据库：
```bash
# 进入后端容器
docker-compose exec backend python reset_db.py

# 或者直接运行
docker-compose exec backend python init_db.py
```

#### 本地开发环境
```bash
# 激活虚拟环境
source topshope_env/bin/activate

# 初始化数据库
cd backend
python init_db.py

# 启动后端
uvicorn main:app --reload

# 启动前端（新终端）
cd frontend
npm start
```

### 故障排除

#### 数据库枚举错误
如果遇到 "invalid input value for enum region" 错误：
1. 确保使用 Docker Compose 启动（会自动初始化）
2. 或者手动运行 `python init_db.py`

#### 端口冲突
如果端口被占用，可以修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8001:8000"  # 后端使用 8001 端口
  - "3001:3000"  # 前端使用 3001 端口
```

### 开发说明

- **数据库初始化**：在 Docker 环境中，数据库会在容器启动时自动初始化
- **热重载**：开发模式下，代码更改会自动重新加载
- **数据持久化**：PostgreSQL 和 Redis 数据会保存在 Docker volumes 中   