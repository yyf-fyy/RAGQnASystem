import ollama

def test_connection():
    host = "202.118.19.61"
    port = "11434"
    client = ollama.Client(host=f"http://{host}:{port}")
    for i in range(100):  # 测试 5 次
        try:
            response = client.chat(
                model="qwen2.5:32b",
                messages=[{"role": "user", "content": "测试连接是否正常"}],
                options={"temperature": 0, "response_format": "json_object"}
            )
            print(f"第 {i + 1} 次请求成功: {response['message']['content']}")
        except Exception as e:
            print(f"第 {i + 1} 次请求失败: {e}")

test_connection()
