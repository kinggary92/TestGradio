from pathlib import Path
import gradio as gr
from fastapi import FastAPI
import importlib.util
import uvicorn
import time
from sub_app import sub_app

BASE_DIR = Path(__file__).parent
INSTANCE_DIR = BASE_DIR / "instance"
app = FastAPI()
app_sub = None

# ---------- 工具函数 ----------
def list_py_files():
    return [f.name for f in INSTANCE_DIR.glob("*.py")]
def load_py_file(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
def read_file_content(file_name):
    with open(INSTANCE_DIR / file_name, "r", encoding="utf-8") as f:
        return f.read()


# ---------- 主页面 Gradio ----------
with gr.Blocks(title='GrWinterBear', fill_height=True) as demo:
    with gr.Row():
        with gr.Column(scale=1, min_width=150):
            gr.Label(value="WinterBear", container=False)
            btn_refresh = gr.Button("刷新", size="md")
            btn_edit = gr.Button("编辑", size="md")
            btn_render = gr.Button("渲染", size="md")
            file_dd = gr.Dropdown(container=False, choices=list_py_files())
        with gr.Column(scale=20, visible=True) as ColRender:
            iframe = gr.HTML('<iframe src="/sub" style="width:100%; height:90vh; border:1px solid #ccc;"></iframe>')
        with gr.Column(scale=20, visible=False) as ColEditor:
            with gr.Row():
                btn_edit_save = gr.Button(value="保存修改", size="md")
                btn_edit_exit = gr.Button(value="退出编辑", size="md")
            editor = gr.Code(container=False, language="python", interactive=True, lines=38, max_lines=38)


    def fun_refresh():
        return gr.update(choices=list_py_files())
    btn_refresh.click(fun_refresh, outputs=[file_dd])

    def fun_edit(file_in):
        content = read_file_content(file_in)
        return gr.update(visible=True), gr.update(value=content)
    btn_edit.click(fn=fun_edit, inputs=[file_dd], outputs=[ColEditor, editor])

    def fun_edit_save(file_in, content):
        with open(INSTANCE_DIR / file_in, "w", encoding="utf-8") as f:
            f.write(content)
    btn_edit_save.click(fn=fun_edit_save, inputs=[file_dd, editor])

    def fun_edit_exit():
        return gr.update(visible=False)
    btn_edit_exit.click(fn=fun_edit_exit, outputs=[ColEditor])


    def fun_render(selected_file):
        return gr.HTML(
            f'<iframe src="/sub?file={selected_file}&_t={time.time()}" '
            f'style="width:100%; height:90vh; border:1px solid #ccc;"></iframe>'
        )
    btn_render.click(fn=fun_render, inputs=[file_dd], outputs=[iframe]
    )



gr.routes.mount_gradio_app(app, demo, path="/host", footer_links=[], theme=gr.themes.Glass())
gr.routes.mount_gradio_app(app, sub_app, path="/sub", footer_links=[], theme=gr.themes.Glass())

# ---------- 启动 ----------
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=7778, reload=True, reload_dirs=["instance"])
