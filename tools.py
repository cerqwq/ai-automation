"""
AI Automation - AI自动化工具
支持工作流自动化、任务调度、RPA
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIAutomationTools:
    """
    AI自动化工具
    支持：工作流、调度、RPA
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def design_workflow(self, process: str, triggers: List[str]) -> Dict:
        """设计工作流"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        triggers_text = ", ".join(triggers)

        prompt = f"""请设计以下流程的自动化工作流：

流程：{process}
触发条件：{triggers_text}

请返回JSON格式：
{{
    "workflow_name": "工作流名称",
    "steps": [
        {{"step": "步骤", "action": "动作", "condition": "条件", "tool": "工具"}}
    ],
    "error_handling": "错误处理",
    "monitoring": "监控建议"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"workflow": content}

    def generate_n8n_workflow(self, description: str) -> str:
        """生成n8n工作流"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请根据以下描述生成n8n工作流JSON：

{description}

请返回完整的n8n工作流JSON："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def generate_zapier_integration(self, app1: str, app2: str, trigger: str) -> Dict:
        """生成Zapier集成"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请设计{app1}和{app2}的Zapier集成：

触发条件：{trigger}

请返回JSON格式：
{{
    "zap_name": "Zap名称",
    "trigger_app": "触发应用",
    "trigger_event": "触发事件",
    "actions": [
        {{"app": "应用", "action": "动作", "mapping": "字段映射"}}
    ],
    "filters": ["过滤条件"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"zapier": content}

    def generate_cron_job(self, task: str, schedule: str) -> str:
        """生成Cron任务"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为以下任务生成Cron配置和脚本：

任务：{task}
调度：{schedule}

请返回完整的crontab配置和脚本："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content

    def generate_rpa_script(self, process: str, tool: str = "python") -> str:
        """生成RPA脚本"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为以下流程生成{tool} RPA脚本：

流程：{process}

要求：
1. 完整可运行
2. 错误处理
3. 日志记录"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def optimize_workflow(self, current_workflow: str, metrics: Dict) -> Dict:
        """优化工作流"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        metrics_text = json.dumps(metrics, ensure_ascii=False)

        prompt = f"""请优化以下工作流：

当前工作流：{current_workflow[:500]}
性能指标：{metrics_text}

请返回JSON格式：
{{
    "bottlenecks": ["瓶颈"],
    "optimizations": [
        {{"area": "领域", "change": "变更", "expected_improvement": "预期提升"}}
    ],
    "automated_tasks": ["可自动化的任务"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"optimization": content}


def create_tools(**kwargs) -> AIAutomationTools:
    """创建自动化工具"""
    return AIAutomationTools(**kwargs)


if __name__ == "__main__":
    tools = create_tools()

    print("AI Automation Tools")
    print()

    # 测试
    workflow = tools.design_workflow("新员工入职", ["HR提交申请", "IT创建账号"])
    print(json.dumps(workflow, ensure_ascii=False, indent=2))
