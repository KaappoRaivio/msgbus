from messagebus import *


class Logger(Recipient):
    def __init__(self, printstring):
        self.string = printstring

    def onMessageReceived(self, message: Message):
        if message.content == Message.LOG:
            print("Logging!")
            print(f"\t{message}")
            self.sendMessage(Message(Message.SUCCESS, "Log"))

class Renderer(Recipient):
    def __init__(self, res_x, res_y):
        self.res_x = res_x
        self.res_y = res_y

    def onMessageReceived(self, message: Message):
        if message.content == Message.RENDER:
            # print(f"Rendering with resolution {self.res_x} * {self.res_y}")
            self.sendMessage(Message(Message.SUCCESS, f"Rendering with resolution {self.res_x} * {self.res_y}"))
            # Render
            # self.sendMessage(Message(Message.SUCCESS, "Render"))


