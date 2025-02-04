import ollama
from py2neo import Graph

# Ollama 和 Neo4j 的参数
# OLLAMA_ADDRESS = "202.118.11.9"
OLLAMA_ADDRESS = "192.168.2.79"# 地址
OLLAMA_PORT = "11434"            # 端口
OLLAMA_HOST = f"http://{OLLAMA_ADDRESS}:{OLLAMA_PORT}"  # 拼接完整 URL
NEO4J_HOST = "bolt://192.168.2.79:7687"
NEO4J_AUTH = ("neo4j", "neo4jneo4j")
NEO4J_NAME = "neo4j"


def get_ollama_client():
    """
    返回一个 Ollama 客户端
    """
    # 创建并返回自定义的 Ollama 客户端
    custom_client = ollama.Client(host=OLLAMA_HOST)

    # 将 ollama.generate 和 ollama.chat 分别指向 custom_client 的方法
    ollama.generate = custom_client.generate
    ollama.chat = custom_client.chat

    return custom_client

def get_neo4j_client():
    """
    返回一个 Neo4j 客户端
    """
    return Graph(
        NEO4J_HOST,
        auth=NEO4J_AUTH,
        name=NEO4J_NAME
    )
