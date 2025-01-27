import subprocess

def get_running_ollama_models():
    """
    使用 `ollama ps` 命令获取当前已运行的模型
    :return: 一个包含运行模型名称的列表
    """
    try:
        # 执行 `ollama ps` 命令
        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True, check=True)

        # 解析命令输出
        running_models = []
        for line in result.stdout.splitlines():
            # 假设输出格式为： "MODEL_NAME     STATUS"
            if line.strip() and not line.lower().startswith('name') and not line.lower().startswith('status'):
                # 提取模型名称（按空格分隔的第一部分）
                model_name = line.split()[0]
                running_models.append(model_name)

        return running_models

    except subprocess.CalledProcessError as e:
        print(f"Error executing `ollama ps`: {e}")
        return []
    except FileNotFoundError:
        print("`ollama` command not found. Make sure it is installed and added to PATH.")
        return []

if __name__ == "__main__":
    models = get_running_ollama_models()
    if models:
        print(f"当前运行的模型: {', '.join(models)}")
    else:
        print("没有检测到运行中的模型。")
