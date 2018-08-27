from threading import Thread
import time

from messagebus import *
from recipients import Logger, Renderer


class Commander(CustomThread, Recipient):
    def __init__(self):
        super().__init__()

        MessageBus.getSingletonInstance().addToRecipientList(self)

    def run(self):
        print("Moi")
        counter = 0
        while self.do_run:
            time.sleep(1)

            if not counter % 1:
                self.sendMessage(Message(Message.RENDER))
            if not counter % 2:
                self.sendMessage(Message(Message.LOG))

            counter += 1

    def onMessageReceived(self, message: Message):
        pass

try:
    messagebus = MessageBus()

    commander = Commander()
    logger = Logger("asd")
    renderer = Renderer(1920, 1080)
    MessageBus.getSingletonInstance().addToRecipientList(logger, renderer)
    commander.start()
except KeyboardInterrupt:
    messagebus.stop()
    commander.stop()
