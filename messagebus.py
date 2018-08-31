from __future__ import annotations
from typing import List
from threading import Thread
import time

class CustomThread(Thread):
    def __init__(self):
        super().__init__()
        self.do_run = True
        self.daemon = True
    def stop(self):
        self.do_run = False

class MessageBus(CustomThread):
    __inst = None
    __possibility = True

    @classmethod
    def getSingletonInstance(cls) -> MessageBus:
        if cls.__inst is None:
            cls.__inst = cls()

        return cls.__inst



    def __init__(self):
        super().__init__()

        if self.__possibility:
            MessageBus.__inst = self
            self.__possibility = False
        else:
            raise Exception("Must be a singleton instance!")

        self.message_queue: List[Message] = []
        self.recipent_list: List[Recipient] = []

        self.start()

    @classmethod
    def addToRecipientList(cls, *instances):
        self = cls.getSingletonInstance()
        for i in instances:
            if i in self.recipent_list:
                raise Exception(f"{i} is already in the recipent list!")
            else:
                self.recipent_list.append(i)

    @classmethod
    def deliverMessage(cls, message: Message):
        self = cls.getSingletonInstance()
        # print(message)
        for i in self.recipent_list:
            try:
                # print(i)
                i.onMessageReceived(message)
            except Exception as e:
                print(i)
                raise e

    @classmethod
    def sendMessage(cls, message: Message):
        self = cls.getSingletonInstance()

        self.message_queue.append(message)


    def run(self):
        while self.do_run:

            message: Message
            time.sleep(0.001)

            # print(self.message_queue)
            if self.message_queue:
                message = self.message_queue.pop()
                self.deliverMessage(message)

class Recipient:
    def __init__(self):
        pass
    """Interface"""
    def onMessageReceived(self, message: Message):
        raise NotImplementedError("Class must implement this!")

    def sendMessage(self, message: Message):
        MessageBus.getSingletonInstance().sendMessage(message)

class Message:
    RENDER = 0
    UPDATE = 1
    LOG = 2
    PAUSE = 3
    SUCCESS = 4

    def __init__(self, content: int, human_readable_intent: str=""):
        self.content = content
        self.human_readable_intent = human_readable_intent

    def __str__(self):
        return f"Message({self.content}, {self.human_readable_intent})"