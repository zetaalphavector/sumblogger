import json

OUTPUT_DIR = "output_vos_networks_citations"
CONFERENCE = "ICLR"


def create_markdown_from(blogpost_vos_file: str):
    with open(blogpost_vos_file) as f:
        vos = json.loads(json.load(f))
        full_vos_frame = __vos_frame_from(None)
        blog_title = f"# {vos['network']['blog_title']}"
        blog_intro = vos["network"]["blog_intro"]
        blog_conclusion = vos["network"]["blog_conclusion"]
        summarized_clusters = vos["network"]["clusters"]
        blog_body = "\n" + "\n\n".join(
            [
                __body_from(cluster, i + 1)
                for i, cluster in enumerate(summarized_clusters)
            ]
        )

        blog_md = "\n".join(
            [blog_title, blog_intro, full_vos_frame, blog_body, blog_conclusion]
        )
        return blog_md


def __body_from(cluster, cluster_id):
    title = cluster["label"]
    content = cluster["summary"]["tldr_summary"]
    intro = content.split("\n\n", 1)[0]
    body = content.split("\n\n", 1)[1]
    vos_frame = __vos_frame_from(cluster_id)
    return f"## {title}\n{intro}\n{vos_frame}\n\n{body}\n"


def __vos_frame_from(cluster_id):
    if cluster_id is not None:
        return f"""<div> <figure><iframe allow="fullscreen" title="VOSViewer" class="jss1373" style="align:center; width: 100%; height: 300px;" src="https://vos.zeta-alpha.com/?json=https://zav-vos-viewer.s3.eu-central-1.amazonaws.com/data/automated-blog/{OUTPUT_DIR}/vos/{cluster_id}-VOS-{CONFERENCE}.blog.json" data-dashlane-frameid="25634"></iframe> <figcaption style="font-size: 0.8em; text-align: center;">The 10 red nodes were picked as representatives of the cluster</figcaption></figure></div>"""
    else:
        return f"""<div> <figure><iframe allow="fullscreen" title="VOSViewer" class="jss1373" style="align:center; width: 100%; height: 300px;" src="https://vos.zeta-alpha.com/?json=https://zav-vos-viewer.s3.eu-central-1.amazonaws.com/data/automated-blog/{OUTPUT_DIR}/vos/VOS-{CONFERENCE}.blog.json" data-dashlane-frameid="25634"></iframe> <figcaption style="font-size: 0.8em; text-align: center;">VosViewer visualization of the conference</figcaption></figure></div>"""


def create_md(vos_file, output_md_file_path):
    blog_md = create_markdown_from(vos_file)
    with open(output_md_file_path, "w") as f:
        f.write(blog_md)
