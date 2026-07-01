from models.player import Player


class PlayerRegistrationJSON:
    @staticmethod
    def to_json(player: Player) -> str:
        return player.chess_id
