"""
Agent 配置归一化与校验工具（A 档功能）。

负责把前端传入或 Agent Builder 生成的 memory_config / planning_config / validation_config
三类嵌套 JSON 做严格校验与规范化：
- 非法 strategy/mode 直接抛 ValueError
- 数值边界校验（window_size>=1, max_retries 0..5 等）
- 自动补默认值，过滤未知字段，避免脏数据落库

所有归一化函数都遵循一个统一约定：
- 输入为 None / 空 dict → 返回 None（表示该 Agent 走默认策略）
- 输入合法 → 返回标准化后的 dict
- 输入非法 → raise ValueError("可读的中文错误信息")
"""
from __future__ import annotations

from typing import Any, Optional

# ============== 枚举白名单 ==============
MEMORY_STRATEGIES = {"none", "sliding_window", "summary"}
PLANNING_MODES = {"direct", "react", "plan_execute"}
VALIDATION_STRATEGIES = {"none", "rules", "llm_judge"}
VALIDATION_RULE_TYPES = {"regex", "json_schema"}


def _require_dict(value: Any, field_name: str) -> Optional[dict]:
    """统一处理 None / 空 dict / 非 dict 三种情况。"""
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} 必须是 JSON 对象 (dict)，实际收到: {type(value).__name__}")
    # 空 dict 视为 None，避免持久化空对象
    if not value:
        return None
    return value


def normalize_memory_config(raw: Any) -> Optional[dict]:
    """
    校验并规范化 memory_config。

    合法形态：
      { "strategy": "none" }
      { "strategy": "sliding_window", "window_size": 10 }
      { "strategy": "summary", "summary_threshold": 4000, "summary_prompt": "..." }
    """
    data = _require_dict(raw, "memory_config")
    if data is None:
        return None

    strategy = str(data.get("strategy", "")).strip().lower()
    if strategy not in MEMORY_STRATEGIES:
        raise ValueError(
            f"memory_config.strategy 非法: '{strategy}'，可选值: {sorted(MEMORY_STRATEGIES)}"
        )

    result: dict = {"strategy": strategy}

    if strategy == "sliding_window":
        try:
            window_size = int(data.get("window_size", 10))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"memory_config.window_size 必须是整数: {exc}") from exc
        if window_size < 1 or window_size > 200:
            raise ValueError(f"memory_config.window_size 必须在 1..200 之间，实际: {window_size}")
        result["window_size"] = window_size

    elif strategy == "summary":
        try:
            threshold = int(data.get("summary_threshold", 4000))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"memory_config.summary_threshold 必须是整数: {exc}") from exc
        if threshold < 200 or threshold > 200000:
            raise ValueError(
                f"memory_config.summary_threshold 必须在 200..200000 之间，实际: {threshold}"
            )
        result["summary_threshold"] = threshold
        prompt = str(data.get("summary_prompt") or "").strip()
        if prompt:
            if len(prompt) > 5000:
                raise ValueError("memory_config.summary_prompt 长度不能超过 5000 字符")
            result["summary_prompt"] = prompt

    return result


def normalize_planning_config(raw: Any) -> Optional[dict]:
    """
    校验并规范化 planning_config。

    合法形态：
      { "mode": "direct" }
      { "mode": "react" }
      { "mode": "plan_execute", "steps_template": "...", "require_confirmation_for_complex_tasks": true }
    """
    data = _require_dict(raw, "planning_config")
    if data is None:
        return None

    mode = str(data.get("mode", "")).strip().lower()
    if mode not in PLANNING_MODES:
        raise ValueError(
            f"planning_config.mode 非法: '{mode}'，可选值: {sorted(PLANNING_MODES)}"
        )

    result: dict = {"mode": mode}

    if mode == "plan_execute":
        steps_template = data.get("steps_template")
        if steps_template:
            steps_template = str(steps_template).strip()
            if len(steps_template) > 5000:
                raise ValueError("planning_config.steps_template 长度不能超过 5000 字符")
            result["steps_template"] = steps_template

    if "require_confirmation_for_complex_tasks" in data:
        result["require_confirmation_for_complex_tasks"] = bool(
            data["require_confirmation_for_complex_tasks"]
        )

    return result


def _normalize_validation_rule(rule: Any, idx: int) -> dict:
    """校验单条 validation rule。"""
    if not isinstance(rule, dict):
        raise ValueError(f"validation_config.rules[{idx}] 必须是 dict")
    rule_type = str(rule.get("type", "")).strip().lower()
    if rule_type not in VALIDATION_RULE_TYPES:
        raise ValueError(
            f"validation_config.rules[{idx}].type 非法: '{rule_type}'，可选值: {sorted(VALIDATION_RULE_TYPES)}"
        )
    result: dict = {"type": rule_type}
    if rule_type == "regex":
        pattern = str(rule.get("pattern") or "").strip()
        if not pattern:
            raise ValueError(f"validation_config.rules[{idx}] regex 规则必须提供 pattern")
        # 简单尝试编译一次，提前抛错
        import re
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"validation_config.rules[{idx}].pattern 正则非法: {exc}") from exc
        result["pattern"] = pattern
    elif rule_type == "json_schema":
        schema = rule.get("schema")
        if not isinstance(schema, dict):
            raise ValueError(f"validation_config.rules[{idx}] json_schema 规则必须提供 schema 对象")
        result["schema"] = schema
    if rule.get("message"):
        result["message"] = str(rule["message"]).strip()
    return result


def normalize_validation_config(raw: Any) -> Optional[dict]:
    """
    校验并规范化 validation_config。

    合法形态：
      { "strategy": "none" }
      { "strategy": "rules", "rules": [...], "max_retries": 1 }
      { "strategy": "llm_judge", "judge_prompt": "...", "max_retries": 1 }
    """
    data = _require_dict(raw, "validation_config")
    if data is None:
        return None

    strategy = str(data.get("strategy", "")).strip().lower()
    if strategy not in VALIDATION_STRATEGIES:
        raise ValueError(
            f"validation_config.strategy 非法: '{strategy}'，可选值: {sorted(VALIDATION_STRATEGIES)}"
        )

    result: dict = {"strategy": strategy}

    # max_retries 公共字段（仅在非 none 时有意义，但 none 时容忍）
    if "max_retries" in data:
        try:
            max_retries = int(data["max_retries"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"validation_config.max_retries 必须是整数: {exc}") from exc
        if max_retries < 0 or max_retries > 5:
            raise ValueError(
                f"validation_config.max_retries 必须在 0..5 之间，实际: {max_retries}"
            )
        result["max_retries"] = max_retries

    if strategy == "rules":
        rules = data.get("rules") or []
        if not isinstance(rules, list):
            raise ValueError("validation_config.rules 必须是数组")
        if not rules:
            raise ValueError("validation_config.strategy=rules 时必须提供至少一条 rules")
        result["rules"] = [_normalize_validation_rule(r, i) for i, r in enumerate(rules)]

    elif strategy == "llm_judge":
        judge_prompt = str(data.get("judge_prompt") or "").strip()
        if not judge_prompt:
            raise ValueError("validation_config.strategy=llm_judge 时必须提供 judge_prompt")
        if len(judge_prompt) > 5000:
            raise ValueError("validation_config.judge_prompt 长度不能超过 5000 字符")
        result["judge_prompt"] = judge_prompt

    return result
