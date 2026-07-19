# Voyage Copilot 部署说明

## 公网演示

项目通过GitHub Actions构建Next.js静态导出并发布到GitHub Pages。每次推送`main`都会执行类型检查、静态构建和部署。

- 站点路径：`https://ongqan.github.io/voyage-copilot/`
- 工作流：`.github/workflows/deploy-pages.yml`
- 部署模式：公开MVP Demo，浏览器本地保存模拟行程

## 数据边界

GitHub Pages版本不会发送真实会员、行程、权益或订单数据。公开Demo的新增行程仅保存在访问者浏览器的`localStorage`中。仓库中的FastAPI服务仍用于本地联调、自动化测试和未来独立API部署。

## 首次启用

仓库管理员需要在GitHub的`Settings → Pages → Build and deployment`中将`Source`设为`GitHub Actions`。之后可以在`Actions → Deploy public demo`查看部署状态或手工重跑。

## 本地验证静态产物

```bash
STATIC_EXPORT=true pnpm build:web
```

产物位于`apps/web/out`。
