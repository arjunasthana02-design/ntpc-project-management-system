import json

with open(
"categorized_rules.json",
"r",
encoding="utf8"
) as f:

    data=json.load(f)


critical=[]

medium=[]

low=[]


critical_words=[

"shall",
"mandatory",
"must",
"required",
"not allowed"

]

medium_words=[

"recommended",
"should",
"ensure"

]


for category in data:

    for rule in data[category]:

        text=rule.lower()


        if any(
        x in text
        for x in critical_words
        ):

            critical.append(rule)


        elif any(
        x in text
        for x in medium_words
        ):

            medium.append(rule)


        else:

            low.append(rule)



print(
"Critical:",
len(critical)
)

print(
"Medium:",
len(medium)
)

print(
"Low:",
len(low)
)


result={

"critical":critical,

"medium":medium,

"low":low

}


with open(
"severity_rules.json",
"w",
encoding="utf8"
) as f:

    json.dump(
    result,
    f,
    indent=4,
    ensure_ascii=False
    )