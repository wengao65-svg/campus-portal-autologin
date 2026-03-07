# GitHub 开源准备指南

## 已创建的文件

以下文件已在 `/tmp/` 目录准备好，请复制到项目根目录：

### 1. LICENSE
标准的 MIT 开源协议文件

```bash
cp /tmp/LICENSE LICENSE
```

### 2. .gitignore
增强的 .gitignore，包含敏感文件保护

```bash
cp /tmp/.gitignore.new .gitignore
```

### 3. SECURITY.md
安全说明文档，包含：
- 敏感信息保护说明
- 安全最佳实践
- 漏洞报告指引

```bash
cp /tmp/SECURITY.md SECURITY.md
```

### 4. README.md
更新的 README，包含：
- GitHub Star/Fork 徽章
- 安全与隐私章节
- 更详细的贡献指南

```bash
cp /tmp/README_open_source.md README.md
```

### 5. GitHub 模板

Issue 和 Pull Request 模板：

```bash
mkdir -p .github/ISSUE_TEMPLATE
cp /tmp/.github/PULL_REQUEST_TEMPLATE.md .github/PULL_REQUEST_TEMPLATE.md
cp /tmp/.github/ISSUE_TEMPLATE/bug_report.md .github/ISSUE_TEMPLATE/bug_report.md
cp /tmp/.github/ISSUE_TEMPLATE/feature_request.md .github/ISSUE_TEMPLATE/feature_request.md
```

## 敏感信息检查结果

✅ **config.json** - 不存在，无需清理
⚠️ **日志文件** - 发现 2 个日志文件：
  - `./src/campus_connect.log`
  - `./campus_connect.log`

**建议操作**：
```bash
# 删除日志文件（如果包含敏感信息）
rm src/campus_connect.log
rm campus_connect.log
```

## GitHub 仓库初始化步骤

### 1. 初始化 Git 仓库

```bash
git init
git branch -M main
```

### 2. 复制准备好的文件

```bash
# 复制所有准备好的文件
cp /tmp/LICENSE .
cp /tmp/.gitignore.new .gitignore
cp /tmp/SECURITY.md .
cp /tmp/README_open_source.md README.md

# 复制 GitHub 模板
mkdir -p .github/ISSUE_TEMPLATE
cp /tmp/.github/PULL_REQUEST_TEMPLATE.md .github/
cp /tmp/.github/ISSUE_TEMPLATE/*.md .github/ISSUE_TEMPLATE/
```

### 3. 添加文件到 Git

```bash
git add .
git status  # 检查是否有敏感文件被误加入
```

### 4. 首次提交

```bash
git commit -m "Initial commit: Campus AutoConnect with MIT License"
```

### 5. 推送到 GitHub

```bash
# 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/YOUR_USERNAME/mykit.git

# 推送
git push -u origin main
```

## 重要提醒

### ✅ 必须做的事情

1. **检查 .gitignore 确认敏感文件被忽略**
   ```bash
   git check-ignore -v config.json
   # 应该输出 matched，表示被忽略
   ```

2. **确认没有敏感信息被提交**
   ```bash
   git ls-files
   # 检查列表中是否有 config.json、*.log、*.png
   ```

3. **更新 README 中的 GitHub 用户名**
   - 将 `username/mykit` 替换为你的实际 GitHub 用户名
   - 更新 Star/Fork 徽章链接

### ⚠️ 注意事项

- **config.json** 不会被提交（已在 .gitignore 中）
- 用户需要手动从 `config.json.template` 创建 `config.json`
- 日志和截图文件不会被提交（已在 .gitignore 中）
- `run_hidden.vbs` 不会被提交（包含绝对路径）

## 提交前最终检查清单

- [ ] LICENSE 文件已存在
- [ ] SECURITY.md 文件已存在
- [ ] .gitignore 包含所有敏感文件
- [ ] README.md 已更新开源信息
- [ ] GitHub 模板已创建
- [ ] config.json 不在待提交列表
- [ ] 日志文件已删除
- [ ] README 中的用户名已更新
- [ ] 已检查 `git status` 确认无敏感文件

## 推荐的 GitHub 设置

### Repository Topics
在 GitHub 仓库设置中添加这些标签：
- campus-network
- automation
- python
- playwright
- drcom
- login-automation

### Repository Description
```
广科校园网自动连接工具 - 基于 Python + Playwright 的浏览器自动化解决方案，支持开机静默自动登录
```

### Security & Analysis
- 启用 Dependabot（依赖更新提醒）
- 启用 Code scanning（代码扫描）
- 启用 Secret scanning（敏感信息扫描）

## 后续维护

1. **定期更新版本号**（如果使用版本管理）
2. **维护 CHANGELOG.md**（记录版本变更）
3. **及时响应 Issue 和 PR**
4. **定期更新依赖**（Playwright、Python 等）

