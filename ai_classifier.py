import json


CATEGORY_SAMPLES = {
    "Engineering": "engineering design calculation load wind seismic staad rcdc is456 is875 is1893",
    "Layout": "layout plot plan access road clearance spacing transformer yard cable routing equipment placement",
    "Foundation": "foundation footing pile raft pedestal anchor bolt geotechnical soil bearing capacity excavation rcc",
    "Electrical": "transformer switchyard breaker relay earthing cable inverter ht lt scada bus duct",
    "Structural": "beam column truss bracing steel frame purlin welding gusset base plate",
    "Civil": "concrete drainage road culvert retaining wall slab plinth pavement flooring building",
    "Safety": "fire extinguisher emergency ppe hazard escape route lightning protection first aid",
    "QAQC": "inspection quality assurance quality control test report procedure witness approval audit checklist",
    "Construction": "erection installation construction execution contractor site work sequence commissioning",
    "Documentation": "drawing datasheet calculation report document revision approval submission compliance sheet",
    "Solar": "solar module string inverter tracker dc ac photovoltaic pv module mounting structure",
    "SCADA": "scada communication ethernet plc control system networking protocol remote monitoring gateway",
    "Testing": "testing performance test inspection fat sat routine type commissioning validation",
}


def load_rules(path="ntpc_rules.json"):
    with open(path, "r", encoding="utf8") as file:
        return json.load(file)


def classify_rules(input_path="ntpc_rules.json", output_path="categorized_rules.json", threshold=0.23):
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError as exc:
        raise RuntimeError(
            "AI classifier requires sentence-transformers and scikit-learn. "
            "Install requirements.txt before running this utility."
        ) from exc

    print("Loading AI model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Loading extracted NTPC rules...")
    rules = load_rules(input_path)
    print("Total rules:", len(rules))

    print("Creating category embeddings...")
    category_embeddings = {
        category: model.encode(sample)
        for category, sample in CATEGORY_SAMPLES.items()
    }

    results = {category: [] for category in CATEGORY_SAMPLES}
    results["Others"] = []

    print("\nAI Classification Started...\n")
    for index, rule in enumerate(rules):
        try:
            rule_embedding = model.encode(rule)
            best_category = "Others"
            best_score = 0

            for category, embedding in category_embeddings.items():
                score = cosine_similarity([rule_embedding], [embedding])[0][0]
                if score > best_score:
                    best_score = score
                    best_category = category

            results[best_category if best_score > threshold else "Others"].append(rule)

            if index % 500 == 0:
                print(index, "rules processed")
        except Exception as exc:
            print("Classification skipped one rule:", exc)

    with open(output_path, "w", encoding="utf8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    return results


if __name__ == "__main__":
    classified = classify_rules()
    print("\n========== FINAL RESULT ==========\n")
    for category, rules in classified.items():
        print(category, len(rules))
