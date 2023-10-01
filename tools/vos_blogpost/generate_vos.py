import json
import os

from src.scripts.generate_blogpost import generate_blogpost
from src.types.vos import VosConferenceClusteredDocuments

CONFERENCE_INFO = {
    "name": "ICLR",
    "website": "https://iclr.cc/Conferences/2023",
    "location": "Kawai",
    "start_date": "11 May 2023",
    "end_date": "17 May 2023",
}


async def create_blogpost(
    input_file_path,
    output_file_path,
    vos_clusters_dir,
    representative_docs_flag,
):
    with open(input_file_path) as f:
        data = json.load(f)

    if "clusters" not in data["network"]:
        cluster_ids = {node["cluster"] for node in data["network"]["items"]}
        data["network"]["clusters"] = [
            {"cluster": idx, "label": ""} for idx in cluster_ids
        ]
    data["conference_info"] = CONFERENCE_INFO

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
