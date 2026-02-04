import gradio as gr
import importlib.util
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
DEMO_DIR = BASE_DIR / "demo"


def load_module(file_name: str):
    path = DEMO_DIR / file_name
    mod_name = f"demo_{path.stem}"

    # 🔥 热重载
    sys.modules.pop(mod_name, None)

    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


with gr.Blocks() as sub_app:

    @gr.render()
    def render(request: gr.Request):
        file_name = request.query_params.get("file")

        if not file_name:
            gr.Markdown("# 请点击左侧渲染按钮")
            return

        mod = load_module(file_name)
        mod.build()   # ✅ 这里动态创建 UI
