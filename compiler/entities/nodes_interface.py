from abc import ABCMeta, abstractmethod


class INodeInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def enter(self, node, parent): raise NotImplementedError

    @abstractmethod
    def exit(self, node, parent): raise NotImplementedError
