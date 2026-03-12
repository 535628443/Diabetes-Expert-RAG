import os
import sys
import subprocess

def main():
    """
    启动糖尿病AI医学助手的入口脚本。
    使用 sys.executable 确保用当前虚拟环境的 Python 和 Streamlit。
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ui_script = os.path.join(current_dir, "src", "ui.py")

    if not os.path.exists(ui_script):
        print(f"错误: 找不到启动文件 {ui_script}")
        sys.exit(1)

    print("🚀 正在启动糖尿病AI医学助手...")
    print(f"   Python: {sys.executable}")
    print(f"   UI文件: {ui_script}")

    # 关键：用 sys.executable -m streamlit，确保用 venv 内的 streamlit
    cmd = [sys.executable, "-m", "streamlit", "run", ui_script,
           "--server.port", "8501"]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 已停止服务。")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

