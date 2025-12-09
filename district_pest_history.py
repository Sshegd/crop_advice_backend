# district_pest_history.py
PEST_HISTORY = {

    # 1. Bagalkot
    "bagalkot": {
        "sorghum": {
            "Shoot Fly": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            },
            "Stem Borer": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "LOW",
            },
        },
        "cotton": {
            "Pink Bollworm": {
                "season": ["September", "October", "November"],
                "peak_months": ["October"],
                "risk_level": "HIGH",
            }
        },
        "groundnut": {
            "Leaf Spot & Rust": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 2. Ballari
    "ballari": {
        "groundnut": {
            "Leaf Miner": {
                "season": ["August", "September"],
                "peak_months": ["August"],
                "risk_level": "LOW",
            },
            "Leaf Spot & Rust": {
                "season": ["September", "October"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            },
        },
        "sunflower": {
            "Head Borer": {
                "season": ["September", "October"],
                "peak_months": ["October"],
                "risk_level": "MEDIUM",
            }
        },
        "paddy": {
            "Brown Planthopper": {
                "season": ["September", "October"],
                "peak_months": ["October"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 3. Belagavi
    "belagavi": {
        "sugarcane": {
            "Early Shoot Borer": {
                "season": ["June", "July"],
                "peak_months": ["July"],
                "risk_level": "HIGH",
            },
            "Red Rot": {
                "season": ["August", "September"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            },
        },
        "soybean": {
            "Stem Fly": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "LOW",
            },
            "Rust": {
                "season": ["September", "October"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            },
        },
        "maize": {
            "Fall Armyworm": {
                "season": ["June", "July", "August"],
                "peak_months": ["July"],
                "risk_level": "HIGH",
            },
        },
    },

    # 4. Bengaluru Rural
    "bengaluru rural": {
        "ragi": {
            "Blast": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "vegetables": {
            "Fruit Borer Complex": {
                "season": ["January", "February", "March"],
                "peak_months": ["February"],
                "risk_level": "MEDIUM",
            }
        },
        "mulberry": {
            "Leaf Spot": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "LOW",
            }
        },
    },

    # 5. Bengaluru Urban
    "bengaluru urban": {
        "tomato": {
            "Leaf Curl Virus": {
                "season": ["January", "February", "March"],
                "peak_months": ["February"],
                "risk_level": "HIGH",
            },
            "Early Blight": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            },
        },
        "flowers": {
            "Aphid & Mite Complex": {
                "season": ["November", "December", "January"],
                "peak_months": ["December"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 6. Bidar
    "bidar": {
        "pigeon pea": {
            "Pod Borer": {
                "season": ["October", "November", "December"],
                "peak_months": ["November"],
                "risk_level": "HIGH",
            }
        },
        "soybean": {
            "Rust": {
                "season": ["September", "October"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
        "bengal gram": {
            "Helicoverpa Armigera": {
                "season": ["December", "January"],
                "peak_months": ["January"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 7. Vijayapura
    "vijayapura": {
        "grapes": {
            "Downy Mildew": {
                "season": ["December", "January", "February"],
                "peak_months": ["January"],
                "risk_level": "HIGH",
            },
            "Powdery Mildew": {
                "season": ["January", "February"],
                "peak_months": ["February"],
                "risk_level": "MEDIUM",
            },
        },
        "pomegranate": {
            "Bacterial Blight": {
                "season": ["August", "September", "October"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "onion": {
            "Thrips": {
                "season": ["December", "January", "February"],
                "peak_months": ["January"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 8. Chamarajanagar
    "chamarajanagar": {
        "sugarcane": {
            "Early Shoot Borer": {
                "season": ["June", "July"],
                "peak_months": ["July"],
                "risk_level": "MEDIUM",
            }
        },
        "ragi": {
            "Blast": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "turmeric": {
            "Rhizome Rot": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 9. Chikkamagaluru
    "chikkamagaluru": {
        "coffee": {
            "Coffee Berry Borer": {
                "season": ["August", "September", "October"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            },
            "Leaf Rust": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            },
        },
        "pepper": {
            "Foot Rot": {
                "season": ["June", "July", "August"],
                "peak_months": ["July"],
                "risk_level": "HIGH",
            }
        },
        "areca nut": {
            "Mite Infestation": {
                "season": ["March", "April", "May"],
                "peak_months": ["April"],
                "risk_level": "HIGH",
            }
        },
    },

    # 10. Chikkaballapur
    "chikkaballapur": {
        "ragi": {
            "Blast": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "tomato": {
            "Leaf Curl Virus": {
                "season": ["January", "February", "March"],
                "peak_months": ["February"],
                "risk_level": "HIGH",
            }
        },
        "mulberry": {
            "Leaf Spot": {
                "season": ["July", "August"],
                "peak_months": ["July"],
                "risk_level": "LOW",
            }
        },
    },

    # 11. Chitradurga
    "chitradurga": {
        "groundnut": {
            "Leaf Spot": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "sunflower": {
            "Head Borer": {
                "season": ["September", "October"],
                "peak_months": ["October"],
                "risk_level": "MEDIUM",
            }
        },
        "maize": {
            "Stem Borer": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "LOW",
            }
        },
    },

    # 12. Dakshina Kannada
    "dakshina kannada": {
        "areca nut": {
            "Mite Infestation": {
                "season": ["February", "March", "April"],
                "peak_months": ["March"],
                "risk_level": "HIGH",
            },
            "Yellow Leaf Disease": {
                "season": ["June", "July", "August"],
                "peak_months": ["July"],
                "risk_level": "MEDIUM",
            },
        },
        "coconut": {
            "Rhinoceros Beetle": {
                "season": ["June", "July", "August"],
                "peak_months": ["July"],
                "risk_level": "MEDIUM",
            }
        },
        "paddy": {
            "Blast Disease": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 13. Davanagere
    "davanagere": {
        "paddy": {
            "Stem Borer": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            },
            "Brown Spot": {
                "season": ["September", "October"],
                "peak_months": ["October"],
                "risk_level": "LOW",
            },
        },
        "cotton": {
            "Whitefly & Viral Complex": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 14. Dharwad
    "dharwad": {
        "soybean": {
            "Leaf Miner": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
        "cotton": {
            "Pink Bollworm": {
                "season": ["September", "October", "November"],
                "peak_months": ["October"],
                "risk_level": "HIGH",
            },
            "Whitefly & Viral Complex": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            },
        },
        "groundnut": {
            "Leaf Spot & Rust": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
    },

    # 15. Gadag
    "gadag": {
        "bengal gram": {
            "Helicoverpa Armigera": {
                "season": ["December", "January"],
                "peak_months": ["January"],
                "risk_level": "MEDIUM",
            }
        },
        "groundnut": {
            "Leaf Spot": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
        "jowar": {
            "Shoot Fly": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "LOW",
            }
        },
    },

    # 16. Hassan
    "hassan": {
        "paddy": {
            "Blast Disease": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "coffee": {
            "Leaf Rust": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            }
        },
        "potato": {
            "Late Blight": {
                "season": ["December", "January"],
                "peak_months": ["January"],
                "risk_level": "HIGH",
            }
        },
    },

    # 17. Haveri
    "haveri": {
        "cotton": {
            "Pink Bollworm": {
                "season": ["September", "October"],
                "peak_months": ["October"],
                "risk_level": "HIGH",
            }
        },
        "chilli": {
            "Thrips & Mite Complex": {
                "season": ["January", "February", "March"],
                "peak_months": ["February"],
                "risk_level": "MEDIUM",
            },
            "Anthracnose": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            },
        },
        "maize": {
            "Fall Armyworm": {
                "season": ["June", "July"],
                "peak_months": ["July"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 18. Kalaburagi
    "kalaburagi": {
        "pigeon pea": {
            "Pod Borer": {
                "season": ["October", "November", "December"],
                "peak_months": ["November"],
                "risk_level": "HIGH",
            }
        },
        "bengal gram": {
            "Helicoverpa Armigera": {
                "season": ["December", "January"],
                "peak_months": ["January"],
                "risk_level": "MEDIUM",
            }
        },
        "jowar": {
            "Shoot Fly": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "LOW",
            }
        },
    },

    # 19. Kodagu
    "kodagu": {
        "coffee": {
            "Coffee Berry Borer": {
                "season": ["August", "September", "October"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "pepper": {
            "Foot Rot": {
                "season": ["June", "July", "August"],
                "peak_months": ["July"],
                "risk_level": "HIGH",
            }
        },
        "cardamom": {
            "Shoot & Capsule Borer": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 20. Kolar
    "kolar": {
        "tomato": {
            "Leaf Curl Virus": {
                "season": ["January", "February", "March"],
                "peak_months": ["February"],
                "risk_level": "HIGH",
            }
        },
        "mango": {
            "Powdery Mildew": {
                "season": ["February", "March"],
                "peak_months": ["March"],
                "risk_level": "MEDIUM",
            }
        },
        "ragi": {
            "Blast": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 21. Koppal
    "koppal": {
        "paddy": {
            "Stem Borer": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
        "cotton": {
            "Pink Bollworm": {
                "season": ["September", "October"],
                "peak_months": ["October"],
                "risk_level": "HIGH",
            }
        },
        "chilli": {
            "Thrips": {
                "season": ["January", "February"],
                "peak_months": ["February"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 22. Mandya
    "mandya": {
        "sugarcane": {
            "Early Shoot Borer": {
                "season": ["June", "July"],
                "peak_months": ["July"],
                "risk_level": "HIGH",
            }
        },
        "paddy": {
            "Stem Borer": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
        "banana": {
            "Sigatoka": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 23. Mysuru
    "mysuru": {
        "ragi": {
            "Blast": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "cotton": {
            "Whitefly & Viral Complex": {
                "season": ["August", "September"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            }
        },
        "groundnut": {
            "Leaf Spot & Rust": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "HIGH",
            }
        },
    },

    # 24. Raichur
    "raichur": {
        "paddy": {
            "Brown Planthopper": {
                "season": ["September", "October"],
                "peak_months": ["October"],
                "risk_level": "HIGH",
            }
        },
        "cotton": {
            "Pink Bollworm": {
                "season": ["September", "October", "November"],
                "peak_months": ["October"],
                "risk_level": "HIGH",
            }
        },
        "redgram": {
            "Pod Borer": {
                "season": ["November", "December"],
                "peak_months": ["December"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 25. Ramanagara
    "ramanagara": {
        "ragi": {
            "Blast": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "mulberry": {
            "Leaf Spot": {
                "season": ["July", "August"],
                "peak_months": ["July"],
                "risk_level": "LOW",
            }
        },
        "vegetables": {
            "Fruit Borer Complex": {
                "season": ["January", "February"],
                "peak_months": ["February"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 26. Shivamogga
    "shivamogga": {
        "areca nut": {
            "Mite Infestation": {
                "season": ["March", "April", "May"],
                "peak_months": ["April"],
                "risk_level": "HIGH",
            },
            "Yellow Leaf Disease": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            },
        },
        "banana": {
            "Sigatoka Leaf Spot": {
                "season": ["June", "July", "August", "September"],
                "peak_months": ["August"],
                "risk_level": "HIGH",
            },
            "Panama Wilt": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "MEDIUM",
            },
        },
        "ginger": {
            "Soft Rot": {
                "season": ["June", "July", "August"],
                "peak_months": ["July"],
                "risk_level": "HIGH",
            }
        },
    },

    # 27. Tumakuru
    "tumakuru": {
        "ragi": {
            "Blast": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "HIGH",
            }
        },
        "pigeon pea": {
            "Pod Borer": {
                "season": ["October", "November", "December"],
                "peak_months": ["November"],
                "risk_level": "MEDIUM",
            }
        },
        "tomato": {
            "Leaf Curl Virus": {
                "season": ["January", "February", "March"],
                "peak_months": ["February"],
                "risk_level": "HIGH",
            }
        },
    },

    # 28. Udupi
    "udupi": {
        "paddy": {
            "Blast": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
        "areca nut": {
            "Mite Infestation": {
                "season": ["February", "March"],
                "peak_months": ["March"],
                "risk_level": "HIGH",
            }
        },
        "coconut": {
            "Rhinoceros Beetle": {
                "season": ["June", "July", "August"],
                "peak_months": ["July"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 29. Uttara Kannada
    "uttara kannada": {
        "areca nut": {
            "Mite Infestation": {
                "season": ["February", "March", "April", "May"],
                "peak_months": ["March", "April"],
                "risk_level": "HIGH",
            },
            "Yellow Leaf Disease": {
                "season": ["June", "July", "August", "September"],
                "peak_months": ["July"],
                "risk_level": "MEDIUM",
            },
        },
        "pepper": {
            "Quick Wilt (Phytophthora Foot Rot)": {
                "season": ["June", "July", "August", "September"],
                "peak_months": ["July", "August"],
                "risk_level": "HIGH",
            },
            "Pollu Beetle": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            },
        },
        "paddy": {
            "Blast Disease": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
    },

    # 30. Yadgir
    "yadgir": {
        "pigeon pea": {
            "Pod Borer": {
                "season": ["October", "November"],
                "peak_months": ["November"],
                "risk_level": "HIGH",
            }
        },
        "paddy": {
            "Brown Planthopper": {
                "season": ["September", "October"],
                "peak_months": ["October"],
                "risk_level": "MEDIUM",
            }
        },
        "jowar": {
            "Shoot Fly": {
                "season": ["July", "August"],
                "peak_months": ["August"],
                "risk_level": "LOW",
            }
        },
    },

    # 31. Vijayanagara
    "vijayanagara": {
        "cotton": {
            "Pink Bollworm": {
                "season": ["September", "October", "November"],
                "peak_months": ["October"],
                "risk_level": "HIGH",
            }
        },
        "chilli": {
            "Thrips & Mite Complex": {
                "season": ["January", "February"],
                "peak_months": ["February"],
                "risk_level": "MEDIUM",
            }
        },
        "paddy": {
            "Stem Borer": {
                "season": ["August", "September"],
                "peak_months": ["September"],
                "risk_level": "MEDIUM",
            }
        },
    },
}
