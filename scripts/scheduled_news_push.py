#!/usr/bin/env python3
"""
AI新闻定时推送脚本
每天自动搜索AI新闻并发送到指定平台
"""

import sys
import os
import json
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from src.tools.email_tool import send_news_email
from src.tools.feishu_tool import send_feishu_message

def search_news(query="AI人工智能 最新动态", sites=""):
    """搜索AI新闻（非tool包装版本）"""
    try:
        # 创建context
        ctx = new_context(method="search_news")
        
        # 初始化搜索客户端
        client = SearchClient(ctx=ctx)
        
        # 准备搜索参数
        search_params = {
            "query": query,
            "search_type": "web",
            "count": 20,
            "need_summary": True,
            "time_range": "1d"
        }
        
        # 如果指定了网站
        if sites and sites.strip():
            search_params["sites"] = sites.strip()
            print(f"🔍 在指定网站搜索: {sites.strip()}")
        
        # 执行搜索
        response = client.search(**search_params)
        
        if not response.web_items or len(response.web_items) == 0:
            return "未找到相关新闻，请尝试更换关键词或稍后再试。"
        
        # 格式化搜索结果
        result_text = f"搜索到 {len(response.web_items)} 条AI相关新闻:\n\n"
        
        for idx, item in enumerate(response.web_items, 1):
            result_text += f"{idx}. {item.title}\n"
            result_text += f"   来源: {item.site_name}\n"
            result_text += f"   时间: {item.publish_time or '未知'}\n"
            result_text += f"   摘要: {item.summary[:200] if item.summary else (item.snippet[:200] if item.snippet else '')}...\n"
            result_text += f"   链接: {item.url}\n\n"
        
        return result_text
        
    except Exception as e:
        print(f"搜索新闻时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"搜索新闻时发生错误: {str(e)}"

def generate_news_summary():
    """搜索并生成AI新闻摘要"""
    print(f"[{datetime.now()}] 开始搜索AI新闻...")
    
    # 搜索新闻
    result = search_news("AI人工智能 最新动态")
    
    print(f"[{datetime.now()}] 新闻搜索完成")
    return result

def send_to_email(content, recipient_email):
    """发送到邮箱"""
    print(f"[{datetime.now()}] 发送邮件到 {recipient_email}...")
    
    subject = f"[AI热点日报] {datetime.now().strftime('%Y-%m-%d')} - AI领域热点新闻汇总"
    result = send_news_email(subject, content, recipient_email)
    
    print(f"[{datetime.now()}] 邮件发送结果: {result}")
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
    config_path = os.path.join(os.path.dirname(__file__), "schedule_config.json")
    
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
    
    # 发送到飞书
    if platforms.get("feishu", {}).get("enabled"):
        send_to_feishu(news_content)
    
    print("=" * 60)
    print(f"AI新闻定时推送任务完成 - {datetime.now()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
