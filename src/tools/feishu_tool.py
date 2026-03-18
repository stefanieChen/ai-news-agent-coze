from langchain.tools import tool, ToolRuntime
import json
import requests
from coze_workload_identity import Client
from coze_coding_utils.runtime_ctx.context import new_context

client = Client()

def get_feishu_webhook():
    """获取飞书机器人webhook"""
    feishu_credential = client.get_integration_credential("integration-feishu-message")
    webhook_url = json.loads(feishu_credential)["webhook_url"]
    return webhook_url

@tool
def send_feishu_message(title: str, content: str, runtime: ToolRuntime = None) -> str:
    """
    发送消息到飞书群

    Args:
        title: 消息标题
        content: 消息内容（支持富文本格式）

    Returns:
        发送结果
    """
    try:
        webhook_url = get_feishu_webhook()

        payload = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            [{"tag": "text", "text": content}]
                        ]
                    }
                }
            }
        }

        response = requests.post(webhook_url, json=payload, timeout=15)
        result = response.json()

        if result.get("StatusCode", 0) == 0:
            return "消息发送成功"
        else:
            return f"发送失败: {result.get('msg', '未知错误')}"

    except Exception as e:
        return f"发送消息时发生错误: {str(e)}"
