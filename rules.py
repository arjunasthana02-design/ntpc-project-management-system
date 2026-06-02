import json

with open("ntpc_rules.json","r",encoding="utf8") as f:
    rules=json.load(f)

categories={

"Engineering":[
"staad","rcdc","load","wind","seismic",
"design","calculation","analysis",
"engineering","is875","is1893","is456"
],

"Layout":[
"layout","road","clearance",
"access","spacing","transformer",
"plot","distance","arrangement"
],

"Foundation":[
"foundation","pile","soil",
"sbc","footing","pedestal",
"anchor","excavation","grouting"
],

"Electrical":[
"electrical","cable","earthing",
"voltage","breaker","bus",
"transformer","ct","pt",
"switchyard"
],

"Structural":[
"beam","column","steel",
"structure","frame",
"bracing","member"
],

"Civil":[
"concrete","building",
"drain","wall",
"pavement","roadwork"
],

"Safety":[
"safety","fire","ppe",
"hazard","protection",
"emergency"
]

}

results={}

for category in categories:
    results[category]=[]

results["Others"]=[]


for rule in rules:

    found=False

    text=rule.lower()

    for category,words in categories.items():

        if any(word in text for word in words):

            results[category].append(rule)

            found=True
            break

    if not found:
        results["Others"].append(rule)


with open(
"categorized_rules.json",
"w",
encoding="utf8"
) as f:

    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )

for category in results:

    print(
    category,
    len(results[category])
    )