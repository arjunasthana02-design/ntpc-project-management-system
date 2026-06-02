import json

with open(
"severity_rules.json",
"r",
encoding="utf8"
) as f:

    data=json.load(f)


critical=data["critical"]

clean=[]

seen=set()


for rule in critical:

    x=rule.strip()

    x=x.lower()


    if len(x)>40:

        if x not in seen:

            seen.add(x)

            clean.append(rule)


print(
"Old:",
len(critical)
)

print(
"Clean:",
len(clean)
)


with open(
"clean_rules.json",
"w",
encoding="utf8"
) as f:

    json.dump(
    clean,
    f,
    indent=4,
    ensure_ascii=False
    )