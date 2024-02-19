try:
    from statistics import mean

    from lookup_table import LookupTable
    from dsbg_utility import log


    soulCost = {
        "Assassin": {
            "expansions": set(["Dark Souls The Board Game"]),
            "strength": LookupTable(
                (10, 0),
                (16, 2),
                (25, 6),
                (34, 14)),
            "dexterity": LookupTable(
                (14, 0),
                (22, 2),
                (31, 6),
                (40, 14)),
            "intelligence": LookupTable(
                (11, 0),
                (18, 2),
                (27, 6),
                (36, 14)),
            "faith": LookupTable(
                (9, 0),
                (14, 2),
                (22, 6),
                (30, 14))
            },
        "Cleric": {
            "expansions": set(["Tomb of Giants", "Characters Expansion"]),
            "strength": LookupTable(
                (12, 0),
                (18, 2),
                (27, 6),
                (37, 14)),
            "dexterity": LookupTable(
                (8, 0),
                (15, 2),
                (24, 6),
                (33, 14)),
            "intelligence": LookupTable(
                (7, 0),
                (14, 2),
                (22, 6),
                (30, 14)),
            "faith": LookupTable(
                (16, 0),
                (23, 2),
                (32, 6),
                (40, 14))
            },
        "Deprived": {
            "expansions": set(["Tomb of Giants", "Characters Expansion"]),
            "strength": LookupTable(
                (10, 0),
                (20, 2),
                (30, 6),
                (40, 14)),
            "dexterity": LookupTable(
                (10, 0),
                (20, 2),
                (30, 6),
                (40, 14)),
            "intelligence": LookupTable(
                (10, 0),
                (20, 2),
                (30, 6),
                (40, 14)),
            "faith": LookupTable(
                (10, 0),
                (20, 2),
                (30, 6),
                (40, 14))
            },
        "Herald": {
            "expansions": set(["Dark Souls The Board Game", "The Sunless City"]),
            "strength": LookupTable(
                (12, 0),
                (19, 2),
                (28, 6),
                (37, 14)),
            "dexterity": LookupTable(
                (11, 0),
                (17, 2),
                (26, 6),
                (34, 14)),
            "intelligence": LookupTable(
                (8, 0),
                (12, 2),
                (20, 6),
                (29, 14)),
            "faith": LookupTable(
                (13, 0),
                (22, 2),
                (31, 6),
                (40, 14))
            },
        "Knight": {
            "expansions": set(["Dark Souls The Board Game"]),
            "strength": LookupTable(
                (13, 0),
                (21, 2),
                (30, 6),
                (40, 14)),
            "dexterity": LookupTable(
                (12, 0),
                (19, 2),
                (29, 6),
                (38, 14)),
            "intelligence": LookupTable(
                (9, 0),
                (15, 2),
                (23, 6),
                (31, 14)),
            "faith": LookupTable(
                (9, 0),
                (15, 2),
                (23, 6),
                (31, 14))
            },
        "Mercenary": {
            "expansions": set(["Painted World of Ariamis", "Characters Expansion"]),
            "strength": LookupTable(
                (10, 0),
                (17, 2),
                (26, 6),
                (35, 14)),
            "dexterity": LookupTable(
                (16, 0),
                (22, 2),
                (32, 6),
                (40, 14)),
            "intelligence": LookupTable(
                (10, 0),
                (17, 2),
                (26, 6),
                (35, 14)),
            "faith": LookupTable(
                (8, 0),
                (14, 2),
                (21, 6),
                (30, 14))
            },
        "Pyromancer": {
            "expansions": set(["Tomb of Giants", "Characters Expansion", "The Sunless City"]),
            "strength": LookupTable(
                (12, 0),
                (17, 2),
                (26, 6),
                (35, 14)),
            "dexterity": LookupTable(
                (9, 0),
                (13, 2),
                (20, 6),
                (27, 14)),
            "intelligence": LookupTable(
                (14, 0),
                (21, 2),
                (31, 6),
                (40, 14)),
            "faith": LookupTable(
                (14, 0),
                (19, 2),
                (28, 6),
                (38, 14))
            },
        "Sorcerer": {
            "expansions": set(["Painted World of Ariamis", "Characters Expansion"]),
            "strength": LookupTable(
                (7, 0),
                (14, 2),
                (22, 6),
                (31, 14)),
            "dexterity": LookupTable(
                (12, 0),
                (18, 2),
                (27, 6),
                (36, 14)),
            "intelligence": LookupTable(
                (16, 0),
                (23, 2),
                (32, 6),
                (40, 14)),
            "faith": LookupTable(
                (7, 0),
                (15, 2),
                (24, 6),
                (33, 14))
            },
        "Thief": {
            "expansions": set(["Tomb of Giants", "Characters Expansion"]),
            "strength": LookupTable(
                (9, 0),
                (16, 2),
                (24, 6),
                (33, 14)),
            "dexterity": LookupTable(
                (13, 0),
                (21, 2),
                (31, 6),
                (40, 14)),
            "intelligence": LookupTable(
                (10, 0),
                (18, 2),
                (27, 6),
                (36, 14)),
            "faith": LookupTable(
                (8, 0),
                (15, 2),
                (23, 6),
                (31, 14))
            },
        "Warrior": {
            "expansions": set(["Dark Souls The Board Game", "The Sunless City"]),
            "strength": LookupTable(
                (16, 0),
                (23, 2),
                (32, 6),
                (40, 14)),
            "dexterity": LookupTable(
                (9, 0),
                (16, 2),
                (25, 6),
                (35, 14)),
            "intelligence": LookupTable(
                (8, 0),
                (15, 2),
                (23, 6),
                (30, 14)),
            "faith": LookupTable(
                (9, 0),
                (16, 2),
                (25, 6),
                (35, 14))
            }
    }

    def mean_soul_cost(item, setsAvailable, charactersActive):
        try:
            log("Start of mean_soul_cost")

            costs = []
            for c in [c for c in soulCost if c in charactersActive and soulCost[c]["expansions"] & setsAvailable]:
                strength = soulCost[c]["strength"][item["strength"]]
                dexterity = soulCost[c]["dexterity"][item["dexterity"]]
                intelligence = soulCost[c]["intelligence"][item["intelligence"]]
                faith = soulCost[c]["faith"][item["faith"]]
                if strength is not None and dexterity is not None and intelligence is not None and faith is not None:
                    costs.append(strength + dexterity + intelligence + faith)

                log("End of mean_soul_cost")

            return mean(costs)
        except Exception as e:
            log(e, exception=True)
            raise
except Exception as e:
    log(e, exception=True)
    raise
