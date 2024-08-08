from openai import OpenAI
import os
from config.settings import settings

if settings.llm_enable_proxy:
    os.environ["http_proxy"] = f"http://{settings.proxy_host}:{settings.proxy_port}"
    os.environ["https_proxy"] = f"http://{settings.proxy_host}:{settings.proxy_port}"


class Prompt:
    specify_role_prompt = """
        假定你是个数据分析与提取的专家，并且能通过网页的源码来分析网页所呈现的内容,现在请遵循以下指令(instruction)来分析网页内容:
    """
    instruction_prompt = """
        instruction:
        - 在提取xpath时候不要使用标签+数字定位,只使用class和id属性来定位
    """
    ins_analyze_website_themes_prompt = "- 请分析网页的主题,并以json类型数据返回.你只能从以下列表中选择键(key)和值(value). key:sections ,value:['main_text','table_of_contents']"
    ins_extract_main_text_prompt = "- 如果这是小说的正文, 请提取出正文所在的最短的不重复xpath路径, key为: xpath_of_main_text"
    ins_extract_mt_next_page_prompt = "- 如果这是小说的正文,请提取出指向翻页按钮链接的最短的不会重复xpath路径, key为: xpath_of_main_text_next"
    ins_extract_table_of_contents_prompt = "- 如果这是小说的目录, 请提取出目录所在的最短的不重复xpath路径,注意只要主目录,不要提取最新章节目录, key为: xpath_of_contents"
    ins_extract_toc_next_page_prompt = "- 如果这是小说的目录,请提取出指向翻页按钮链接的最短的不会重复xpath路径, key为: xpath_of_contents_next"

    content_generate_prompt = """
        现在我将会提供网页的源码,请严格按照指令(instruction)来分析网页内容,不要自由发挥.
        source_code:
        {{source_code}}
        最后以json类型数据返回
    """

    def __init__(self, source_code: str, instruction: list):
        self.source_code = source_code
        self.instruction = instruction

    def generate(self):
        instructions = self.instruction_prompt + '\n'.join(self.instruction)
        return self.specify_role_prompt + instructions + self.content_generate_prompt.replace('{{source_code}}',
                                                                                              self.source_code)


class OpenAICore:
    def __init__(self):
        self.base_url = settings.llm_base_url
        self.api_key = settings.llm_api_key
        self.llm_model = settings.llm_model
        if settings.llm_type != "openai":
            raise ValueError("llm_type must be openai in OpenAICore")

    def analyze_website(self, prompt_generator: Prompt, stream=False):
        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        chat_completion = client.chat.completions.create(
            model=self.llm_model,
            stream=stream,
            temperature=0.4,
            response_format={"type": "json_object"},
            messages=[
                {
                    'role': 'user',
                    'content': prompt_generator.generate(),
                }
            ],
        )
        return chat_completion


# 此函数用于流式输出, 如果直接输出,请将stream设置为False,后可直接print(chat_completion)
def response_stream(openai_response):
    for message in openai_response:
        print(message.choices[0].delta.content, end='')
