import os
import requests
import json
import logging

logger = logging.getLogger(__name__)


def web_search(query: str) -> str:
    """
    联网搜索互联网上的最新信息，输入搜索关键词，返回搜索结果的摘要。
    当你需要查询最新资讯、技术文档、实时数据，或者自身知识无法回答的问题时调用这个工具。

    Args:
        query: 搜索关键词，必须是字符串

    Returns:
        搜索结果的文本摘要
    """
    logger.info(f"[web_search] 被调用，query='{query}'")

    api_key = os.getenv("WEBSEARCH_API_KEY")
    if not api_key:
        logger.error("[web_search] WEBSEARCH_API_KEY 未配置")
        return "错误：未配置 WEBSEARCH_API_KEY"

    logger.info(f"[web_search] API_KEY 前缀: {api_key[:20]}...")

    payload = {
        "messages": [{"role": "user", "content": query}],
        "stream": False,
        "model": "ernie-3.5-8k",
        "instruction": "##",
        "enable_corner_markers": True,
        "enable_deep_search": True,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    logger.info(f"[web_search] 请求 URL: https://qianfan.baidubce.com/v2/ai_search/chat/completions")
    logger.info(f"[web_search] 请求头: {{'Authorization': 'Bearer {api_key[:8]}...', 'Content-Type': 'application/json'}}")
    logger.info(f"[web_search] 请求体: {json.dumps(payload, ensure_ascii=False)[:200]}...")

    try:
        resp = requests.post(
            "https://qianfan.baidubce.com/v2/ai_search/chat/completions",
            headers=headers,
            json=payload,
            timeout=90
        )
        logger.info(f"[web_search] HTTP 响应状态码: {resp.status_code}")
        logger.info(f"[web_search] HTTP 响应头: {dict(resp.headers)}")

        if resp.status_code != 200:
            error_text = resp.text[:500]
            logger.error(f"[web_search] API 返回错误: {error_text}")
            return f"搜索API HTTP {resp.status_code}: {error_text}"

        data = resp.json()
        logger.info(f"[web_search] 响应 JSON 根字段: {list(data.keys())}")

        # 兼容两种返回格式
        result = data.get("result", "")
        if not result:
            choices = data.get("choices", [])
            if choices:
                result = choices[0].get("message", {}).get("content", "")
                logger.info(f"[web_search] 从 choices[0].message.content 提取结果，长度: {len(result)}")
            else:
                logger.warning(f"[web_search] choices 为空，完整响应: {json.dumps(data, ensure_ascii=False)[:500]}")
        else:
            logger.info(f"[web_search] 从 result 字段提取结果，长度: {len(result)}")

        if not result:
            logger.warning("[web_search] API 返回空结果")
            return f"搜索API返回空结果"

        logger.info(f"[web_search] 搜索成功，结果长度: {len(result)}")
        return f"🔍 搜索结果（{query}）：\n{result}"

    except requests.Timeout:
        logger.error("[web_search] 请求超时（30秒）")
        return "搜索API请求超时（30秒）"
    except Exception as e:
        logger.error(f"[web_search] 请求异常: {e}", exc_info=True)
        return f"搜索失败: {e}"