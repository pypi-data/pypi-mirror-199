import os

from chatgpt_tool_hub.apps.app import App
from chatgpt_tool_hub.bots.initialize import initialize_bot
from chatgpt_tool_hub.common.log import logger
from config import conf, load_config
from lib.langchain_lite.memory import ConversationTokenBufferMemory
from lib.langchain_lite.models.chatgpt import ChatOpenAI
from chatgpt_tool_hub.tools.load_tools import load_tools


class WechatManager(App):

    mandatory_tools = ["wechat-send-message", "wechat-send-picture"]

    def __init__(self):
        super().__init__()
        if not self.init_flag:
            os.environ["OPENAI_API_KEY"] = conf().get('open_ai_api_key')
            self.llm = ChatOpenAI(temperature=0,  # 值在[0,1]之间，越大表示回复越具有不确定性
                                  model_name="gpt-3.5-turbo",  # 对话模型的名称
                                  top_p=1,
                                  frequency_penalty=0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                                  presence_penalty=0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                                  request_timeout=12,
                                  max_retries=3)

            self.memory = ConversationTokenBufferMemory(llm=self.llm, memory_key="chat_history",
                                                        output_key='output', max_token_limit=1000)
            self.init_flag = True

    def create(self, use_tools: list):
        logger.debug(f"Initializing {self.get_class_name()}, use_tools={use_tools}")

        if not self._check_mandatory_tools(use_tools):
            raise ValueError("_check_mandatory_tools failed")

        tools = load_tools(use_tools, llm=self.llm, news_api_key=conf().get('news_api_key'),
                           searx_host=conf().get('searx_host'))

        self.bot = initialize_bot(tools, self.llm, bot="qa-bot", verbose=True,
                                    memory=self.memory, max_iterations=4, early_stopping_method="generate")

    def _check_mandatory_tools(self, use_tools: list) -> bool:
        for tool in self.mandatory_tools:
            if tool not in use_tools:
                logger.error(f"You have to load {tool} as a basic tool for f{self.get_class_name()}")
                return False
        return True


if __name__ == "__main__":
    load_config()

    bot = WechatManager()
    bot.create(conf().get('use_tools'))
    bot.bot.run("文心一言是什么")
