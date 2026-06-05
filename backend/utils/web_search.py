import os
import requests
from typing import List, Dict, Any

def web_search(query: str) -> str:
    """
    联网搜索互联网上的最新信息，输入搜索关键词，返回搜索结果的摘要。
    当你需要查询最新资讯、技术文档、实时数据，或者自身知识无法回答的问题时调用这个工具。
    
    Args:
        query: 搜索关键词，必须是字符串
        
    Returns:
        搜索结果的文本摘要
    """
    # 使用百度的联网搜索API，读取.env里配置的WEBSEARCH_API_KEY
    api_key = os.getenv("WEBSEARCH_API_KEY")
    if not api_key:
        return "错误：未配置WEBSEARCH_API_KEY环境变量，无法执行联网搜索，请先在.env中配置百度搜索API密钥"
    
    try:
        # 调用百度的搜索API（根据你实际用的百度API地址调整，这里用通用的百度搜索接口格式）
        response = requests.get(
            "https://api.baidu.com/search",  # 替换为你实际的百度搜索API地址
            params={"q": query, "apikey": api_key, "limit": 3}
        )
        if response.status_code == 200:
            data = response.json()
            # 适配百度API的返回格式，提取前3个搜索结果
            results = data.get("results", [])[:3]
            if not results:
                return f"未找到与'{query}'相关的有效搜索结果"
            summary = f"🔍 联网搜索'{query}'的结果：\n"
            for i, res in enumerate(results, 1):
                title = res.get('title', '无标题')
                snippet = res.get('summary', '无摘要')
                link = res.get('url', '#')
                summary += f"{i}. {title}\n   📝 {snippet}\n   🔗 {link}\n"
            return summary
        else:
            return f"搜索API调用失败，HTTP状态码: {response.status_code}，响应: {response.text[:200]}"
    except Exception as e:
        return f"联网搜索执行失败，异常信息: {str(e)}"