from abc import ABC, abstractmethod

from classes.sprites.basic_sprite import BasicSprite

class BaseStage(ABC):
    @abstractmethod
    def make_bg_sprites(self) -> list[BasicSprite]:
        pass

    @abstractmethod
    def make_fg_sprites(self) -> list[BasicSprite]:
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def postcreate(self):
        pass