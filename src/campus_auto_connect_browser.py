#!/usr/bin/env python3
"""
广科 校园网自动连接脚本 - Playwright 浏览器自动化版 (V3 终极DOM树定位版)
"""

import json
import logging
import os
import sys
import time
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:
    print("错误: 请先安装playwright：pip install playwright")
    sys.exit(1)

# 获取当前脚本所在目录的上级目录 (即 mykit 根目录)
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
LOG_PATH = os.path.join(BASE_DIR, 'campus_connect.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_PATH, encoding='utf-8') # 明确指定绝对路径
    ]
)
logger = logging.getLogger(__name__)

ISP_SUFFIX = {
    'free': '',
    'mobile': '', 
    'telecom': '@dx',
    'unicom': '@lt'
}

def load_config():
    config_file = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    if not os.path.exists(config_file):
        logger.error(f"配置文件不存在: {config_file}")
        sys.exit(1)

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"配置文件读取错误: {e}")
        sys.exit(1)

def login_with_browser(config):
    username = config.get('username', '')
    password = config.get('password', '')
    isp = config.get('isp', 'free')
    gateway_url = config.get('gateway_url', '')

    final_username = username + ISP_SUFFIX.get(isp, '')

    logger.info(f"目标网关: {gateway_url} | 账号: {final_username} | 运营商: {isp}")

    with sync_playwright() as p:
        # 如果你想看着它自动输入，可以把 headless=True 改为 headless=False
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            logger.info("正在加载登录页面...")
            page.goto(gateway_url, timeout=15000)
            
            # 稍微等待一下页面的 JS 渲染
            page.wait_for_load_state('networkidle', timeout=5000)

            # ==========================================
            # 核心判断逻辑：根据截图DOM，寻找“登录”按钮
            # ==========================================
            login_button = page.get_by_role("button", name="登录")
            
            if not login_button.is_visible():
                # 如果没看到登录按钮，检查是否有成功页面的标志（图2中的“可用状态”）
                if page.get_by_text("可用状态").is_visible():
                    logger.info("✓ [状态检测] 页面上显示'可用状态'，设备已经在线，无需重复登录！")
                    return True
                else:
                    logger.warning("未找到登录按钮，也未找到成功标志。可能页面加载异常。")
                    page.screenshot(path="debug_unknown_state.png")
                    return False

            logger.info("检测到未登录，开始填写表单...")
            
            # ==========================================
            # 填写表单：完美契合图1和图3的 DOM 树
            # ==========================================
            username_field = page.get_by_role("textbox", name="请输入账号")
            password_field = page.get_by_role("textbox", name="请输入您的密码")
            
            username_field.fill(final_username, timeout=3000)
            password_field.fill(password, timeout=3000)

            # 处理下拉菜单
            combobox = page.get_by_role("combobox")
            if isp == 'telecom':
                combobox.select_option(label="中国电信")
            elif isp == 'mobile':
                combobox.select_option(label="中国移动")
            elif isp == 'unicom':
                combobox.select_option(label="中国联通")
            else:
                combobox.select_option(label="校园网（免费）")
            logger.info(f"已选择网络下拉框。")

            # 点击登录
            logger.info("点击登录按钮...")
            login_button.click()

            # ==========================================
            # 验证结果：等待图2中的特征元素出现
            # ==========================================
            try:
                # 等待“可用状态”这几个字在页面上变为可见状态
                page.wait_for_selector('text="可用状态"', state='visible', timeout=5000)
                logger.info("✓ 登录成功！页面已刷新并显示在线状态。")
                return True
            except PlaywrightTimeoutError:
                logger.error("点击登录后，未在预期时间内看到成功标志。可能是密码错误或欠费。")
                page.screenshot(path="login_failed_screenshot.png")
                return False

        except Exception as e:
            logger.error(f"浏览器操作执行异常: {e}")
            page.screenshot(path="login_error_crash.png")
            return False
        finally:
            browser.close()

def login(config, retry_times=3, retry_interval=5):
    for attempt in range(1, retry_times + 1):
        try:
            logger.info(f"--- 第 {attempt}/{retry_times} 次尝试 ---")
            if login_with_browser(config):
                return True
        except Exception as e:
            logger.error(f"执行异常: {e}")

        if attempt < retry_times:
            logger.info(f"等待 {retry_interval} 秒后重试...")
            time.sleep(retry_interval)

    return False

def main():
    logger.info("=" * 50)
    logger.info("校园网自动连接工具 (V3 终极DOM版)")
    logger.info("=" * 50)

    try:
        config = load_config()
        success = login(config, config.get('retry_times', 3), config.get('retry_interval', 5))

        if success:
            logger.info("🎉 脚本执行完成，网络畅通！")
            sys.exit(0)
        else:
            logger.error("❌ 脚本执行失败。请查看当前目录下的 screenshot 截图排查原因。")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("手动中断")
        sys.exit(1)

if __name__ == '__main__':
    main()