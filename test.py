from ollama._client import Client
import ollama  # 导入 ollama 库

# 设置你要访问的服务器 IP 地址
ollama_host = "http://192.168.2.79:11434"  # 替换为你的 Ollama 服务器 IP 地址

# 创建一个新的 Client 实例
custom_client = Client(host=ollama_host)

# 动态赋值 ollama.generate 为 custom_client.generate 方法
ollama.generate = custom_client.generate

# 示例调用 ollama.generate（方法名保持不变）
response = ollama.generate(model="qwen2.5", prompt="Hello, how are you?")
print(response)
