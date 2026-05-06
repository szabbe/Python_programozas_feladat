import json

epuletek_pattern = {
    "Fureszmalom": {
        "Ar": {"Arany": 3, "Fa": 5, "Ko": 3, "Vas": 3},
        "Termeles": {
            "Arany": 0,
            "Fa": lambda epuletek: 5 + 2 * epuletek["Erdo"],
            "Ko": 0,
            "Vas": 0
        }
    },
    "Erdo": {
        "Ar": {"Arany": 0, "Fa": 0, "Ko": 0, "Vas": 0},
        "Termeles": {
            "Arany": 0,
            "Fa": 0,
            "Ko": 0,
            "Vas": 0
        }
    },
    "Vadaszkunyho": {
       "Ar": {"Arany": 5, "Fa": 5, "Ko": 2, "Vas": 4},
        "Termeles": {
            "Arany": lambda epuletek: 5 + 2 * epuletek["Erdo"],
            "Fa": 0,
            "Ko": 0,
            "Vas": 0
        } 
    },
        "Mezo": {
        "Ar": {"Arany": 0, "Fa": 0, "Ko": 0, "Vas": 0},
        "Termeles": {
            "Arany": 0,
            "Fa": 0,
            "Ko": 0,
            "Vas": 0
        }
    },
        "Farm": {
        "Ar": {"Arany": 5, "Fa": 2, "Ko": 2, "Vas": 2},
        "Termeles": {
            "Arany": lambda epuletek: 3 + 2 * epuletek["Mezo"],
            "Fa": 0,
            "Ko": 0,
            "Vas": 0
        }
    },
        "Hegy": {
        "Ar": {"Arany": 0, "Fa": 0, "Ko": 0, "Vas": 0},
        "Termeles": {
            "Arany": 0,
            "Fa": 0,
            "Ko": 0,
            "Vas": 0
        }
    },

}



with open("epuletek.json", "w", encoding="utf-8") as f:
    json.dump(epuletek_pattern, f)