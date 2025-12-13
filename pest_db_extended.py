PEST_DB = {

    # ===================== COTTON =====================
    "cotton": {
        "Pink Bollworm": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["September", "October", "November"],
            "stage": ["flowering", "boll_development"],
            "soil": ["black soil", "red soil"],
            "symptoms": "Rosetted flowers, larvae feeding inside bolls",
            "preventive": "Use pheromone traps, resistant hybrids, timely sowing",
            "corrective": "Apply recommended insecticide at ETL"
        },
        "Whitefly & Viral Complex": {
            "temp_range": [25, 35],
            "humidity_gt": 55,
            "season": ["August", "September"],
            "stage": ["vegetative", "flowering"],
            "soil": ["black soil", "red soil"],
            "symptoms": "Leaf curling, yellowing, sticky honeydew",
            "preventive": "Avoid excess nitrogen, remove weeds",
            "corrective": "Spray selective systemic insecticide"
        }
    },

    # ===================== PADDY / RICE =====================
    "paddy": {
        "Blast Disease": {
            "temp_range": [18, 28],
            "humidity_gt": 85,
            "season": ["July", "August", "September"],
            "stage": ["tillering", "panicle_initiation"],
            "soil": ["clayey", "alluvial"],
            "symptoms": "Spindle shaped lesions on leaves and neck",
            "preventive": "Use resistant varieties, balanced fertilization",
            "corrective": "Spray tricyclazole fungicide"
        },
        "Brown Planthopper": {
            "temp_range": [25, 32],
            "humidity_gt": 70,
            "season": ["August", "September"],
            "stage": ["tillering", "grain_filling"],
            "soil": ["clayey", "alluvial"],
            "symptoms": "Hopper burn patches, yellowing",
            "preventive": "Avoid excess nitrogen, maintain spacing",
            "corrective": "Apply systemic insecticide"
        }
    },

    # ===================== MAIZE =====================
    "maize": {
        "Fall Armyworm": {
            "temp_range": [20, 32],
            "humidity_gt": 60,
            "season": ["June", "July", "August"],
            "stage": ["seedling", "vegetative"],
            "soil": ["red soil", "black soil"],
            "symptoms": "Shot holes in leaves, larvae in whorl",
            "preventive": "Early sowing, pheromone traps",
            "corrective": "Apply Spinosad or recommended insecticide"
        }
    },

    # ===================== SUGARCANE =====================
    "sugarcane": {
        "Early Shoot Borer": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["June", "July"],
            "stage": ["early_tillering"],
            "soil": ["alluvial", "black soil"],
            "symptoms": "Dead hearts in young crop",
            "preventive": "Trash mulching, resistant varieties",
            "corrective": "Apply granular insecticide in whorl"
        }
    },

    # ===================== GROUNDNUT =====================
    "groundnut": {
        "Leaf Spot & Rust": {
            "temp_range": [22, 30],
            "humidity_gt": 75,
            "season": ["August", "September"],
            "stage": ["vegetative", "flowering"],
            "soil": ["red soil", "sandy_loam"],
            "symptoms": "Brown spots on leaves, defoliation",
            "preventive": "Crop rotation, tolerant varieties",
            "corrective": "Spray mancozeb or chlorothalonil"
        }
    },

    # ===================== SOYBEAN =====================
    "soybean": {
        "Stem Fly": {
            "temp_range": [22, 32],
            "humidity_gt": 60,
            "season": ["July", "August"],
            "stage": ["vegetative"],
            "soil": ["black soil"],
            "symptoms": "Wilting, tunneling in stem",
            "preventive": "Early sowing, seed treatment",
            "corrective": "Apply systemic insecticide"
        }
    },

    # ===================== CHILLI =====================
    "chilli": {
        "Thrips & Mite Complex": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["January", "February", "March"],
            "stage": ["vegetative", "flowering"],
            "soil": ["red soil", "black soil"],
            "symptoms": "Leaf curling, silver streaks",
            "preventive": "Neem sprays, weed control",
            "corrective": "Apply selective acaricide"
        }
    },

    # ===================== TOMATO =====================
    "tomato": {
        "Leaf Curl Virus": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["December", "January", "February"],
            "stage": ["seedling", "vegetative"],
            "soil": ["red soil", "loamy"],
            "symptoms": "Severe leaf curling, stunting",
            "preventive": "Virus resistant hybrids",
            "corrective": "Control whitefly vector"
        }
    },

    # ===================== ONION =====================
    "onion": {
        "Thrips": {
            "temp_range": [24, 32],
            "humidity_gt": 50,
            "season": ["January", "February"],
            "stage": ["vegetative"],
            "soil": ["red soil", "loamy"],
            "symptoms": "Silvery streaks, drying tips",
            "preventive": "Reflective mulch, neem sprays",
            "corrective": "Apply selective insecticide"
        }
    },

    # ===================== RAGI =====================
    "ragi": {
        "Blast Disease": {
            "temp_range": [20, 28],
            "humidity_gt": 80,
            "season": ["August", "September"],
            "stage": ["tillering"],
            "soil": ["red soil"],
            "symptoms": "Diamond lesions on leaves",
            "preventive": "Balanced fertilization",
            "corrective": "Spray fungicide"
        }
    },

    # ===================== BANANA =====================
    "banana": {
        "Sigatoka Leaf Spot": {
            "temp_range": [24, 30],
            "humidity_gt": 80,
            "season": ["June", "July"],
            "stage": ["vegetative"],
            "soil": ["alluvial", "red soil"],
            "symptoms": "Yellow streaks on leaves",
            "preventive": "Good spacing, aeration",
            "corrective": "Spray fungicide"
        }
    },

    # ===================== ARECA NUT =====================
    "areca nut": {
        "Mite Infestation": {
            "temp_range": [28, 35],
            "humidity_lt": 60,
            "season": ["February", "March", "April"],
            "stage": ["fruiting"],
            "soil": ["laterite", "red soil"],
            "symptoms": "Shrivelled nuts, webbing",
            "preventive": "Maintain moisture",
            "corrective": "Spray neem oil or sulphur"
        }
    },

    # ===================== COFFEE =====================
    "coffee": {
        "Coffee Berry Borer": {
            "temp_range": [18, 28],
            "humidity_gt": 75,
            "season": ["August", "September"],
            "stage": ["berry_development"],
            "soil": ["laterite", "red soil"],
            "symptoms": "Bore holes in berries",
            "preventive": "Timely harvest",
            "corrective": "Apply biocontrol agents"
        }
    },

    # ===================== PEPPER =====================
    "pepper": {
        "Quick Wilt": {
            "temp_range": [20, 28],
            "humidity_gt": 85,
            "season": ["June", "July"],
            "stage": ["vegetative"],
            "soil": ["laterite"],
            "symptoms": "Sudden wilting",
            "preventive": "Good drainage",
            "corrective": "Soil drenching"
        }
    },

    # ===================== GRAPES =====================
    "grapes": {
        "Downy Mildew": {
            "temp_range": [18, 26],
            "humidity_gt": 85,
            "season": ["July", "August"],
            "stage": ["vegetative"],
            "soil": ["black soil", "red soil"],
            "symptoms": "Oil spots on leaves",
            "preventive": "Canopy management",
            "corrective": "Spray fungicide"
        }
    },

    # ===================== POMEGRANATE =====================
    "pomegranate": {
        "Bacterial Blight": {
            "temp_range": [24, 32],
            "humidity_gt": 70,
            "season": ["July", "August"],
            "stage": ["fruiting"],
            "soil": ["black soil"],
            "symptoms": "Cracked oozing fruits",
            "preventive": "Sanitation, pruning",
            "corrective": "Spray copper fungicide"
        }
    },

    # ===================== MANGO =====================
    "mango": {
        "Powdery Mildew": {
            "temp_range": [18, 28],
            "humidity_gt": 70,
            "season": ["January", "February"],
            "stage": ["flowering"],
            "soil": ["red soil"],
            "symptoms": "White powder on flowers",
            "preventive": "Pruning",
            "corrective": "Spray sulphur"
        }
    },
    "pigeon pea": {
        "Pod Borer": {
            "temp_range": [25, 35],
            "humidity_gt": 60,
            "season": ["September", "October"],
            "stage": ["flowering", "pod_formation"],
            "soil": ["black soil", "red soil"],
            "symptoms": "Holes in pods, larvae feeding on seeds",
            "preventive": "Use pheromone traps, early sowing",
            "corrective": "Apply recommended insecticide at ETL"
        }
    },
    
    "green gram": {
        "Yellow Mosaic Virus": {
            "temp_range": [25, 35],
            "humidity_gt": 60,
            "season": ["August", "September"],
            "stage": ["vegetative"],
            "soil": ["red soil"],
            "symptoms": "Yellow patches on leaves, stunted growth",
            "preventive": "Use resistant varieties",
            "corrective": "Control whitefly vector"
        }
    },
    
    "black gram": {
        "Leaf Curl & Mosaic": {
            "temp_range": [25, 35],
            "humidity_gt": 60,
            "season": ["August", "September"],
            "stage": ["vegetative"],
            "soil": ["red soil"],
            "symptoms": "Leaf curling, yellowing",
            "preventive": "Seed treatment, weed control",
            "corrective": "Spray systemic insecticide"
        }
    },
    
    "bengal gram": {
        "Gram Pod Borer": {
            "temp_range": [20, 30],
            "humidity_gt": 55,
            "season": ["December", "January"],
            "stage": ["flowering", "pod_formation"],
            "soil": ["black soil"],
            "symptoms": "Damaged pods, larvae inside",
            "preventive": "Deep summer ploughing",
            "corrective": "Spray recommended insecticide"
        }
    },
    
    "horse gram": {
        "Leaf Spot": {
            "temp_range": [22, 30],
            "humidity_gt": 65,
            "season": ["September"],
            "stage": ["vegetative"],
            "soil": ["red soil"],
            "symptoms": "Brown spots on leaves",
            "preventive": "Crop rotation",
            "corrective": "Spray fungicide"
        }
    },
    
    "cowpea": {
        "Aphid Infestation": {
            "temp_range": [25, 32],
            "humidity_gt": 60,
            "season": ["August", "September"],
            "stage": ["vegetative"],
            "soil": ["red soil"],
            "symptoms": "Sticky honeydew, leaf curling",
            "preventive": "Neem oil spray",
            "corrective": "Apply systemic insecticide"
        }
    },
    "sunflower": {
        "Head Rot": {
            "temp_range": [20, 28],
            "humidity_gt": 75,
            "season": ["September"],
            "stage": ["flowering"],
            "soil": ["black soil"],
            "symptoms": "Rotting of flower head",
            "preventive": "Avoid water stagnation",
            "corrective": "Spray fungicide"
        }
    },
    
    "sesame": {
        "Phyllody Disease": {
            "temp_range": [25, 35],
            "humidity_gt": 60,
            "season": ["August"],
            "stage": ["flowering"],
            "soil": ["red soil"],
            "symptoms": "Flowers turn leafy",
            "preventive": "Vector control",
            "corrective": "Rogue infected plants"
        }
    },
    
    "castor": {
        "Semilooper": {
            "temp_range": [25, 32],
            "humidity_gt": 60,
            "season": ["August", "September"],
            "stage": ["vegetative"],
            "soil": ["black soil"],
            "symptoms": "Defoliation",
            "preventive": "Encourage natural enemies",
            "corrective": "Apply biopesticide"
        }
    },
    
    "safflower": {
        "Aphid": {
            "temp_range": [20, 30],
            "humidity_gt": 55,
            "season": ["December", "January"],
            "stage": ["vegetative"],
            "soil": ["black soil"],
            "symptoms": "Curling and yellowing",
            "preventive": "Early sowing",
            "corrective": "Spray insecticide"
        }
    },
    "tobacco": {
            "Leaf Curl Virus": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["January", "February"],
            "stage": ["vegetative"],
            "soil": ["red soil"],
            "symptoms": "Leaf curling, stunted growth",
            "preventive": "Vector control",
            "corrective": "Spray insecticide"
        }
    },
    "coconut": {
            "Rhinoceros Beetle": {
            "temp_range": [25, 35],
            "humidity_gt": 70,
            "season": ["May", "June"],
            "stage": ["vegetative"],
            "soil": ["laterite"],
            "symptoms": "V-shaped cuts on leaves",
            "preventive": "Destroy breeding sites",
            "corrective": "Apply neem-based formulations"
        }
    },

    "arecanut": {
            "Yellow Leaf Disease": {
            "temp_range": [20, 30],
            "humidity_gt": 80,
            "season": ["June", "July"],
            "stage": ["vegetative"],
            "soil": ["laterite"],
            "symptoms": "Yellowing of midrib",
            "preventive": "Good drainage",
            "corrective": "Balanced nutrition"
        }
    },

    "cashew": {
        "Tea Mosquito Bug": {
            "temp_range": [25, 32],
            "humidity_gt": 60,
            "season": ["December", "January"],
            "stage": ["flowering"],
            "soil": ["laterite"],
            "symptoms": "Necrotic lesions on shoots",
            "preventive": "Pruning",
            "corrective": "Spray recommended insecticide"
        }
    },

    "rubber": {
        "Powdery Mildew": {
            "temp_range": [20, 28],
            "humidity_gt": 80,
            "season": ["July"],
            "stage": ["leaf_fall"],
            "soil": ["laterite"],
            "symptoms": "White powdery growth",
            "preventive": "Improve aeration",
            "corrective": "Spray fungicide"
        }
    },
    "papaya": {
        "Ring Spot Virus": {
            "temp_range": [25, 35],
            "humidity_gt": 60,
            "season": ["March", "April"],
            "stage": ["vegetative"],
            "soil": ["red soil"],
            "symptoms": "Ring spots on leaves",
            "preventive": "Resistant varieties",
            "corrective": "Remove infected plants"
        }
    },
    
    "guava": {
        "Fruit Fly": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["April", "May"],
            "stage": ["fruiting"],
            "soil": ["red soil"],
            "symptoms": "Maggots inside fruit",
            "preventive": "Bagging fruits",
            "corrective": "Use bait traps"
        }
    },
    
    "sapota": {
        "Bud Borer": {
            "temp_range": [25, 32],
            "humidity_gt": 60,
            "season": ["January"],
            "stage": ["flowering"],
            "soil": ["red soil"],
            "symptoms": "Damaged buds",
            "preventive": "Pruning",
            "corrective": "Spray insecticide"
        }
    },
    
    "orange": {
        "Citrus Psylla": {
            "temp_range": [22, 32],
            "humidity_gt": 60,
            "season": ["February", "March"],
            "stage": ["vegetative"],
            "soil": ["red soil"],
            "symptoms": "Leaf curling, sooty mold",
            "preventive": "Neem oil spray",
            "corrective": "Apply insecticide"
        }
    },
        "brinjal": {
        "Shoot & Fruit Borer": {
            "temp_range": [25, 32],
            "humidity_gt": 60,
            "season": ["August", "September"],
            "stage": ["flowering", "fruiting"],
            "soil": ["red soil"],
            "symptoms": "Holes in fruits",
            "preventive": "Remove affected shoots",
            "corrective": "Apply insecticide"
        }
    },
    
    "cabbage": {
        "Diamond Back Moth": {
            "temp_range": [20, 30],
            "humidity_gt": 60,
            "season": ["December"],
            "stage": ["vegetative"],
            "soil": ["loamy"],
            "symptoms": "Window pane damage",
            "preventive": "Net covering",
            "corrective": "Apply biopesticide"
        }
    },
    
    "cauliflower": {
        "Curd Rot": {
            "temp_range": [18, 25],
            "humidity_gt": 80,
            "season": ["January"],
            "stage": ["curd_formation"],
            "soil": ["loamy"],
            "symptoms": "Brown curd",
            "preventive": "Avoid water stagnation",
            "corrective": "Spray fungicide"
        }
    },
    
    "beans": {
        "Pod Borer": {
            "temp_range": [22, 30],
            "humidity_gt": 60,
            "season": ["September"],
            "stage": ["flowering"],
            "soil": ["red soil"],
            "symptoms": "Damaged pods",
            "preventive": "Timely harvesting",
            "corrective": "Apply insecticide"
        }
    },
    
    "cucumber": {
        "Downy Mildew": {
            "temp_range": [18, 25],
            "humidity_gt": 85,
            "season": ["July"],
            "stage": ["vegetative"],
            "soil": ["loamy"],
            "symptoms": "Yellow patches on leaves",
            "preventive": "Good ventilation",
            "corrective": "Spray fungicide"
        }
    },
    
    "turmeric": {
        "Rhizome Rot": {
            "temp_range": [24, 30],
            "humidity_gt": 80,
            "season": ["July"],
            "stage": ["vegetative"],
            "soil": ["red soil"],
            "symptoms": "Yellowing, rotting rhizomes",
            "preventive": "Raised beds",
            "corrective": "Soil drenching"
        }
    },
    
    "ginger": {
        "Soft Rot": {
            "temp_range": [24, 30],
            "humidity_gt": 85,
            "season": ["June"],
            "stage": ["vegetative"],
            "soil": ["loamy"],
            "symptoms": "Soft watery rot",
            "preventive": "Good drainage",
            "corrective": "Apply fungicide"
        }
    },
    
    "coriander": {
        "Powdery Mildew": {
            "temp_range": [18, 25],
            "humidity_gt": 70,
            "season": ["January"],
            "stage": ["vegetative"],
            "soil": ["loamy"],
            "symptoms": "White powdery growth",
            "preventive": "Spacing",
            "corrective": "Spray sulphur"
        }
    },
    
    "cardamom": {
        "Capsule Rot": {
            "temp_range": [18, 28],
            "humidity_gt": 85,
            "season": ["July"],
            "stage": ["fruiting"],
            "soil": ["laterite"],
            "symptoms": "Rotting capsules",
            "preventive": "Shade regulation",
            "corrective": "Spray fungicide"
        }
    }
}
