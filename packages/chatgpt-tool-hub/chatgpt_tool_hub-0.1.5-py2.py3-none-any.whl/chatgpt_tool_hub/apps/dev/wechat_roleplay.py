import logging

from chatgpt_tool_hub.apps.app import App
from chatgpt_tool_hub.bots.initialize import initialize_bot
from common.log import logger
from config import conf, load_config
from lib.langchain_lite.memory import ConversationTokenBufferMemory
from lib.langchain_lite.models.chatgpt import ChatOpenAI
from chatgpt_tool_hub.tools.load_tools import load_tools


class WechatRolePlay(App):

    helper_bot = None
    chat_bot = None

    mandatory_tools = ["news-api"]

    def __init__(self):
        super().__init__()
        if not self.init_flag:
            model_kwargs = {
                "openai_api_key": conf().get('open_ai_api_key'),
                "proxy": conf().get('proxy'),
                "model_name": "gpt-3.5-turbo",  # 对话模型的名称
                "top_p": 1,
                "frequency_penalty": 0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                "presence_penalty": 0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                "request_timeout": 12,
                "max_retries": 3
            }
            self.strict_llm = ChatOpenAI(temperature=0, **model_kwargs)
            self.chat_llm = ChatOpenAI(temperature=0.8, **model_kwargs)
            self.memory = ConversationTokenBufferMemory(llm=self.chat_llm, memory_key="chat_history",
                                                        output_key='output', max_token_limit=1600,
                                                        filter_key_list=["helper_output"])
            self.init_flag = True

    def create(self, use_tools: list):
        logger.debug(f"Initializing {self.get_class_name()}, use_tools={use_tools}")
        if not self._check_mandatory_tools(use_tools):
            raise ValueError("_check_mandatory_tools failed")

        # loading tools from config.
        tools_kwargs = dict()
        for key, value in conf().get('app', {}).get('tools_kwargs', {}).items():
            tools_kwargs[key] = value
        tools = load_tools(use_tools, llm=self.strict_llm, **tools_kwargs)

        # create bots
        self.helper_bot = initialize_bot(tools, self.strict_llm, bot="qa-bot", verbose=True, max_iterations=3,
                                           early_stopping_method="generate")
        self.chat_bot = initialize_bot([], self.chat_llm, bot="catgirl-bot", verbose=True, memory=self.memory,
                                         max_iterations=1)

    def ask(self, query: str, session: list = None, retry_num: int = 0) -> str:
        assert self.chat_bot is not None and self.helper_bot is not None
        if not query:
            logger.warning("[APP]: query is zero value")
            return "query is empty"
        if session is not None:
            self._refresh_memory(session)
        try:
            helper_output = self.helper_bot.run(query)
            logger.info(f"[APP]: {str(helper_output)}")
            return self.chat_bot.run(input=query, helper_output=helper_output)
        except ValueError as e:
            logger.exception(e)
            logger.error(f"[APP] catch a ValueError: {str(e)}")
            if retry_num < 1:
                return self.ask(query, session, retry_num+1)
            else:
                return "exceed retry_num"

    def _refresh_memory(self, session: list):
        self.memory.chat_memory.clear()

        for item in session:
            if item.get('role') == 'user':
                self.memory.chat_memory.add_user_message(item.get('content'))
            elif item.get('role') == 'assistant':
                self.memory.chat_memory.add_ai_message(item.get('content'))
        logger.debug("Now memory: {}".format(self.memory.chat_memory))

    def _check_mandatory_tools(self, use_tools: list) -> bool:
        for tool in self.mandatory_tools:
            if tool not in use_tools:
                logger.error(f"You have to load {tool} as a basic tool for f{self.get_class_name()}")
                return False
        return True


if __name__ == "__main__":
    load_config()
    logger.setLevel(logging.DEBUG)

    bot = WechatRolePlay()
    bot.create(["news-api", "requests", "open-meteo-api"])
    response = bot.ask("分享给我一条最近中国的新闻")
    # print(str(response))
