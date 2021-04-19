class EmoteRoleSettings:
    """Encapsulates data for role reactions based on emotes
    """

    def __init__(self, role_id: int, emote: str, text: str):
        self.role_id = role_id
        self.emote = emote
        self.text = text
