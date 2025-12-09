PEST_DB = {
    "areca nut": {
        "Mite Infestation": {
            "temp_gt": 30,
            "humidity_lt": 60,
            "rainfall_lt": 1000,
            "season": ["February", "March", "April"],
            "stage": ["pre_planting", "planting_cultivation", "fruiting"],
            "symptoms": "Brown nuts, rough husk, webbing.",
            "preventive": "Maintain irrigation, avoid drought stress.",
            "corrective": "Spray neem oil 0.5% or sulphur dust."
        },
        "Yellow Leaf Disease": {
            "rainfall_gt": 1800,
            "humidity_gt": 80,
            "season": ["July", "August", "September"],
            "stage": ["vegetative"],
            "symptoms": "Midrib yellowing, leaf drooping.",
            "preventive": "Improve drainage, apply lime.",
            "corrective": "Trichoderma root feeding + Bordeaux spray."
        }
    },

    "paddy": {
        "Blast Disease": {
            "humidity_gt": 85,
            "temp_range": [18, 28],
            "season": ["July", "August", "September"],
            "symptoms": "Spindle-shaped leaf lesions.",
            "preventive": "Avoid excess nitrogen, maintain spacing.",
            "corrective": "Spray tricyclazole 0.6 gm/ltr."
        }
    }
}
