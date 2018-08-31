from messagebus import *


class Logger(Recipient):
    def __init__(self,):
        super().__init__()

    def onMessageReceived(self, message: Message):
        # print(message)
        if message.content in [Message.SUCCESS, Message.LOG]:
            print(f"Logging\n\t{message}")

class Renderer(Recipient):
    def __init__(self, res_x, res_y):
        super().__init__()
        self.res_x = res_x
        self.res_y = res_y

    def onMessageReceived(self, message: Message):
        # print("Moi")
        if message.content == Message.RENDER:
            # print("moi")
            self.sendMessage(Message(Message.SUCCESS, f"Rendering with resolution {self.res_x} * {self.res_y}"))


# class Gameloop(CustomThread):
#     def __init__(self):
#         super().__init__()
#
#     def run(self):
#

# messagebus = MessageBus()
renderer = Renderer(1920, 1080)
logger = Logger()

MessageBus.addToRecipientList(renderer, logger)

import time
counter = 0

while True:
    time.sleep(1)
    if not counter % 5:
        MessageBus.sendMessage(Message(Message.RENDER, "Render now!"))