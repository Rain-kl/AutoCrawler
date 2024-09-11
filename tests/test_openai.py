from plugins.openai_core import OpenAICore, Prompt,response_stream

def test_openai():
    with open('./data/test.html', 'r') as f:
        source_code = f.read()
    prompt = Prompt(
        source_code=source_code,
        instruction=[
            Prompt.ins_analyze_website_themes_prompt,
            Prompt.ins_extract_main_text_prompt,
            Prompt.ins_extract_mt_next_page_prompt,
            Prompt.ins_extract_table_of_contents_prompt,
            Prompt.ins_extract_toc_next_page_prompt,
        ]
    )
    # print(prompt.generate_prompt())
    openai = OpenAICore()
    chat_completion = openai.analyze_website(prompt,stream=True)
    response_stream(chat_completion)
