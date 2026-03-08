import os
import sys
import subprocess
import ctypes
import argparse


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--portable', type=str, help='便携Python路径')
    args = parser.parse_args()

    if not is_admin():
        print("正在请求管理员权限，请在弹出的窗口中点击「是」...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return

    print("==================================================")
    print("  校园网自动连接 - 计划任务安装工具 (环境修复强化版)")
    print("==================================================")

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

    print(f"\n[1/4] 正在生成静默启动脚本 (已锁定工作目录)...")
    vbs_content = f'Set WshShell = CreateObject("WScript.Shell")\n'
    vbs_content += f'WshShell.CurrentDirectory = "{base_dir}"\n'
    vbs_content += f'WshShell.Run """{python_exe}"" ""{script_path}""", 0, False\n'

    with open(vbs_path, "w", encoding="utf-8") as f:
        f.write(vbs_content)

    task_name = "GXUST_Campus_AutoConnect"
    print(f"[2/4] 正在清理可能存在的旧任务...")
    subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"[3/4] 正在注册 Windows 任务计划: {task_name}")
    cmd = f'schtasks /create /tn "{task_name}" /tr "wscript.exe \\"{vbs_path}\\"" /sc onlogon /delay 0000:30 /f /rl highest'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="gbk")

    if result.returncode == 0:
        print(f"[4/4] 正在解除笔记本「仅插电运行」的限制...")
        ps_cmd = f'Set-ScheduledTask -TaskName "{task_name}" -Settings (New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries)'
        ps_result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

        if ps_result.returncode == 0:
            print("\n[SUCCESS] 开机自启任务已完美配置！")
            print(f"绑定的 Python 路径: {python_exe}")
            print("每次开机登录桌面后约 30 秒，它将在后台静默为你连接网络。")
            print("🚀 [已优化] 无论是否插着电源，任务都会正常触发！")
        else:
            print("\n[WARNING] 任务创建成功，但解除电源限制失败。建议手动在「任务计划程序」中取消勾选电源条件。")
    else:
        print(f"\n[FAILED] 任务创建失败: {result.stderr}")

    input("\n配置完成，请按回车键退出...")


if __name__ == "__main__":
    main()
