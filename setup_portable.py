#!/usr/bin/env python3

import os
import sys
import subprocess
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_command(cmd, description, exit_on_fail=True):
    print(f"[INFO] {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] {description} 失败: {result.stderr}")
        if exit_on_fail:
            input("请按回车键退出...")
            sys.exit(1)
        return False
    return True


def get_python_exe():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    python_exe = os.path.join(base_dir, "python_env", "python.exe")
    if not os.path.exists(python_exe):
        print(f"[ERROR] 找不到 python.exe: {python_exe}")
        input("请按回车键退出...")
        sys.exit(1)
    return python_exe


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    python_exe = get_python_exe()
    scripts_dir = os.path.join(base_dir, "python_env", "Scripts")

    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(base_dir, "browsers")
    os.environ["PLAYWRIGHT_DOWNLOAD_HOST"] = "https://npmmirror.com/mirrors/playwright/"

    print("=" * 50)
    print("  校园网自动连网配置工具")
    print("  正在初始化便携版 Python 环境...")
    print("=" * 50)
    print()

    if not os.path.exists("get-pip.py"):
        print("[ERROR] 找不到 get-pip.py，请确保文件在当前目录")
        input("请按回车键退出...")
        sys.exit(1)

    pip_exe = os.path.join(scripts_dir, "pip.exe")
    if not os.path.exists(pip_exe):
        print("[1/4] 正在安装 pip...")
        run_command(f'"{python_exe}" get-pip.py --no-warn-script-location', "安装 pip")
    else:
        print("[1/4] pip 已安装，跳过")

    print("[2/4] 正在安装 Playwright...")
    run_command(f'"{python_exe}" -m pip install playwright==1.40.0 --no-warn-script-location --quiet', "安装 Playwright")

    browsers_dir = os.path.join(base_dir, "browsers")
    if not os.path.exists(browsers_dir) or not os.listdir(browsers_dir):
        print("[3/4] 正在下载内置浏览器内核 (约100MB，请耐心等待)...")
        run_command(f'"{python_exe}" -m playwright install chromium', "安装 Chromium 浏览器")
    else:
        print("[3/4] 浏览器已存在，跳过")

    print()
    print("环境初始化完成！")

    print("[4/4] 正在配置开机自启...")
    if not is_admin():
        print("需要管理员权限，正在请求...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, f'"{os.path.join(base_dir, "install_task.py")}" --portable "{python_exe}"', None, 1)
        print("请在弹出的窗口中点击「是」授权")
        input("配置完成，请按回车键退出...")
    else:
        run_command(f'"{python_exe}" "{os.path.join(base_dir, "install_task.py")}" --portable "{python_exe}"', "配置开机自启", exit_on_fail=False)
        print()
        print("=" * 50)
        print("  配置完成！系统将自动连接校园网")
        print("=" * 50)
        input("请按回车键退出...")


if __name__ == "__main__":
    main()