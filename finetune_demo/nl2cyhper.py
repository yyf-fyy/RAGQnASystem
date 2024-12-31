import ollama
import os
from zhipuai import ZhipuAI
from tqdm import tqdm
import json
import time
os.chdir(os.path.dirname(__file__))#vscode要用
import pandas as pd
OLLAMA_HOST = "http://202.118.19.61"
OLLAMA_PORT = "11434"
OLLAMA_MODEL = "qwen:32b"

# 全局 Ollama 客户端
client = ollama.Client(host=f"{OLLAMA_HOST}:{OLLAMA_PORT}")
def append_data_to_json(data, filename):
    with open(filename, 'a', encoding='utf-8') as file:  # 使用UTF-8编码打开文件
        json_data = json.dumps(data, ensure_ascii=False)  # 将字典转换为JSON字符串，保持中文等字符的正确显示
        file.write(json_data + ',\n')  # 写入JSON数据，并在末尾添加逗号和换行符
client = ZhipuAI(api_key="d0e5b641e4606dd20e98906b231bc59d.zFeDxjbHDl5V6KlY") # 填写您自己的APIKey


# 读取CSV文件
df = pd.read_csv('questions.csv', delimiter=',', on_bad_lines='skip')

# 将'content'列的数据保存到列表中
content_list = df['content'].tolist()
for i,content in enumerate(tqdm(content_list[5000:])):
    prompt = f"""你是一个判断机器人，下面用户将会输入一个问题，你需要判断这是不是一个和具体疾病有关的问题。如果是，你就回答“是”，否则回答“否”。不要输出多余的解释。
    问题：{content}
    请注意 ，如果问题中没有出现具体的疾病特征，一律回答“否”。如果只是询问某种药物(和具体疾病没关系)，回答“否”。
    """
    response = ollama.generate(model='qwen:32b', prompt=prompt)['response']
    
    if response!='是':
        continue

    prompt = f"""提示:目前，我的图数据库中有8类实体：疾病、药品、药品商、疾病症状、食物、检查项目、治疗方法、科目。在这里面，“疾病”这个实体有7个属性：名称、治愈概率、治疗周期、疾病易感人群、疾病病因、疾病简介、预防措施；其余实体均只有名称这个属性。在实体之间，具有8个关系：疾病使用药品、治疗的方法、疾病宜吃食物、疾病忌吃食物、疾病的症状、疾病所需检查、疾病所属科目、疾病并发疾病。其中“疾病使用药品”是“疾病”和“药品”之间的关系，“治疗的方法”是“疾病”和“治疗方法”之间的关系，“疾病宜吃食物”是“疾病”和“食物”之间的关系，“疾病忌吃食物”是“疾病”和“食物”之间的关系，“疾病的症状”是“疾病”和“疾病症状”之间的关系，“疾病所需检查”是“疾病”和“检查项目”之间的关系，“疾病所属科目”是“疾病”和“科目”之间的关系，“疾病并发疾病”是“疾病”和“疾病”之间的关系。
现在，你是一个机器人医生，用户对你输入问题，你需要精准的理解问题的内容，根据其含义构建Neo4j数据库的查询语句，多条查询语句请用逗号分割。在输出查询后，请简要输出你这样生成查询语句的原因。

请注意，你的查询语句只限于两个操作：1.查询疾病的属性，你需要提供疾病具体名称和属性名。2.查询疾病与其他实体之间的关系，你需要提供疾病具体名称、关系名称、实体类别名。为了简化输出，你输出查询语句格式的应为：对于类型1的查询，输出“1 疾病名称 属性”；对于类型2的查询，输出“2 疾病名称 关系 实体类别”。如果有多个查询，每个查询之间用中文逗号隔开。

下面是一些示例：

示例1:
问题:皮肤赘生物，传染性软疣到底怎么治疗呢？？
查询语句:1 皮肤赘生物  疾病简介,1 传染性软疣 疾病简介,2 皮肤赘生物 治疗的方法 治疗方法,2 传染性软疣 治疗的方法 治疗方法
解释:首先需要向用户介绍这两种病，然后依次告诉他们治疗的方法。

示例2:第一天白天拉了4-5次后来每天拉2-3次
查询语句:1 急性腹泻 疾病简介,2 急性腹泻 疾病使用药品 药品,2 急性腹泻 治疗的方法 治疗方法,2 急性腹泻 疾病宜吃食物 食物
解释:根据症状判断出这是急性腹泻，为用户介绍一下急性腹泻，然后告诉他要吃什么药，怎么治疗，吃什么食物。

示例3:得了癌症就死定了吗？
查询语句:1 癌症 疾病简介,1 癌症 治愈概率,2 癌症 治疗的方法 治疗方法
解释:用户问会不会死，其实他最想知道的是治愈概率。因此可以给用户介绍一下癌症，然后告诉他治愈概率和治疗方法。

示例4:有8-9年的灰指甲了过段时间会好痒最开始是一个，慢慢的两个，三个，期间在修脚房治疗过但没见效果，希望能帮帮我，谢谢
查询语句:1 灰指甲 疾病简介,2 灰指甲 治疗的方法 治疗方法
解释:用户显然想知道灰指甲的治疗方法。

示例5:我有胃炎和乙肝，平时我应该吃什么好，不能吃什么？
查询语句:2 胃炎 疾病宜吃食物 食物,2 乙肝 疾病宜吃食物 食物,2 胃炎 疾病忌吃食物 食物,2 乙肝 疾病忌吃食物 食物
解释:按照用户的需求，为他查找胃炎和乙肝的宜吃与忌吃食物。

示例6:就感冒一次，每次都会喉咙发炎，感冒，大便干，食欲不振，吃饭少，睡眠易醒，爱哭闹，偶尔带发烧，体重22kg，身高127cm，体型瘦高
查询语句:1 感冒 疾病简介,1 咳嗽 疾病简介,2 感冒 治疗的方法 治疗方法,2 咳嗽 治疗的方法 治疗方法
解释:用户主要想问感冒和感冒两种病怎么治好。

下面请你根据示例，回答用户的问题。
问题:{content}
查询语句:
解释:
    """
    try:
        response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": prompt},
        ],
        )

        data = {
            "question":content,
            "answer":response.choices[0].message.content,
        }
        append_data_to_json(data,'nl2cyhper_data.txt')
    except:
        print(f'失败{i}')
        time.sleep(10)
        with open('log.txt', 'a', encoding='utf-8') as file:  # 使用UTF-8编码打开文件
            file.write(f'失败{i}\n')  # 写入JSON数据，并在末尾添加逗号和换行符

