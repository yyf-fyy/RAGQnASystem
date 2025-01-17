import ollama
from py2neo import Graph

# Ollama 和 Neo4j 的参数
# OLLAMA_ADDRESS = "202.118.11.9"
OLLAMA_ADDRESS = "localhost"# 地址
OLLAMA_PORT = "11434"            # 端口
OLLAMA_HOST = f"http://{OLLAMA_ADDRESS}:{OLLAMA_PORT}"  # 拼接完整 URL
NEO4J_HOST = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "neo4jneo4j")
NEO4J_NAME = "neo4j"

def get_ollama_client():
    """
    返回一个 Ollama 客户端
    """
    return ollama.Client(host=OLLAMA_HOST)

def get_neo4j_client():
    """
    返回一个 Neo4j 客户端
    """
    return Graph(
        NEO4J_HOST,
        auth=NEO4J_AUTH,
        name=NEO4J_NAME
    )
