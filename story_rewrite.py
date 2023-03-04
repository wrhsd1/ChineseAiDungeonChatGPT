import os

# from app import ChatApplication
from utils import print_logo, print_warp, error, input_option
from colorama import Fore


PYCHATGPT_AVAILABLE = True
try:
    from revChatGPT.V1 import Chatbot
    from revChatGPT.V3 import Chatbot as ofChatbot
except:
    error("你没有安装revChatGPT或没有更新到最新版本，无法使用。\n\n\n")
    PYCHATGPT_AVAILABLE = False

email = os.getenv("EMAIL")
password = os.getenv("PASS")

class StoryTeller:
    def __init__(self, background):
        """
        Setup chatbot based on type and config.
        Config has different format base on type.
        if type = 0:
            config = {
                "session_token": str,
            }
        if type = 1:
            config = {
                "email": str,
                "password": str,
            }
        """
        self.background = background
        self.type = 1  # 0 for api token (official api) or 1 for openai account (free api)
        self.config = None
        self.chatbot = None
        self.first_interact = True

    def login(self, _config):
        if self.type == 0:
            self.chatbot = ofChatbot(api_key=_config['api_key'])
        else:
            self.chatbot = Chatbot(_config)

    def setup_chatbot(self):
        self.config = self.get_config()
        self.login(self.config)

        if self.first_interact:
            print("请输入背景故事。置空则使用默认背景故事，继续上次，运行continue.py")
            background = input()
            if background:
                self.background = background
        else:
            try:
                with open('chat_log.txt', 'r') as f:
                    lines = f.readlines()
                    last_line = lines[-1]
                    if last_line:
                        self.background = last_line
            except:
                self.background = ""
        print("\n\n\n")

    def get_config(self): 
        _config = {}
        if email and password:
            _config.update({"email": email,
                           "password": password})
  
            return _config
        # return self.config_by_account()

    def start_cli(self):
        print_logo()
        self.setup_chatbot()
        self.interactive()

    # def start_app(self):
    #     app = ChatApplication(self.background)
    #     app.run()

    def save_conversation_id(self, conv_id):
        with open('id_log.txt', 'w') as f:
            f.writelines(conv_id)

    def save_conversations(self, res):
        with open('chat_log.txt', 'w') as f:
            f.writelines(res)

    def action(self, user_action):
        if user_action[-1] != "。":
            user_action = user_action + "。"
        if self.first_interact:
            prompt = """现在来充当一个冒险文字游戏，描述时候注意节奏，不要太快，仔细描述各个人物的身体细节和行为动作细节。一次只需写100字左右，用中文。
            开头是，""" + self.background + """ 你""" + user_action
        else:
            prompt = """继续，一次只需要续写100字左右，用中文。
            你""" + user_action
        response = ""

        if self.type == 1:
            for data in self.chatbot.ask(
                prompt
            ):
                response = data["message"]
            self.save_conversations(response)
            if self.first_interact:
                self.first_interact = False
                self.save_conversation_id(self.chatbot.get_conversations()[0]['id'])
        else:
            response = self.chatbot.ask(prompt)
        return response

    def interactive(self):
        # os.system('clear')
        print_warp(self.background)
        while True:
            action = input(Fore.GREEN + "> 你")
            print_warp(self.action(action))


