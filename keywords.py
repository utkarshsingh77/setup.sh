import json
import os
import re
from collections import defaultdict

OUTPUT_DIRECTORY = "output"
KEYWORDS = [
    "Conversions API",
    "app events",
    "offline events",
    "deduplication",
    "custom data",
    "EMQ score",
    "Implementation",
    "Parameters",
    "Setup guide",
    "Event optimization",
    "Improvement strategies",
    "Offline events tracking",
    "Omnichannel marketing",
    "Measuring offline conversions",
    "Event validation",
    "Facebook Pixel",
    "Client engagement",
    "Lower funnel strategies",
    "Conversion lift tests",
    "External_id hashing",
    "PII handling",
    "Onboarding process",
    "Business messaging integration",
    "IP address requirement",
    "Conversion value adjustments",
    "PII best practices",
    "Pitching CAPI",
    "Event deduplication",
    "LDU compliance",
    "Conversions API integration",
]


def find_content_for_keywords():
    content_by_keyword = defaultdict(set)

    for filename in os.listdir(OUTPUT_DIRECTORY):
        if filename.endswith(".txt"):
            with open(os.path.join(OUTPUT_DIRECTORY, filename), "r") as file:
                content = file.read()
                for keyword in KEYWORDS:
                    if re.search(r"\b{}\b".format(keyword), content, re.IGNORECASE):
                        content_by_keyword[keyword].add(content)

    deduplicated_content_by_keyword = {
        keyword: list(contents) for keyword, contents in content_by_keyword.items()
    }

    with open(os.path.join(OUTPUT_DIRECTORY, "keywords.json"), "w") as file:
        json.dump(deduplicated_content_by_keyword, file, indent=4)


if __name__ == "__main__":
    find_content_for_keywords()
    print("Finished creating keywords.json")
