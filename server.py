from pathlib import Path
import gradio as gr
from fastapi import FastAPI
import importlib.util
import uvicorn
import time
from sub_app import sub_app
import requests


BASE_DIR = Path(__file__).parent
DEMO_DIR = BASE_DIR / "demo"
VENV_PYTHON = BASE_DIR / ".venv" / "Scripts" / "python.exe"
OPENCODE_BASE = "http://127.0.0.1:4096"
_opencode_session_id = None
app = FastAPI()
app_sub = None

# ---------- 工具函数 ----------
def list_py_files():
    return [f.name for f in DEMO_DIR.glob("*.py")]

def list_files():
    files = []
    for p in DEMO_DIR.rglob("*"):
        if p.is_file():
            files.append(str(p.relative_to(DEMO_DIR)))
    return sorted(files)

def load_py_file(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
def read_pyfile_content(file_name):
    with open(DEMO_DIR / file_name, "r", encoding="utf-8") as f:
        return f.read()

def read_file_content(rel_path: str):
    path = (DEMO_DIR / rel_path).resolve()
    if not path.is_relative_to(DEMO_DIR):
        raise ValueError("非法路径")
    return path.read_text(encoding="utf-8", errors="ignore")


# ================== OpenCode Serve ==================
def get_opencode_session():
    global _opencode_session_id
    if _opencode_session_id is None:
        resp = requests.post(f"{OPENCODE_BASE}/session", timeout=10)
        resp.raise_for_status()
        _opencode_session_id = resp.json()["id"]
    return _opencode_session_id


def run_opencode(prompt: str):
    if not prompt.strip():
        return "❌ 请输入问题"

    sid = get_opencode_session()

    resp = requests.post(
        f"{OPENCODE_BASE}/session/{sid}/message",
        json={
            "parts": [
                {"type": "text", "text": prompt}
            ]
        },
        timeout=300,
    )
    resp.raise_for_status()

    data = resp.json()
    texts = [
        p["text"]
        for p in data.get("parts", [])
        if p.get("type") == "text"
    ]
    return "".join(texts).strip()




# ---------- private 页面 ----------
with gr.Blocks(title='FMTC-Test', fill_height=True) as demo_private:
    with gr.Row():
        with gr.Column(scale=1, min_width=150):
            gr.Label(value="Wangguanyu", container=False)
            btn_refresh = gr.Button("刷新", size="md")
            btn_edit = gr.Button("编辑", size="md")
            btn_render = gr.Button("渲染", size="md")
            file_dd = gr.Dropdown(container=False, choices=list_files())
        with gr.Column(scale=20, visible=True):
            # iframe = gr.HTML('<iframe src="/sub" style="width:100%; height:100%;"></iframe>')
            user_input = gr.Textbox(
                label="你的问题 / 指令",
                placeholder="例如：请解释这个文件的主要逻辑，或直接修改它",
                lines=3,
            )
            output = gr.Textbox(
                label="opencode 输出",
                lines=20,
                interactive=False,
            )

            btn_render.click(
                run_opencode,
                inputs=[user_input],
                outputs=output
            )
        with gr.Column(scale=20, visible=False) as ColEditor:
            with gr.Row():
                btn_edit_save = gr.Button(value="保存修改", size="md")
                btn_edit_exit = gr.Button(value="退出编辑", size="md")
            editor = gr.Textbox(container=False, interactive=True, lines=38, max_lines=38)


    def fun_refresh():
        return gr.update(choices=list_files())
    btn_refresh.click(fun_refresh, outputs=[file_dd])

    def fun_edit(file_in):
        content = read_file_content(file_in)
        return gr.update(visible=True), gr.update(value=content)
    btn_edit.click(fn=fun_edit, inputs=[file_dd], outputs=[ColEditor, editor])

    def fun_edit_save(file_in, content):
        with open(DEMO_DIR / file_in, "w", encoding="utf-8") as f:
            f.write(content)
    btn_edit_save.click(fn=fun_edit_save, inputs=[file_dd, editor])

    def fun_edit_exit():
        return gr.update(visible=False)
    btn_edit_exit.click(fn=fun_edit_exit, outputs=[ColEditor])


    def fun_render(selected_file):
        return gr.HTML(
            f'<iframe src="/sub?file={selected_file}&_t={time.time()}" '
            f'style="width:100%; height:90vh;"></iframe>'
        )
    # btn_render.click(fn=fun_render, inputs=[file_dd], outputs=[iframe])

# ---------- public 页面 ----------
with gr.Blocks(title='FMTC-Test', fill_height=True) as demo_public:
    list_public = ['Calendar2026.py']
    with gr.Row():
        with gr.Column(scale=1, min_width=150):
            gr.Label(value="Test", container=False)
            btn_render = gr.Button("渲染", size="md")
            file_dd = gr.Dropdown(container=False, choices=list_public)
        with gr.Column(scale=20, visible=True):
            iframe = gr.HTML(
                f'<iframe src="/sub?file={list_public[0]}&_t={time.time()}" '
                f'style="width:100%; height:90vh;"></iframe>'
            )

    def fun_render(selected_file):
        return gr.HTML(
            f'<iframe src="/sub?file={selected_file}>&_t={time.time()}" '
            f'style="width:100%; height:90vh;"></iframe>'
        )
    btn_render.click(fn=fun_render, inputs=[file_dd], outputs=[iframe]
    )

gr.routes.mount_gradio_app(app, demo_public, path="/public", footer_links=[], theme=gr.themes.Glass())
gr.routes.mount_gradio_app(app, demo_private, path="/private", footer_links=[], theme=gr.themes.Glass())
gr.routes.mount_gradio_app(app, sub_app, path="/sub", footer_links=[], theme=gr.themes.Glass())

# ---------- 启动 ----------
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=7778, reload=False, reload_dirs=["private"])
