import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取API Key
api_key = os.getenv("ZHIPUAI_API_KEY")
client = ZhipuAI(api_key=api_key)

response = client.chat.completions.create(
    model="glm-4-flash",  # 免费模型
    messages=[
        {"role": "user", "content": "你好，请用一句话介绍一下你自己"}
    ],
)

print(response.choices[0].message.content)