# 🌐 广科 校园网自动连接工具

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)

基于 **Python** 和 **Playwright** 的校园网自动连接工具，解决校园网计费网关频繁掉线需要手动登录的问题。

支持开机后台静默自动运行，无需手动干预。

---

## ✨ 特性

- 🚀 **全自动登录** - 无需手动输入账号密码
- 🧠 **智能状态检测** - 自动判断是否已登录，避免重复连接
- 📶 **多运营商支持** - 支持校园网/电信/移动/联通
- 🔄 **自动重试** - 登录失败自动重试，可配置次数和间隔
- 🔇 **完全静默** - 开机后台运行，无窗口弹出
- 📝 **详细日志** - 记录每次运行状态，便于问题排查

---

## 🚀 快速开始（小白版 - 推荐）

如果你是普通用户，不想手动安装 Python，使用便携版：

### 📥 下载便携版

**[下载 CampusPortalAutologin-v1.0.0.zip (12.4MB)](../../releases/download/v1.0.0/CampusPortalAutologin-v1.0.0.zip)**

### 步骤 1：解压并配置

1. 解压下载的压缩包到任意目录（不要包含中文路径）
2. 复制 `config.json.template` 并重命名为 `config.json`
3. 使用文本编辑器打开 `config.json`，填写以下信息：

```json
{
  "username": "你的学号",
  "password": "你的校园网密码",
  "isp": "telecom",
  "gateway_url": "http://你的网关IP",
  "retry_times": 3,
  "retry_interval": 5
}
```

**配置说明**：

| 参数 | 说明 | 可选值 |
|:-----|:-----|:--------|
| `username` | 学号（不要加后缀） | `"123456789"` |
| `password` | 校园网密码 | `"你的密码"` |
| `isp` | 运营商 | `free`(免费)、`telecom`(电信)、`mobile`(移动)、`unicom`(联通) |
| `gateway_url` | 网关地址 | `"http://192.168.1.1"` |
| `retry_times` | 失败重试次数 | 默认 `3` |
| `retry_interval` | 重试间隔（秒） | 默认 `5` |

### 步骤 2：自动安装

双击 **`setup.bat`**，脚本会自动完成：

1. 安装 pip 包管理器
2. 安装 Playwright 依赖
3. 下载 Chromium 浏览器内核（约 100MB，首次运行）
4. 配置开机自启任务

> ⚠️ 首次运行会请求管理员权限，请点击「是」

### 步骤 3：完成

- 开机后会自动连接校园网
- 查看日志文件 `campus_connect.log` 确认运行状态
- 如需手动测试：`python_env\python.exe src\campus_auto_connect_browser.py`

---

## 📋 关于便携版

便携版已包含 **Python 3.11.9**，无需安装系统级 Python。

**文件大小**: 12.4MB（解压后约 25MB）

**包含内容**:
- 便携版 Python 环境
- 所有配置脚本
- 核心运行脚本

**首次运行**:
- 会自动下载 Chromium 浏览器内核（约 100MB）
- 需要网络连接

详细发布说明请查看 [Releases](../../releases)

---

## 🛠️ 开发者安装（手动版）

如果你熟悉 Python，想自定义安装：

### 1. 安装 Python

前往 [Python 官网](https://www.python.org/downloads/) 下载并安装 **Python 3.8 或更高版本**。

> ⚠️ 安装时务必勾选 **"Add Python to PATH"**

### 2. 安装依赖

```bash
pip install playwright==1.40.0

# 安装 Chromium 浏览器
playwright install chromium
```

### 3. 配置和运行

1. 复制 `config.json.template` 为 `config.json` 并填写配置
2. 运行测试：`python src/campus_auto_connect_browser.py`
3. 配置开机自启：`python install_task.py`（需要管理员权限）

---

## 📁 项目结构

**源码仓库**（开发用）:
```
mykit/
├── src/
│   └── campus_auto_connect_browser.py   # 核心脚本
├── config.json.template                 # 配置文件模板
├── setup_portable.py                    # 配置脚本
├── install_task.py                      # 开机自启配置
├── remove_task_scheduler.bat            # 卸载开机自启
├── build_portable.py                    # 构建便携版（开发者用）
└── README.guide.md                       # 使用文档
```

**便携版包**（[从 Releases 下载](../../releases)）:
```
mykit/
├── src/
│   └── campus_auto_connect_browser.py   # 核心脚本
├── python_env/                          # 便携版 Python 3.11.9
├── browsers/                            # 浏览器内核（运行时下载）
├── config.json.template                 # 配置文件模板
├── config.json                          # 用户配置（需手动创建）
├── setup_portable.py                    # 配置脚本
├── setup.bat                           # 双击运行（推荐）
├── install_task.py                      # 开机自启配置
├── run_hidden.vbs                       # 静默运行脚本（自动生成）
├── remove_task_scheduler.bat            # 卸载开机自启
└── README.guide.md                       # 使用文档
```

---

## 💡 常见问题

### Q1：开机没有自动连接？

1. 检查 `campus_connect.log` 是否有新日志
   - 有日志 → 已触发但登录失败，检查账号密码或是否欠费
   - 无日志 → 任务计划未生效，双击 `setup.bat` 重新配置

2. 查看截图文件确认页面状态

### Q2：提示"找不到 python.exe"？

确保 `python_env` 目录完整，重新解压压缩包

### Q3：提示"未找到登录按钮"？

1. 确保已连接校园 WiFi 或网线
2. 确认能访问网关地址
3. 查看截图确认页面是否正常

### Q4：如何查看日志？

日志文件位置：`campus_connect.log`（项目根目录）

### Q5：如何卸载开机自启？

右键 `remove_task_scheduler.bat` → 以管理员身份运行

---

## 📊 日志示例

```log
2026-03-07 10:32:12 - INFO - ==================================================
2026-03-07 10:32:12 - INFO - 校园网自动连接工具 (V3 终极DOM版)
2026-03-07 10:32:12 - INFO - ==================================================
2026-03-07 10:32:12 - INFO - --- 第 1/3 次尝试 ---
2026-03-07 10:32:12 - INFO - 目标网关: http://192.168.1.1 | 账号: 123456789@dx | 运营商: telecom
2026-03-07 10:32:12 - INFO - 正在加载登录页面...
2026-03-07 10:32:13 - INFO - 检测到未登录，开始填写表单...
2026-03-07 10:32:20 - INFO - 已选择网络下拉框。
2026-03-07 10:32:21 - INFO - 点击登录按钮...
2026-03-07 10:32:26 - INFO - ✓ 登录成功！页面已刷新并显示在线状态。
2026-03-07 10:32:26 - INFO - 🎉 脚本执行完成，网络畅通！
```

---

## 🔒 安全与隐私

- ✅ **本地运行** - 所有数据仅保存在本地，不会上传
- ✅ **开源透明** - 代码完全开源，可自行审计
- ✅ **敏感保护** - 配置文件已加入 `.gitignore`，不会提交

---

## 📜 许可证

MIT License - 自由使用、修改和分发

---

<div align="center">

**[⭐ Star](../../stargazers) 支持开源开发**

Made with ❤️

</div>
