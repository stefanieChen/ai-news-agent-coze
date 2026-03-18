from langchain.tools import tool, ToolRuntime
import json
import requests
from coze_workload_identity import Client
from coze_coding_utils.runtime_ctx.context import new_context

client = Client()

def get_wechat_webhook():
    """获取企业微信机器人webhook"""
    wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")
    webhook_key = json.loads(wechat_bot_credential)["webhook_key"]
    if "https" in webhook_key:
        import re
        webhook_key = re.search(r"key=([a-zA-Z0-9-]+)", webhook_key).group(1)
    return webhook_key

@tool
def send_wechat_message(content: str, runtime: ToolRuntime = None) -> str:
    """
    发送消息到企业微信群

    Args:
        content: 要发送的消息内容（支持Markdown格式）

    Returns:
        发送结果
    """
    try:
        webhook_key = get_wechat_webhook()
        webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"

        payload = {
            "msgtype": "markdown",
            "markdown": {"content": content}
        }

        response = requests.post(webhook_url, json=payload, timeout=15)
        result = response.json()

        if result.get("errcode", 0) == 0:
            return "消息发送成功"
        else:
            return f"发送失败: {result.get('errmsg', '未知错误')}"

    except Exception as e:
        return f"发送消息时发生错误: {str(e)}"
