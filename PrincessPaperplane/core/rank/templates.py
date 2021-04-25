class Template:
    ALIAS: list = ["rang", "level", "lvl"]
    COMMAND_NAME: str = "rank"
    HELP_TEXT: str = "Shows current level, exp and needed exp for level up."

    NEW_ROLE_MENTION: str = (
        "{MENTION} Du hast eine neue Stufe erreicht und erhältst den neuen Rang {ROLE}!"
    )

    GAINED_EP_LOG_MSG: str = "Exp for Level-Up: {GAINED}, current XP: {CURRENT}"
    NEW_ROLE_LOG_MSG: str = "Assign {AUTHOR} new role {ROLE}"
    REMOVE_ROLE_LOG_MSG: str = "Remove {AUTHOR} old role {ROLE}"

    RANK_EMBED_TITLE: str = "Dein aktuelles Level: {LEVEL}"
    RANK_EMBED_DESCRIPTION: str = (
        "Aktuelle XP: {EXP}\nVerbleibende XP bis Level {NEXT_LEVEL}: {EXP_LEFT}"
    )
    RANK_IMAGE_GENERATOR_URL: str = "https://501-legion.de/princesspaperplane/generateLevel.php?user={AUTHOR_ID}&time={TIME}{EXT}"
