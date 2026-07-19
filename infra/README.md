# Infrastructure

Sprint 0使用本地SQLite和两个开发进程。后续引入PostgreSQL、Redis、对象存储和容器配置时统一放在本目录，不把环境文件散落到应用目录。

约定：

- 本地持久化数据写入根目录 `.data/`；
- 密钥和环境变量不进入仓库；
- 环境模板使用 `.env.example`；
- 数据库迁移、Docker和部署声明在本目录分层管理；
- 生产基线仍以 `document/04-SYSTEM-DESIGN.md` 为准。

