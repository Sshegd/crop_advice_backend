# pest_db_extended.py
# ---------------------------------------------------------
# ICAR-style Karnataka Pest & Disease Knowledge Base
# 20 major crops, each with key pests/diseases.
# Keys are designed to work with PestEngine.evaluate_rule()
# ---------------------------------------------------------

PEST_DB = {

    # =====================================================
    # 1. ARECA NUT
    # =====================================================
    "areca nut": {
        "Mite Infestation": {
            "temp_gt": 30,
            "humidity_lt": 60,
            "rainfall_range": [0, 1200],
            "season": ["February", "March", "April", "May"],
            "stage": ["young", "vegetative", "fruiting"],
            "soil": ["red soil", "laterite"],
            "symptoms": "Brown, shrivelled nuts; rough husk; webbing on bunches.",
            "preventive": "Maintain regular irrigation during summer; avoid moisture stress; maintain field sanitation and remove heavily infested bunches.",
            "corrective": "Spray neem oil 0.5% or wettable sulphur; repeat at 20–25 day interval if infestation continues."
        },
        "Yellow Leaf Disease": {
            "temp_range": [20, 30],
            "humidity_gt": 80,
            "rainfall_range": [1800, 3500],
            "season": ["June", "July", "August", "September"],
            "stage": ["vegetative"],
            "soil": ["laterite", "red soil"],
            "symptoms": "Yellowing of midrib region, drooping leaves, stunted palms.",
            "preventive": "Ensure good drainage, avoid water stagnation, apply lime in acidic soils, use disease-free seedlings.",
            "corrective": "Apply recommended dose of NPK with organic manures; root feeding with plant tonics and Trichoderma; remove severely affected palms."
        }
    },

    # =====================================================
    # 2. PADDY (RICE)
    # =====================================================
    "paddy": {
        "Blast Disease": {
            "temp_range": [18, 28],
            "humidity_gt": 85,
            "rainfall_range": [800, 2000],
            "season": ["July", "August", "September"],
            "stage": ["nursery", "tillering", "panicle_initiation"],
            "soil": ["alluvial", "clayey"],
            "symptoms": "Spindle-shaped spots with grey centre on leaves and neck blast at panicle.",
            "preventive": "Use resistant varieties, avoid excessive nitrogen, maintain optimum plant spacing and proper water management.",
            "corrective": "Spray tricyclazole or equivalent fungicide at recommended dose at first appearance and repeat within 10–12 days."
        },
        "Brown Planthopper": {
            "temp_range": [25, 32],
            "humidity_gt": 70,
            "rainfall_range": [900, 2500],
            "season": ["August", "September", "October"],
            "stage": ["tillering", "panicle_initiation", "grain_filling"],
            "soil": ["alluvial", "clayey"],
            "symptoms": "Hopperburn patches, yellowing then drying of whole clumps; insects seen at base of plants.",
            "preventive": "Avoid indiscriminate insecticide use, maintain optimum plant density, keep 2–3 dry days by draining water during early infestation.",
            "corrective": "Apply recommended systemic insecticide as whorl or root zone application; avoid spraying in late evening when natural enemies are active."
        }
    },

    # =====================================================
    # 3. BANANA
    # =====================================================
    "banana": {
        "Sigatoka Leaf Spot": {
            "temp_range": [24, 30],
            "humidity_gt": 80,
            "rainfall_range": [1200, 3000],
            "season": ["June", "July", "August", "September"],
            "stage": ["vegetative", "fruiting"],
            "soil": ["red soil", "alluvial"],
            "symptoms": "Small yellow streaks on leaves which turn brown and coalesce; drying of leaf lamina.",
            "preventive": "Ensure wider spacing and good aeration, remove and destroy severely infected leaves, avoid overhead irrigation.",
            "corrective": "Spray mancozeb or systemic fungicide alternately at 20–25 day interval during rainy season."
        },
        "Panama Wilt": {
            "temp_range": [25, 32],
            "rainfall_range": [1000, 2500],
            "season": ["July", "August", "September"],
            "stage": ["vegetative", "fruiting"],
            "soil": ["sandy_loam", "red soil"],
            "symptoms": "Yellowing of lower leaves, petiole breaking, internal vascular browning of pseudostem.",
            "preventive": "Use disease-free suckers, adopt crop rotation with non-host crops, avoid waterlogging.",
            "corrective": "Drench soil with recommended fungicide around affected clumps; remove and destroy severely affected mats."
        }
    },

    # =====================================================
    # 4. SUGARCANE
    # =====================================================
    "sugarcane": {
        "Early Shoot Borer": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "rainfall_range": [700, 1400],
            "season": ["June", "July", "August"],
            "stage": ["early_tillering"],
            "soil": ["alluvial", "black soil"],
            "symptoms": "Dead-hearts in early crop, central shoot dries while outer leaves remain green.",
            "preventive": "Trash mulching, use of resistant varieties, avoid late planting.",
            "corrective": "Release Trichogramma egg parasitoids or apply granular insecticide in leaf whorl at recommended dose."
        },
        "Red Rot": {
            "temp_range": [24, 30],
            "rainfall_range": [900, 1500],
            "season": ["July", "August", "September"],
            "stage": ["grand_growth"],
            "soil": ["alluvial", "black soil"],
            "symptoms": "Red discoloration of internal tissues with white patches and fermenting smell, drying of canes.",
            "preventive": "Plant only disease-free setts, treat seed with fungicide before planting, follow crop rotation.",
            "corrective": "Rogue out affected clumps completely and destroy; avoid ratooning in badly affected fields."
        }
    },

    # =====================================================
    # 5. MAIZE
    # =====================================================
    "maize": {
        "Fall Armyworm": {
            "temp_range": [20, 32],
            "humidity_gt": 60,
            "rainfall_range": [700, 1200],
            "season": ["June", "July", "August", "September"],
            "stage": ["seedling", "vegetative"],
            "soil": ["red soil", "black soil"],
            "symptoms": "Shot holes in young leaves, window-pane damage, larvae present inside whorl and on cobs.",
            "preventive": "Timely sowing, avoid staggered planting, install pheromone traps, encourage natural enemies.",
            "corrective": "Apply recommended biopesticides (Spinosad, Metarhizium etc.) or selective insecticides in whorl as per guidelines."
        },
        "Turcicum Leaf Blight": {
            "temp_range": [18, 28],
            "humidity_gt": 80,
            "season": ["August", "September"],
            "stage": ["vegetative", "tasseling"],
            "soil": ["red soil", "alluvial"],
            "symptoms": "Long elliptical grey-green lesions on leaves that turn brown and coalesce.",
            "preventive": "Use resistant hybrids, avoid dense sowing and continuous maize cropping, follow balanced fertilization.",
            "corrective": "Spray appropriate fungicide at first appearance and repeat after 12–15 days if needed."
        }
    },

    # =====================================================
    # 6. GROUNDNUT
    # =====================================================
    "groundnut": {
        "Leaf Spot & Rust": {
            "temp_range": [22, 30],
            "humidity_gt": 75,
            "rainfall_range": [600, 1200],
            "season": ["August", "September", "October"],
            "stage": ["vegetative", "flowering"],
            "soil": ["red soil", "sandy_loam"],
            "symptoms": "Brown necrotic spots on leaves, orange pustules on underside, early defoliation.",
            "preventive": "Use tolerant varieties, practice crop rotation, remove volunteer plants.",
            "corrective": "Spray chlorothalonil or mancozeb followed by systemic fungicide at recommended intervals."
        },
        "Aphid & Jassid Complex": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["July", "August", "September"],
            "stage": ["vegetative", "flowering"],
            "soil": ["red soil", "sandy_loam"],
            "symptoms": "Yellowing and curling of leaves, sticky honeydew, presence of small insects on underside.",
            "preventive": "Avoid excess nitrogen, use border crops like sorghum, apply neem seed kernel extract.",
            "corrective": "Spray selective systemic insecticide if population crosses economic threshold level."
        }
    },

    # =====================================================
    # 7. COTTON
    # =====================================================
    "cotton": {
        "Pink Bollworm": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["September", "October", "November"],
            "stage": ["flowering", "boll_development"],
            "soil": ["black soil", "red soil"],
            "symptoms": "Rosetted flowers, premature boll opening, larvae feeding inside bolls.",
            "preventive": "Adopt timely sowing, use PBW-resistant hybrids, destroy unopened bolls after harvest, use pheromone traps.",
            "corrective": "Apply recommended insecticide at peak flowering and boll formation based on trap catches and ETL."
        },
        "Whitefly & Viral Complex": {
            "temp_range": [25, 35],
            "humidity_gt": 60,
            "season": ["August", "September"],
            "stage": ["vegetative", "flowering"],
            "soil": ["black soil", "red soil"],
            "symptoms": "Yellowing and curling of leaves, stunted plants, sticky honeydew and sooty mould.",
            "preventive": "Avoid excessive nitrogen, remove weed hosts, do not grow cotton continuously on same land.",
            "corrective": "Spray recommended selective insecticide, avoid repeated use of same molecule."
        }
    },

    # =====================================================
    # 8. RAGI (FINGER MILLET)
    # =====================================================
    "ragi": {
        "Blast Disease": {
            "temp_range": [20, 28],
            "humidity_gt": 80,
            "rainfall_range": [600, 1100],
            "season": ["August", "September"],
            "stage": ["tillering", "ear_head"],
            "soil": ["red soil", "laterite"],
            "symptoms": "Diamond-shaped lesions on leaves and neck; shrivelled ear heads.",
            "preventive": "Use tolerant varieties, avoid excess nitrogen, maintain proper spacing.",
            "corrective": "Spray tricyclazole or equivalent fungicide at boot leaf and repeat at ear emergence."
        }
    },

    # =====================================================
    # 9. TURMERIC
    # =====================================================
    "turmeric": {
        "Rhizome Rot": {
            "temp_range": [24, 30],
            "humidity_gt": 80,
            "rainfall_range": [900, 1800],
            "season": ["July", "August", "September"],
            "stage": ["vegetative"],
            "soil": ["red soil", "loamy"],
            "symptoms": "Yellowing and drooping of leaves, soft rotting of rhizomes with foul smell.",
            "preventive": "Use well-drained beds, treat seed rhizomes with fungicide and Trichoderma, avoid water stagnation.",
            "corrective": "Drench soil around affected clumps with recommended systemic fungicide."
        },
        "Leaf Spot": {
            "temp_range": [22, 30],
            "humidity_gt": 75,
            "season": ["August", "September"],
            "stage": ["vegetative"],
            "soil": ["red soil", "loamy"],
            "symptoms": "Small brown spots on leaves that coalesce and cause blighting.",
            "preventive": "Adequate spacing, balanced fertilization, removal of severely infected leaves.",
            "corrective": "Spray mancozeb or copper fungicides at recommended interval."
        }
    },

    # =====================================================
    # 10. GINGER
    # =====================================================
    "ginger": {
        "Soft Rot": {
            "temp_range": [24, 30],
            "humidity_gt": 85,
            "rainfall_range": [1200, 2500],
            "season": ["June", "July", "August"],
            "stage": ["vegetative"],
            "soil": ["red soil", "loamy"],
            "symptoms": "Sudden yellowing and dropping of leaves, soft watery decay of rhizomes.",
            "preventive": "Use raised beds, treat seed rhizomes with fungicide and biocontrol agents, avoid waterlogging.",
            "corrective": "Drench around base with suitable fungicide; remove affected clumps to prevent spread."
        }
    },

    # =====================================================
    # 11. PEPPER
    # =====================================================
    "pepper": {
        "Quick Wilt (Phytophthora Foot Rot)": {
            "temp_range": [20, 28],
            "humidity_gt": 85,
            "rainfall_range": [2000, 3500],
            "season": ["June", "July", "August", "September"],
            "stage": ["vegetative", "fruiting"],
            "soil": ["laterite", "red soil"],
            "symptoms": "Sudden wilting and yellowing of vines, blackening of leaves and spikes.",
            "preventive": "Provide good drainage, avoid water stagnation around vines, apply Trichoderma enriched FYM.",
            "corrective": "Apply recommended systemic fungicide as soil drench and foliar spray at onset of monsoon."
        },
        "Pollu Beetle": {
            "temp_range": [22, 30],
            "rainfall_range": [1500, 3000],
            "season": ["July", "August", "September"],
            "stage": ["flowering", "berry_development"],
            "soil": ["laterite", "red soil"],
            "symptoms": "Galleries on berries, hollow or dried berries, heavy shedding.",
            "preventive": "Keep vines well pruned and open; collect and destroy fallen berries.",
            "corrective": "Spray recommended insecticide targeting berry clusters at early stage."
        }
    },

    # =====================================================
    # 12. COFFEE
    # =====================================================
    "coffee": {
        "Coffee Berry Borer": {
            "temp_range": [18, 28],
            "humidity_gt": 75,
            "rainfall_range": [1500, 2500],
            "season": ["August", "September", "October"],
            "stage": ["berry_development", "ripening"],
            "soil": ["laterite", "red soil"],
            "symptoms": "Small round hole at tip of berries; damaged beans inside.",
            "preventive": "Timely and complete harvest, strip picking of leftover berries, use of pheromone traps.",
            "corrective": "Apply biocontrol agents like Beauveria and follow need-based insecticide application."
        },
        "Leaf Rust": {
            "temp_range": [20, 26],
            "humidity_gt": 80,
            "season": ["July", "August", "September"],
            "stage": ["vegetative"],
            "soil": ["laterite", "red soil"],
            "symptoms": "Orange powdery pustules on underside of leaves leading to defoliation.",
            "preventive": "Grow rust resistant varieties, maintain adequate shade management and nutrition.",
            "corrective": "Spray copper-based fungicides or systemic fungicides at recommended dose."
        }
    },

    # =====================================================
    # 13. SUNFLOWER
    # =====================================================
    "sunflower": {
        "Downy Mildew": {
            "temp_range": [18, 25],
            "humidity_gt": 85,
            "season": ["July", "August"],
            "stage": ["seedling", "vegetative"],
            "soil": ["black soil", "red soil"],
            "symptoms": "Chlorotic leaves with downy growth on underside; stunting.",
            "preventive": "Use certified treated seeds, follow crop rotation, avoid low-lying fields.",
            "corrective": "Spray recommended systemic fungicide at first appearance of symptoms."
        },
        "Helicoverpa Pod Borer": {
            "temp_range": [22, 32],
            "season": ["September", "October"],
            "stage": ["flowering", "head_stage"],
            "soil": ["black soil", "red soil"],
            "symptoms": "Larvae feeding on heads and seeds causing chaffy heads.",
            "preventive": "Install pheromone traps, use bird perches, sow early recommended hybrids.",
            "corrective": "Need-based application of selective insecticide when larval population crosses ETL."
        }
    },

    # =====================================================
    # 14. CHILLI
    # =====================================================
    "chilli": {
        "Fruit Rot & Dieback (Anthracnose)": {
            "temp_range": [24, 30],
            "humidity_gt": 85,
            "rainfall_range": [900, 1800],
            "season": ["August", "September", "October"],
            "stage": ["flowering", "fruiting"],
            "soil": ["red soil", "black soil"],
            "symptoms": "Circular sunken lesions with concentric rings on fruits; dieback of twigs.",
            "preventive": "Use disease-free seed, follow crop rotation, avoid overhead irrigation and water splash.",
            "corrective": "Spray recommended fungicide starting at fruit set stage at 10–12 day interval."
        },
        "Thrips & Mite Complex": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["January", "February", "March", "October", "November"],
            "stage": ["vegetative", "flowering"],
            "soil": ["red soil", "black soil"],
            "symptoms": "Upward curling and crinkling of leaves, silvering, stunted plants.",
            "preventive": "Remove alternate weed hosts, reflective mulches can help, apply neem-based sprays.",
            "corrective": "Apply selective insecticide/acaricide as per ETL and rotate molecules to avoid resistance."
        }
    },

    # =====================================================
    # 15. TOMATO
    # =====================================================
    "tomato": {
        "Tomato Leaf Curl Virus (Whitefly Transmitted)": {
            "temp_range": [24, 32],
            "humidity_gt": 60,
            "season": ["December", "January", "February", "March"],
            "stage": ["seedling", "vegetative"],
            "soil": ["red soil", "loamy"],
            "symptoms": "Severe leaf curling, stunting, pale yellow foliage and poor fruit set.",
            "preventive": "Use virus-tolerant hybrids, raise nursery under insect-proof net, remove infected plants, control whitefly.",
            "corrective": "Spray recommended systemic insecticides against whitefly and use yellow sticky traps."
        },
        "Early Blight": {
            "temp_range": [20, 28],
            "humidity_gt": 80,
            "season": ["July", "August", "September"],
            "stage": ["vegetative", "fruiting"],
            "soil": ["red soil", "loamy"],
            "symptoms": "Concentric brown rings on older leaves, defoliation and fruit infection.",
            "preventive": "Follow crop rotation, avoid overhead irrigation, maintain good staking and spacing.",
            "corrective": "Spray mancozeb or chlorothalonil alternated with systemic fungicide at recommended intervals."
        }
    },

    # =====================================================
    # 16. POTATO
    # =====================================================
    "potato": {
        "Late Blight": {
            "temp_range": [16, 22],
            "humidity_gt": 85,
            "season": ["December", "January", "February"],
            "stage": ["vegetative", "tuber_bulking"],
            "soil": ["loamy", "alluvial"],
            "symptoms": "Water-soaked lesions on leaves and stems, white fungal growth at margins, tuber rot.",
            "preventive": "Use healthy seed tubers, provide adequate ridging, avoid irrigation during late evening.",
            "corrective": "Prophylactic spray of protective fungicides followed by systemic fungicides as per disease forecast."
        },
        "Aphid Transmitted Viruses": {
            "temp_range": [18, 28],
            "humidity_gt": 60,
            "season": ["January", "February", "March"],
            "stage": ["vegetative"],
            "soil": ["loamy", "alluvial"],
            "symptoms": "Mosaic, leaf rolling, stunting; high incidence in seed plots.",
            "preventive": "Use virus-free seed, rogue out infected plants early, manage aphid population with yellow traps.",
            "corrective": "Need-based application of selective insecticide to manage vector population."
        }
    },

    # =====================================================
    # 17. ONION
    # =====================================================
    "onion": {
        "Purple Blotch": {
            "temp_range": [20, 30],
            "humidity_gt": 80,
            "season": ["August", "September", "October"],
            "stage": ["vegetative", "bulb_formation"],
            "soil": ["red soil", "loamy"],
            "symptoms": "Purple concentric rings on leaves and seed stalks leading to drying from tips.",
            "preventive": "Use wide spacing, avoid waterlogging and overhead irrigation, ensure good air movement.",
            "corrective": "Spray protective fungicides followed by systemic fungicides at 10–12 day interval."
        },
        "Thrips": {
            "temp_range": [24, 32],
            "humidity_gt": 50,
            "season": ["January", "February", "March"],
            "stage": ["vegetative", "bulb_formation"],
            "soil": ["red soil", "loamy"],
            "symptoms": "Silvery streaks on leaves, curling and drying from tips, reduced bulb size.",
            "preventive": "Irrigate through furrows to reduce thrips, use reflective mulches, apply neem-based sprays.",
            "corrective": "Apply selective insecticide at ETL and alternate molecules."
        }
    },

    # =====================================================
    # 18. MANGO
    # =====================================================
    "mango": {
        "Powdery Mildew": {
            "temp_range": [18, 28],
            "humidity_gt": 70,
            "season": ["January", "February", "March"],
            "stage": ["flowering", "fruit_set"],
            "soil": ["red soil", "laterite"],
            "symptoms": "White powdery growth on panicles and young fruits causing flower drop.",
            "preventive": "Maintain tree canopy by pruning, avoid overcrowding, provide adequate nutrition.",
            "corrective": "Spray wettable sulphur or systemic fungicides at flower initiation and repeat as necessary."
        },
        "Fruit Fly": {
            "temp_range": [24, 32],
            "season": ["April", "May", "June"],
            "stage": ["fruit_development", "ripening"],
            "soil": ["red soil", "laterite"],
            "symptoms": "Oozing of sap from punctured fruits, internal maggots feeding on pulp, premature fruit drop.",
            "preventive": "Collect and destroy fallen fruits, use bait traps and pheromone traps, bag individual fruits if feasible.",
            "corrective": "Apply bait sprays using recommended insecticides and protein sources around tree canopy as per guidelines."
        }
    },

    # =====================================================
    # 19. GRAPES
    # =====================================================
    "grapes": {
        "Downy Mildew": {
            "temp_range": [18, 26],
            "humidity_gt": 85,
            "rainfall_range": [700, 1200],
            "season": ["July", "August", "September"],
            "stage": ["vegetative", "flowering"],
            "soil": ["red soil", "black soil"],
            "symptoms": "Yellow oil spots on upper leaf surface and white downy growth beneath; flower and berry infection.",
            "preventive": "Maintain open canopy with good air circulation, avoid overhead irrigation, remove basal leaves touching soil.",
            "corrective": "Spray protective fungicides followed by systemic fungicides as per advisory schedule."
        },
        "Powdery Mildew": {
            "temp_range": [20, 30],
            "humidity_gt": 60,
            "season": ["December", "January", "February"],
            "stage": ["flowering", "berry_development"],
            "soil": ["red soil", "black soil"],
            "symptoms": "White powdery growth on leaves, bunches and shoots; cracking of berries.",
            "preventive": "Maintain balanced nutrition, avoid excess nitrogen, ensure proper pruning and training.",
            "corrective": "Spray sulphur or other recommended fungicides at early appearance and repeat as required."
        }
    },

    # =====================================================
    # 20. POMEGRANATE
    # =====================================================
    "pomegranate": {
        "Bacterial Blight": {
            "temp_range": [24, 32],
            "humidity_gt": 70,
            "rainfall_range": [600, 900],
            "season": ["July", "August", "September"],
            "stage": ["vegetative", "fruiting"],
            "soil": ["red soil", "black soil"],
            "symptoms": "Water-soaked spots on leaves, stems and fruits; cracked and oozing fruits.",
            "preventive": "Adopt bahar manipulation to avoid high rainfall flowering, maintain field sanitation and pruning, avoid overhead irrigation.",
            "corrective": "Spray combination of copper fungicides and antibiotics as per university recommendations; remove infected twigs and fruits."
        },
        "Fruit Borer": {
            "temp_range": [24, 32],
            "season": ["August", "September", "October"],
            "stage": ["fruit_development"],
            "soil": ["red soil", "black soil"],
            "symptoms": "Bore holes on fruits, frass extrusion, internal feeding leading to rotting.",
            "preventive": "Use light traps and pheromone traps, bag fruits with suitable covers, remove infested fruits.",
            "corrective": "Need-based application of recommended insecticides during fruit development stage."
        }
    },
}
