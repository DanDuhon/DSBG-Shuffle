try:
    from dsbg_utility import log


    events = {
        "Alluring Skull": {"name": "Alluring Skull", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Big Pilgrim's Key": {"name": "Big Pilgrim's Key", "count": 1, "expansions": set(["The Sunless City"])},
        "Blacksmith's Trial": {"name": "Blacksmith's Trial", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Bleak Bonfire Ascetic": {"name": "Bleak Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Bloodstained Bonfire Ascetic": {"name": "Bloodstained Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Cracked Bonfire Ascetic": {"name": "Cracked Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Firekeeper's Boon": {"name": "Firekeeper's Boon", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Fleeting Glory": {"name": "Fleeting Glory", "count": 2, "expansions": set(["Painted World of Ariamis"])},
        "Forgotten Supplies": {"name": "Forgotten Supplies", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Frozen Bonfire Ascetic": {"name": "Frozen Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Green Blossom": {"name": "Green Blossom", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Hearty Bonfire Ascetic": {"name": "Hearty Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Lifegem": {"name": "Lifegem", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Lost Envoy": {"name": "Lost Envoy", "count": 1, "expansions": set(["The Sunless City"])},
        "Lost to Time": {"name": "Lost to Time", "count": 1, "expansions": set(["The Sunless City"])},
        "Martial Bonfire Ascetic": {"name": "Martial Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Obscured Knowledge": {"name": "Obscured Knowledge", "count": 1, "expansions": set(["Painted World of Ariamis"])},
        "Pine Resin": {"name": "Pine Resin", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Princess Guard": {"name": "Princess Guard", "count": 1, "expansions": set(["The Sunless City"])},
        "Rare Vagrant": {"name": "Rare Vagrant", "count": 1, "expansions": set(["Painted World of Ariamis"])},
        "Repair Powder": {"name": "Repair Powder", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Rite of Rekindling": {"name": "Rite of Rekindling", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Scout Ahead": {"name": "Scout Ahead", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Scrying Stone": {"name": "Scrying Stone", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Skeletal Reforging": {"name": "Skeletal Reforging", "count": 2, "expansions": set(["Tomb of Giants"])},
        "Stolen Artifact": {"name": "Stolen Artifact", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Trustworthy Promise": {"name": "Trustworthy Promise", "count": 2, "expansions": set(["Tomb of Giants"])},
        "Undead Merchant": {"name": "Undead Merchant", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Unhallowed Offering": {"name": "Unhallowed Offering", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Virulent Bonfire Ascetic": {"name": "Virulent Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])}
    }

except Exception as e:
    log(e, exception=True)
    raise