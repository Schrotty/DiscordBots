class Templates:
    DICE = ['dice', 'w', 'd']
    RANDOM = ['wahl', 'pick', 'choose']

    DICE_RESULT = "{MENTION} Du hast folgende Zahlen gewürfelt: {RESULT}"  # Leave whitespace at end!
    RANDOM_INVALID_NUMER = "{MENTION}, gibt bitte eine korrekte Zahl an!"
    RANDOM_NO_CHOICES = "{MENTION}, gib bitte ein paar Optionen an!"

    RANK_TRACK_TOGGLE_BADARGS = "{MENTION}, du musst einen erkennbaren |wahr| oder |falsch| wert angeben!"

    # RANK_TRACK_TOGGLE_TRUE = "{MENTION}, deine XP werden nun getrackt!"
    # RANK_TRACK_TOGGLE_FALSE = "{MENTION}, deine XP werden nicht mehr getrackt!"