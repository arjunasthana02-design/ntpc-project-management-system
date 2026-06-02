import fitz
import re
import json

doc=fitz.open("uploads/SectionVI.pdf")

text=""

for page in doc:
    text+=page.get_text()

sentences=re.split(r'[\n.]',text)

rules=[]

keywords=[
"shall",
"must",
"required",
"mandatory",
"IS",
"load",
"clearance",
"foundation",
"layout",
"wind",
"seismic",
"RCDC",
"STAAD",
"soil"
]

for s in sentences:

    if len(s)>20:

        for k in keywords:

            if k.lower() in s.lower():

                rules.append(s.strip())
                break


with open("ntpc_rules.json","w",encoding="utf8") as f:

    json.dump(
        rules,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Rules extracted:",len(rules))