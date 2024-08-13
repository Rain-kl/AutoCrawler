class LLMSettings:
    # ai相关配置
    llm_type: str = "openai"
    llm_model: str = "gpt-4o"
    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = "your-api-key"
    llm_enable_proxy: bool = False