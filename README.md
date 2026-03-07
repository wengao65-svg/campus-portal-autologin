# 🌐 广科 校园网自动连接工具

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/wengao65-svg/mykit?style=social)](https://github.com/wengao65-svg/mykit/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/wengao65-svg/mykit?style=social)](https://github.com/wengao65-svg/mykit/network/members)

基于 **Python** 和 **Playwright** 框架的校园网自动连接工具，专为解决校园网计费网关频繁掉线需要手动登录的问题设计。

通过 **Windows 任务计划程序**，可实现开机后台静默自动运行，无需手动干预。

---

## ✨ 特性

- ✅ **全自动登录** - 无需手动输入账号密码
- ✅ **智能状态检测** - 自动判断是否已登录，避免重复连接
- ✅ **多运营商支持** - 支持校园网/电信/移动/联通
- ✅ **自动重试** - 登录失败自动重试，可配置次数和间隔
- ✅ **完全静默** - 开机后台运行，无窗口弹出
- ✅ **详细日志** - 记录每次运行状态，便于问题排查
- ✅ **错误截图** - 失败时自动截图保存

---

## 📁 项目结构

```
mykit/
├── src/
│   └── campus_auto_connect_browser.py   # 核心脚本
├── tests/                               # 测试文件（如果有）
├── config.json.template                 # 配置文件模板
├── config.json                          # 用户配置文件（需手动创建）
├── requirements.txt                     # 依赖清单
├── install_task.py                      # 一键安装开机自启（Python 版本）
├── run_hidden.vbs                       # 静默运行脚本（自动生成）
├── remove_task_scheduler.bat            # 一键卸载开机自启
├── .gitignore                           # Git 忽略配置
└── README.md                            # 本文件
```

---

## 🛠️ 安装步骤

### 1. 安装 Python

前往 [Python 官网](https://www.python.org/downloads/) 下载并安装 **Python 3.8 或更高版本**。

> ⚠️ **重要**：安装时务必勾选 **"Add Python to PATH"**

### 2. 安装依赖

打开命令行终端，进入项目目录，执行以下命令：

```bash
# 安装 Playwright
pip install playwright==1.40.0

# 设置国内镜像（可选，加速下载）
# PowerShell:
$env:PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright/"

# CMD:
set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/

# 安装 Chromium 浏览器
playwright install chromium
```

---

## ⚙️ 配置

### 1. 创建配置文件

在项目根目录下，复制 `config.json.template` 并重命名为 `config.json`

### 2. 编辑配置

使用文本编辑器打开 `config.json`，修改以下参数：

```json
{
  "username": "你的校园网账号",
  "password": "你的校园网密码",
  "isp": "telecom",
  "gateway_url": "http://YOUR_GATEWAY_IP",
  "retry_times": 3,
  "retry_interval": 5
}
```

| 参数 | 类型 | 说明 | 可选值 |
|:-----|:-----|:-----|:--------|
| `username` | string | 学号或宽带账号（不需要加后缀） | `"123456789"` |
| `password` | string | 校园网密码 | `"MyPass123"` |
| `isp` | string | 运营商 | `free`（免费）、`telecom`（电信）、`mobile`（移动）、`unicom`（联通）|
| `gateway_url` | string | 校园网登录页面地址 | `"http://YOUR_GATEWAY_IP"` |
| `retry_times` | number | 失败重试次数 | 默认 `3` |
| `retry_interval` | number | 重试间隔（秒） | 默认 `5` |

**注意**：脚本会自动根据 ISP 选择添加对应账号后缀（电信 `@dx`、联通 `@lt`）

---

## 🚀 使用方法

### 手动运行测试

首次使用建议先手动运行测试：

```bash
python src/campus_auto_connect_browser.py
```

**运行结果**：
- `✓ 登录成功` - 配置正确，可以设置开机自启
- `✗ 执行失败` - 查看日志和截图排查问题

**错误排查**：
- 检查 `campus_connect.log` 日志文件（项目根目录）
- 查看可能生成的截图：`login_failed_screenshot.png`、`login_error_crash.png`、`debug_unknown_state.png`

---

### 设置开机自启（推荐）

确认手动运行成功后，设置开机自动连接：

```bash
# 以管理员身份运行
python install_task.py
```

或直接在文件管理器中右键 `install_task.py` → "使用管理员 PowerShell 运行"

脚本会自动：
1. 请求管理员权限
2. 生成静默启动脚本 `run_hidden.vbs`
3. 注册 Windows 任务计划（开机登录后 30 秒触发）
4. 完成，无需手动干预

### 取消开机自启

```bash
# 以管理员身份运行
remove_task_scheduler.bat
```

或右键 `remove_task_scheduler.bat` → "以管理员身份运行"

---

## 💡 常见问题

### Q1：开机没有自动连上？

**排查步骤**：

1. 检查 `campus_connect.log` 是否有新日志
   - 有新日志 → 任务已触发但登录失败，检查账号密码或是否欠费
   - 无新日志 → 任务计划未生效，重新运行 `install_task.py`

2. 检查截图文件，确认页面加载状态

### Q2：提示 `playwright: command not found`？

**解决**：执行 `playwright install chromium` 安装浏览器

### Q3：提示"未找到登录按钮"？

**排查**：
1. 确保已连接校园 WiFi 或网线
2. 确认能访问网关地址 `https://your.gateway.ip`
3. 查看截图确认页面是否正常

### Q4：如何查看日志？

日志文件位置：`campus_connect.log`（项目根目录）

---

## 📊 日志示例

```log
2026-03-06 22:32:12 - INFO - ==================================================
2026-03-06 22:32:12 - INFO - 校园网自动连接工具 (V3 终极DOM版)
2026-03-06 22:32:12 - INFO - ==================================================
2026-03-06 22:32:12 - INFO - --- 第 1/3 次尝试 ---
2026-03-06 22:32:12 - INFO - 目标网关: http://your.gateway.ip | 账号: 123456789@dx | 运营商: telecom
2026-03-06 22:32:12 - INFO - 正在加载登录页面...
2026-03-06 22:32:13 - INFO - 检测到未登录，开始填写表单...
2026-03-06 22:32:20 - INFO - 已选择网络下拉框。
2026-03-06 22:32:21 - INFO - 点击登录按钮...
2026-03-06 22:32:26 - INFO - ✓ 登录成功！页面已刷新并显示在线状态。
2026-03-06 22:32:26 - INFO - 🎉 脚本执行完成，网络畅通！
```

---

## 🔒 安全与隐私

本项目重视用户隐私和安全：

- ✅ **本地运行** - 所有数据仅保存在本地，不会上传到任何服务器
- ✅ **开源透明** - 代码完全开源，可自行审计
- ✅ **敏感保护** - 配置文件已加入 `.gitignore`，不会被提交到仓库
- ✅ **MIT 协议** - 自由使用、修改和分发

请查看 [SECURITY.md](SECURITY.md) 了解详细的安全说明和最佳实践。

---

## 🤝 贡献

欢迎贡献代码、报告 Bug 或提出建议！

### 报告 Bug

使用 GitHub Issues 提交 Bug 报告，请提供：
- 详细的问题描述
- 复现步骤
- 环境信息（系统、Python 版本）
- 相关日志和截图

### 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

**重要**：
- 请遵循现有代码风格
- 确保代码通过测试（如果有）
- 提交前请检查是否不小心提交了敏感信息

---

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源协议。您可以自由使用、修改和分发本软件。

---

## 🙏 致谢

- [Playwright](https://playwright.dev/) - 强大的浏览器自动化框架
- 校园网认证系统

---

<div align="center">

**[⭐ Star](../../stargazers) 本项目，支持开源开发**

Made with ❤️ by 广科学生 · [MIT License](LICENSE)

</div>
