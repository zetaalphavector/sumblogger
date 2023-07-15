import json
import os

import requests

INPUT_DIR = "input_vos_networks"
VOS_INPUT_FILE = "ICLR2023.json"
OUTPUT_DIR = "output_vos_networks"
REPRESENTATIVE_DOCS_FLAG = True
# DETAILED_PARAGRAPH_USECASE_VARIANT = "oneshot_detailed_paragraph"
# SUMMARIZED_VOS_FILE = VOS_INPUT_FILE.replace(
#     ".json", f"{DETAILED_PARAGRAPH_USECASE_VARIANT}.json"
# )
variants = [
    "oneshot_detailed_paragraph",
    "detailed_paragraph",
    "detailed_paragraph_with_refinements",
    "oneshot_detailed_paragraph_with_refinements",
]


def summarize(variant):
    with open(os.path.join(INPUT_DIR, VOS_INPUT_FILE)) as f:
        data = json.load(f)

    response = requests.post(
        "http://localhost:8080/v1/vos/summaries",
        json=data,
        params={
            "detailed_paragraph_usecase_variant": variant,
            "focus_on_most_representatives": REPRESENTATIVE_DOCS_FLAG,
        },
    ).json()

    output_file = VOS_INPUT_FILE.replace(".json", f"_{variant}.json")

    with open(os.path.join(OUTPUT_DIR, output_file), "w") as f:
        json.dump(response, f, indent=2)
    return response


for variant in variants:
    summarize(variant)
