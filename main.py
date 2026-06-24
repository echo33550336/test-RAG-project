# AI工具使用标注（2026大赛要求）
# 1. DeepSeek：立项、方向确认、分工优化
# 2. 豆包：方案整理、规范文档
# 3. Kimi K2.5：代码生成、Debug、优化
# 4. Trae：前端UI样式微调
# AI仅辅助开发，核心设计与整合均为团队原创

"""
应用入口兼容层：实际 FastAPI 定义在 Backend.app.main。

启动：
  uvicorn Backend.main:app --host 0.0.0.0 --port 5000
"""

from Backend.app.main import app  # noqa: F401

__all__ = ["app"]
