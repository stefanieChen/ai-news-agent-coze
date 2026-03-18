#!/usr/bin/env python3
"""
AI新闻定时推送脚本
每天自动搜索AI新闻并发送到指定平台
"""

import sys
import os
import json
import requests
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools.news_search_tool import search_ai_news
from src.tools.email_tool import send_news_email
from src.tools.wechat_tool import send_wechat_message
from src.tools.feishu_tool import send_feishu_message
from src.agents.agent import build_agent
from coze_coding_utils.runtime_ctx.context import new_context

def generate_news_summary():
    """搜索并生成AI新闻摘要"""
    print(f"[{datetime.now()}] 开始搜索AI新闻...")
    
    # 搜索新闻
    result = search_ai_news("AI人工智能 最新动态")
    
    print(f"[{datetime.now()}] 新闻搜索完成")
    return result

def send_to_email(content, recipient_email):
    """发送到邮箱"""
    print(f"[{datetime.now()}] 发送邮件到 {recipient_email}...")
    
    subject = f"[AI热点日报] {datetime.now().strftime('%Y-%m-%d')} - AI领域热点新闻汇总"
    result = send_news_email(subject, content, recipient_email)
    
    print(f"[{datetime.now()}] 邮件发送结果: {result}")
    return result

def send_to_wechat(content):
    """发送到企业微信"""
    print(f"[{datetime.now()}] 推送到企业微信...")
    
    result = send_wechat_message(content)
    
    print(f"[{datetime.now()}] 企业微信推送结果: {result}")
    return result

def send_to_feishu(content):
    """发送到飞书"""
    print(f"[{datetime.now()}] 推送到飞书...")
    
    title = f"AI热点日报 - {datetime.now().strftime('%Y-%m-%d')}"
    result = send_feishu_message(title, content)
    
    print(f"[{datetime.now()}] 飞书推送结果: {result}")
    return result

def main():
    """主函数"""
    print("=" * 60)
    print(f"AI新闻定时推送任务开始 - {datetime.now()}")
    print("=" * 60)
    
    # 读取配置
    config_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "config/schedule_config.json")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 搜索新闻
    news_content = generate_news_summary()
    
    # 推送到配置的平台
    platforms = config.get("platforms", {})
    
    # 发送邮件
    if platforms.get("email", {}).get("enabled"):
        recipient = platforms["email"].get("recipient")
        if recipient:
            send_to_email(news_content, recipient)
    
    # 发送到企业微信
    if platforms.get("wechat", {}).get("enabled"):
        send_to_wechat(news_content)
    
    # 发送到飞书
    if platforms.get("feishu", {}).get("enabled"):
        send_to_feishu(news_content)
    
    print("=" * 60)
    print(f"AI新闻定时推送任务完成 - {datetime.now()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
