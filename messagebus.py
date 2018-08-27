from __future__ import annotations
from typing import List
from threading import Thread

class CustomThread(Thread):
    def __init__(self):
        super().__init__()
        self.do_run = True
    def stop(self):
        self.do_run = False

class MessageBus(CustomThread):
    __inst = None
    __possibility = True

    @classmethod
    def getSingletonInstance(cls) -> MessageBus:
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

    def addToRecipientList(self, instance, *instances):
        if instance in self.recipent_list:
            raise Exception(f"{instance} is already in the recipent list!")
        else:
            self.recipent_list.append(instance)

        for i in instances:
            if i in self.recipent_list:
                raise Exception(f"{i} is already in the recipent list!")
            else:
                self.recipent_list.append(i)

    def deliverMessage(self, message: Message):
        # print(message)
        for i in self.recipent_list:
            try:
                # print(i)
                i.onMessageReceived(message)
            except Exception as e:
                print(i)
                raise e

    def sendMessage(self, message: Message):
        self.message_queue.append(message)


    def run(self):
        while self.do_run:

            message: Message

            print(self.message_queue)
            if self.message_queue:
                message = self.message_queue.pop()
                self.deliverMessage(message)

class Recipient:
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