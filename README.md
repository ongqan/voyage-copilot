# Voyage Copilot

Voyage Copilot 是面向旅行权益平台的AI旅程编排与异常履约系统。本仓库已经进入MVP开发阶段。

## 目录

```text
voyage-copilot/
├── apps/
│   ├── api/              # FastAPI业务API
│   └── web/              # Next.js用户端纵向切片
├── packages/
│   └── contracts/        # OpenAPI与共享契约
├── data/
│   └── seeds/            # 虚拟演示数据
├── tests/                # 跨应用/端到端测试预留
├── infra/                # 部署与本地环境配置
└── document/             # PRD、设计、架构、测试与原型
```

产品和研发规格统一从[文档中心](document/README.md)进入。可点击低保真原型位于[document/prototype/index.html](document/prototype/index.html)。

## 当前开发状态

当前已完成三端MVP演示产品：

```text
用户端：首页、行程、权益、推荐、AI对话、时间线、模拟订单、异常处理
客服端：会话队列、AI摘要、人工接管、工单处理
运营端：业务看板、知识、规则、服务、AI质量
```

本地SQLite和Demo API用于MVP演示；生产基线仍为PostgreSQL、OIDC、真实模型与受控外部适配器。

## 快速开始

### API

```bash
python3 -m venv .venv
.venv/bin/pip install -r apps/api/requirements-dev.txt
.venv/bin/uvicorn app.main:app --app-dir apps/api --reload --port 8000
```

API文档：`http://localhost:8000/docs`

### Web

```bash
pnpm install
pnpm dev:web
```

Web地址：`http://localhost:3000`。默认API地址为 `http://localhost:8000/api/v1`，可通过 `NEXT_PUBLIC_API_BASE_URL` 覆盖。

## 公网演示

GitHub Pages自动部署地址：`https://ongqan.github.io/voyage-copilot/`。公开Demo使用浏览器本地模拟数据，不会把访问者行程发送到服务端。部署配置和首次启用说明见[部署文档](document/12-DEPLOYMENT.md)。

### 测试

```bash
pnpm test:api
pnpm typecheck:web
pnpm build:web
```

## Demo身份

开发环境通过以下请求头模拟已认证上下文：

- `X-Demo-Tenant-ID: tenant_demo_01`
- `X-Demo-User-ID: user_demo_001`

这些请求头仅在 `APP_ENV=development|test` 时启用，不能作为生产认证方案。
