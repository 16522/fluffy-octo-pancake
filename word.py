from datetime import datetime
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
import os
import openai
from dotenv import load_dotenv
import subprocess

# 加载环境变量
load_dotenv()

# Azure OpenAI 配置
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# 配置 openai 包以使用 Azure 的终结点和密钥
openai.api_type = "azure"
openai.api_base = azure_api_endpoint
openai.api_version = azure_api_version
openai.api_key = azure_api_key

# 配置 Azure ChatOpenAI
llm = AzureChatOpenAI(
    deployment_name="gpt-4o",
    model_name="o1-preview",
    api_version="2024-09-01-preview"
)

# 修改后的系统提示，要求生成中文释义和英文音标，并将音标放在单词和中文释义之间
system_prompt = r"""
You are an assistant that generates English vocabulary words based on a root word.
Your task is to create a Manim animation that displays the root word and its related words along with their meanings in Chinese and their English pronunciations (IPA).

# Rules
1. Generate at least 6 words related to the root word, each with a short definition in Chinese.
2. Include the English pronunciation (IPA) for each word and display it **between** the word and its Chinese definition, enclosed in square brackets [].
3. The root word should be displayed first, at the **center** of the animation with font_size=36.
4. Related words should be arranged **in a circle around the root word** with font_size=24. These related words should **appear one after another** with a delay, so that each word is displayed one by one in sequence.
5. The IPA pronunciation should be placed **between** the word and its definition in square brackets [].
6. The meanings should be displayed below each word with font_size=16.
7. Highlight both the root word and the root part within each related word in **orange color**.
8. Use SimSun as the font for all text.
9. Ensure that all text and animations are clear and non-overlapping.
10. Draw **thin arrows** from the center (root word) to each related word, making the arrows appear finer and more elegant. The arrows should have a **smaller triangle head** and a **narrower line** to appear more subtle and refined.
11. The arrows should appear in sequence as each related word appears, pointing from the root word to the current word being displayed.
12. **Ensure that related words appear one after another** with a slight delay between each appearance. This will allow words to be presented in a sequence without overlapping. Ensure that each word is spaced far enough apart to avoid collision, and adjust the positions dynamically to avoid overlap.
13. The root word should appear **first**, followed by the related words in a **sequential manner**, one at a time. Each word should appear in a **non-overlapping manner**, with appropriate adjustments to their placement.
14. **Ensure arrows and words are evenly distributed**, and the arrows should not overlap with any words or other elements.
15. **Make the arrows thinner overall**, with a smaller triangle at the tip, ensuring they are not too bold or overpowering, allowing the words to stand out.
16. **Ensure that the length of each arrow is smaller than the distance from the root word to the nearest point** between the English word, IPA, or Chinese definition of each related word. The arrows should not exceed the shortest distance from the root word to the nearest of these elements to avoid overlap or clutter.


"""

prompt_knowledge = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user",
     "Generate a Manim script to display words related to the root word: {input}. Each word must include its definition in Chinese and the IPA pronunciation.")
])

output_parser = StrOutputParser()

# 生成代码链
chain = prompt_knowledge | llm | output_parser

# 文件路径配置
file_path = "/Users/qinlishan/project/GenerateManimCode/"
file_name = "manim_generated.py"
output_directory = "./media/"

# 清理生成的代码
def clean_generated_code(raw_code):
    """
    清理生成的代码，只保留有效的 Python 代码部分。
    """
    if "```python" in raw_code:
        raw_code = raw_code.split("```python")[1]  # 提取代码部分
    if "```" in raw_code:
        raw_code = raw_code.split("```")[0]  # 去掉结尾的 ```
    return raw_code.strip()


# Manim 脚本运行函数
def run_manim_script(script_path, scene_name):
    try:
        # 生成输出视频的文件名
        output = datetime.now().strftime("%H%M%S") + '.mp4'
        command = ['python', '-m', 'manim', script_path, scene_name, '-o', output, '--media_dir', output_directory]
        print("Running command:", " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True)

        # 输出脚本的标准输出和错误
        if result.returncode == 0:
            print("Manim script executed successfully")
            print("Standard output:", result.stdout)
            video_path = os.path.join(output_directory, script_path.replace(".py", ""), output)
            return video_path  # 返回生成的视频路径
        else:
            print("Manim script execution failed")
            print("Standard error:", result.stderr)
            return None  # 表示未成功生成视频
    except Exception as e:
        print(f"An error occurred while trying to run the Manim script: {str(e)}")
        return None


# 主函数
def generate_and_run_manim(root_word):
    # 调用生成代码链
    raw_code = chain.invoke({"input": root_word})
    print("Raw Generated Code:\n", raw_code)

    # 清理生成的代码
    clean_code = clean_generated_code(raw_code)

    # 保存代码到文件
    script_path = os.path.join(file_path, file_name)
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(clean_code)

    # 运行 Manim 脚本
    video_path = run_manim_script(script_path, "BioRelatedWords")
    if video_path:
        print(f"Video generated at: {video_path}")
    else:
        print("Failed to generate video. Retrying...")
        generate_and_run_manim(root_word)  # 递归重试


# 示例输入
root_word = input("请输入词根: ").strip()  # 用户输入词根
generate_and_run_manim(root_word)
