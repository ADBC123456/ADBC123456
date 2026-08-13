# 安装

1. 创建公开的 `你的用户名/你的用户名` Profile 仓库。
2. 把本目录所有文件上传到该仓库。
3. 修改 `config.json` 中的姓名、职业、技能、状态和当前任务。
4. 修改 `README.md` 中的 `YOUR_GITHUB_USERNAME`。
5. GitHub → Actions → Update GitHub RPG Profile → Run workflow。
6. 成功后 `generated/terminal.svg` 和 `generated/rpg.svg` 会自动更新。
7. Workflow 每天 00:00 UTC 自动运行，即新加坡时间 08:00。

不需要创建 Personal Access Token；Workflow 使用内置 `GITHUB_TOKEN`。

注意：当前 RPG 的 Commit 部分使用轻量 Activity Score，而不是精确 Contribution Calendar。后续可以升级成 GitHub GraphQL 版，统计真实 Commit、连续贡献天数和年度贡献图。
