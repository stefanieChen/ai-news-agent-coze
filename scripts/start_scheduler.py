#!/usr/bin/env python3
"""
启动定时推送服务
使用APScheduler实现每天定时推送AI新闻到邮箱
"""

import sys
import os
import json
from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scheduled_news_push import main as push_news

# 设置时区为中国标准时间 (UTC+8)
CST_TZ = timezone(timedelta(hours=8))

def load_schedule_config():
    """加载定时配置"""
    config_path = os.path.join(os.path.dirname(__file__), "schedule_config.json")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def job():
    """定时任务：推送AI新闻"""
    print("\n" + "=" * 60)
    print(f"[{datetime.now()}] 定时任务触发：开始推送AI新闻")
    print("=" * 60)
    
    try:
        push_news()
        print(f"[{datetime.now()}] 推送完成")
    except Exception as e:
        print(f"[{datetime.now()}] 推送失败: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """主函数：启动定时调度器"""
    print("=" * 60)
    print("AI新闻定时推送服务")
    print("=" * 60)
    
    # 加载配置
    config = load_schedule_config()
    schedule_config = config.get("schedule", {})
    
    time_str = schedule_config.get("time", "09:00")
    timezone = schedule_config.get("timezone", "Asia/Shanghai")
    
    # 解析时间
    hour, minute = map(int, time_str.split(":"))
    
    print(f"\n⏰ 定时推送时间: 每天 {time_str}")
    print(f"🌍 时区: {timezone}")
    
    # 检查邮件配置
    email_config = config.get("platforms", {}).get("email", {})
    if email_config.get("enabled"):
        recipient = email_config.get("recipient", "your-email@example.com")
        if recipient == "your-email@example.com":
            print("\n⚠️  警告: 收件邮箱未配置！")
            print("   请修改 scripts/schedule_config.json 中的 recipient 字段")
            print("   或设置环境变量 DEFAULT_RECIPIENT_EMAIL")
            return
        print(f"📧 收件邮箱: {recipient}")
    
    print("\n✅ 定时推送服务启动中...")
    print("   按 Ctrl+C 停止服务\n")
    
    # 创建调度器（使用中国标准时间）
    scheduler = BlockingScheduler(timezone=CST_TZ)

    # 添加定时任务（每天指定时间执行）
    scheduler.add_job(
        job,
        CronTrigger(hour=hour, minute=minute, timezone=CST_TZ),
        id='ai_news_push',
        name='AI新闻推送',
        replace_existing=True
    )
    
    # 启动调度器
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n\n⏹️  定时推送服务已停止")
        scheduler.shutdown()

if __name__ == "__main__":
    main()
