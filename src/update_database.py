import argparse
# pathlib 替代了os.path
from pathlib import Path
import shutil
#【搬运工】：专门负责读取一个文件夹里所有的PDF文件
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
#【切片刀】：最核心的工具，它能根据句号、换行，智能地把长文章切成一小块一小块
from langchain_text_splitters import RecursiveCharacterTextSplitter
#【纸片】：定义了“知识碎片”的长相，每一个碎片都包含“文字内容”和“元数据”
from langchain.schema.document import Document
#【仓库】：这是向量数据库 Chroma 的Python接口，它负责把切好的碎片存入本地磁盘
from langchain_community.vectorstores.chroma import Chroma
#【大脑核心】：引入 model_and_embedding.py 中写的函数和配置
from model_and_embedding import get_embedding_function, EMBEDDING_NAME

# --- 路径配置 --- 
# os.path 的写法
""" 
os.path可以让代码在不同操作系统上都能正确处理文件路径(比如Windows和Linux的路径分隔符不同)
DATASET_PATH = os.path.join("data", f"chroma_{EMBEDDING_NAME}")
DOCUMENT_PATH = os.path.join("data", "documents") 
"""

# pathlib 的写法
DATASET_PATH = Path("data") / f"chroma_{EMBEDDING_NAME}"
DOCUMENT_PATH = Path("data") / "documents"

def main():
    parser = argparse.ArgumentParser() # 听候终端上输入的指令
    parser.add_argument("--reset", action="store_true",
help="是否重新构建数据库, 默认是False") 
    # -- 表示可选参数, 定义了按钮的名字(reset), 没有--表示位置参数(必须填)
    # action 表示命令行出现了arts.reset就把 args.reset设为True,(默认为False) 
    # help 表示 --reset 的说明书
    args = parser.parse_args() # 根据之前定义的规则, 把这串文本“翻译”成一个Python对象

    if args.reset:
        clear_database()

    # 1. 加载文档
    documents = load_documents()
    # 2. 切分文档
    chunks = split_documents(documents)
    # 3. 存入数据库
    store_to_chroma(chunks)

def clear_database():
    """删除旧的数据库文件夹，清空之前的知识库"""
    if DATASET_PATH.exists():
        print(f"✨ 正在清理旧数据库：{DATASET_PATH}")
        shutil.rmtree(DATASET_PATH) # 删除整个文件夹
