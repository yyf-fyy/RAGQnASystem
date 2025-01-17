import ollama

# 初始化 Ollama 客户端
OLLAMA_HOST = "http://202.118.11.9:11434"  # 替换为你的 Ollama 服务地址
client = ollama.Client(host=OLLAMA_HOST)

# 调用 `models()` 方法获取已部署的模型列表
try:
    models = client.models()  # 获取模型列表
    print("已部署的模型：")
    for model in models:
        print(f"- {model}")
except Exception as e:
    print(f"获取模型列表时出错：{e}")
