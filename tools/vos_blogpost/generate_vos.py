import json
import os
from typing import cast

from src.scripts.generate_blogpost import generate_blogpost
from src.types.vos import VosConferenceClusteredDocuments


async def create_blogpost(
    input_file_path,
    output_file_path,
    vos_clusters_dir,
    representative_docs_flag,
):
    with open(input_file_path) as f:
        data = json.load(f)
    data["conference_info"] = {
        "name": "ICLR",
        "website": "iclr.cc",
        "location": "Kawai",
        "start_date": "11 May",
        "end_date": "17 May",
    }

    # response = requests.post(
    #     "http://localhost:8080/v1/vos/blogpost",
    #     json=data,
    #     params={
    #         "detailed_paragraph_usecase_variant": "oneshot_detailed_paragraph",
    #         "focus_on_most_representatives": representative_docs_flag,
    #     },
    # ).json()

    response = await generate_blogpost(
        body=VosConferenceClusteredDocuments.parse_obj(data),
        focus_on_most_representatives=representative_docs_flag,
        detailed_paragraph_usecase_variant="oneshot_detailed_paragraph",
    )
    with open(output_file_path, "w") as f:
        json.dump(response["vos"].json(), f, indent=2)

    for cluster_id, vos in response["cluster2vos"].items():
        vos_path = os.path.join(vos_clusters_dir, f"{cluster_id}.json")
        with open(vos_path, "w") as f:
            json.dump(vos.json(), f, indent=2)
