try:
    from dsbg_shuffle_enemies import enemies
    from dsbg_shuffle_utility import log


    tooltipText = {
        "bitterCold": "If a character has a Frostbite token at the end of their turn, they suffer 1 damage.",
        "barrage": "At the end of each character's turn, that character must make a defense roll using only their dodge dice.\n\nIf no dodge symbols are rolled, the character suffers 2 damage and Stagger.",
        "darkness": "During this encounter, characters can only attack enemies on the same or an adjacent node.",
        "eerie": "During setup, take five blank trap tokens and five trap tokens with values on them, and place a random token face down on each of the highlighted nodes.\n\nIf a character moves onto a node with a token, flip the token.\n\nIf the token is blank, place it to one side.\n\nIf the token has a damage value, instead of resolving it normally, spawn an enemy corresponding to the value shown, push the character to a node containing a trap token if possible, then discard the token.",
        "gang": "A gang enemy is a 1 health enemy whose name includes the word in parentheses.\n\nIf a character is attacked by a gang enemy and another gang enemy is within one node of the character, increase the attacking model's damage and dodge difficulty values by 1 when resolving the attack.",
        "hidden": "After declaring an attack, players must discard a die of their choice before rolling.\n\nIf the attacks only has a single die already, ignore this rule.",
        "illusion": "During setup, only place tile one. Then, shuffle one doorway (or blank) trap token and four trap tokens with damage values, and place a token face down on each of the highlighted nodes.\n\nIf a character moves onto a node with a token, flip the token. If the token has a damage value, resolve the effects normally. If the token is the doorway, discard all face down trap tokens, and place the next sequential tile as shown on the encounter card. Then, place the character on a doorway node on the new tile. After placing the character, if the new tile has highlighted nodes, repeat the steps above.\n\nOnce a doorway token has been revealed, it counts as the doorway node that connects to the next sequential tile.",
        "mimic": "If a character opens a chest in this encounter, shuffle the chest deck and draw a card. If a blank card is drawn, resolve the chest rules as normal. If the teeth card is drawn, replace the chest with the listed model instead.\n\nThe chest deck contains three blank cards and two teeth cards. You can simulate this with trap tokens also - shuffle three blank trap tokens and two trap tokens with a value.",
        "onslaught": "Each tile begins the encounter as active (all enemies on active tiles act on their turn).",
        "poisonMist": "During setup, place trap tokens on the tile indicated in brackets using the normal trap placement rules.\n\nThen, reveal the tokens, replacing each token with a value with a poison cloud token. If a character ends their turn on the same node as a poison cloud token, they suffer Poison.",
        "snowstorm": "At the start of each character's turn, that character suffers Frostbite unless they have the torch token on their dashboard or are on the same node as the torch token or a character with the torch token on their dashboard.",
        "timer": "If the timer marker reaches the value shown in brackets, resolve the effect listed.",
        "trial": "Trials offer an extra objective providing additional rewards if completed.\n\nThis is shown in parentheses, either in writing, or as a number of turns in which the characters must complete the encounter's main objective.\n\nCompleting trial objectives is not mandatory to complete an encounter.",
    }

    for enemy in enemies:
        tooltipText[enemy.name] = enemy.name
        
except Exception as e:
    log(e, exception=True)
    raise