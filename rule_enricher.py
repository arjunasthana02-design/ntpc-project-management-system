import json
import re

print("Loading rules...")

with open(
    "clean_rules.json",
    "r",
    encoding="utf8"
) as f:

    rules=json.load(f)


enhanced=[]

for i,rule in enumerate(rules):

    text=rule.lower()

    category="Others"


    if any(x in text for x in
    ["wind","load","staad","design"]):

        category="Engineering"


    elif any(x in text for x in
    ["layout","clearance","spacing"]):

        category="Layout"


    elif any(x in text for x in
    ["foundation","pile","footing","soil"]):

        category="Foundation"


    severity="Low"


    if any(x in text for x in
    ["shall","mandatory","must","required"]):

        severity="Critical"

    elif any(x in text for x in
    ["should","recommended"]):

        severity="Medium"


    page=i//10+1


    clause="Unknown"


    m=re.search(
        r'([A-Z]-\d+)',
        rule
    )

    if m:

        clause=m.group()


    obj={

        "id":i,

        "rule":rule,

        "category":category,

        "severity":severity,

        "page":page,

        "clause":clause,

        "source":"NTPC Section VI"

    }

    enhanced.append(obj)


with open(
    "enhanced_rules.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        enhanced,
        f,
        indent=4,
        ensure_ascii=False
    )

print(
"Enhanced Rules:",
len(enhanced)
)