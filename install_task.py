import os
import sys
import subprocess
import ctypes
import argparse


def is_admin():
    """检查当前是否拥有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--portable', type=str, help='便携Python路径')
    args = parser.parse_args()
    
    # 1. 自动请求管理员权限
    if not is_admin():
        print("正在请求管理员权限，请在弹出的窗口中点击“是”...")
        # 以管理员身份重新启动自身
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return

    print("==================================================")
    print("  校园网自动连接 - 计划任务安装工具 (Python终极版)")
    print("==================================================")

    # 2. 绝对路径获取（彻底解决找不到文件的问题）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "src", "campus_auto_connect_browser.py")
    vbs_path = os.path.join(base_dir, "run_hidden.vbs")
    
    if args.portable and os.path.exists(args.portable):
        python_exe = args.portable
    else:
        python_exe = sys.executable

    if not os.path.exists(script_path):
        print(f"[错误] 找不到核心脚本: {script_path}")
        input("请按回车键退出...")
        return

    # 3. 动态生成隐藏运行的 VBS 脚本
    print(f"\n[1/3] 正在生成静默启动脚本...")
    vbs_content = f'Set WshShell = CreateObject("WScript.Shell")\n'
    vbs_content += f'WshShell.Run """{python_exe}"" ""{script_path}""", 0, False\n'
    
    with open(vbs_path, "w", encoding="utf-8") as f:
        f.write(vbs_content)

    # 4. 注册 Windows 任务计划
    task_name = "GXUST_Campus_AutoConnect"
    print(f"[2/3] 正在注册 Windows 任务计划: {task_name}")
    
    # 先尝试清理可能的旧任务（屏蔽输出）
    subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 创建新任务：用户登录时触发，延迟30秒，赋予最高权限
    cmd = f'schtasks /create /tn "{task_name}" /tr "wscript.exe \\"{vbs_path}\\"" /sc onlogon /delay 0000:30 /f /rl highest'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="gbk")

    # 5. 结果反馈
    if result.returncode == 0:
        print("\n[SUCCESS] 开机自启任务已完美配置！")
        print(f"绑定的 Python 路径: {python_exe}")
        print("每次开机登录桌面后约 30 秒，它将在后台静默为你连接网络。")
    else:
        print(f"\n[FAILED] 任务创建失败: {result.stderr}")

    input("\n配置完成，请按回车键退出...")

if __name__ == "__main__":
    main()