from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class TaskSpec(BaseModel):
    step_id: str
    agent_id: str
    prompt: str                # 派发任务的具体指令
    context: Dict[str, Any] = {}   # 从黑板注入的上下文
    expectations: Dict[str, str] = {}  # pass, standard, excellent
    output_format: str = "自然语言"
    max_retries: int = 1
    dependencies: list[str] = []     # 前置步骤的 step_id

class TaskResult(BaseModel):
    step_id: str
    status: str               # success / partial / failed
    result: str
    findings: str = ""        # 写入黑板的发现
    outputs: Dict[str, Any] = {}