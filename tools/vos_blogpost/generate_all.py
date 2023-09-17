import argparse
import asyncio
import os

from tools.vos_blogpost.generate_html import create_html
from tools.vos_blogpost.generate_md import create_md
from tools.vos_blogpost.generate_vos import create_blogpost

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_file",
    help="input file",
    required=True,
    type=argparse.FileType("r"),
)
parser.add_argument(
    "--output_dir",
    help="output directory",
    required=True,
)


async def main():
    args = parser.parse_args()
    input_file_path = args.input_file.name
    output_dir = args.output_dir
    representative_docs_flag = True

    input_file_name = input_file_path.split(os.sep)[-1].split(".")[0]
    os.makedirs(output_dir, exist_ok=True)

    vos_file_path = os.path.join(output_dir, f"{input_file_name}.json")
    vos_clusters_dir = os.path.join(output_dir, "vos")
    os.makedirs(vos_clusters_dir, exist_ok=True)

    await create_blogpost(
        input_file_path,
        vos_file_path,
        vos_clusters_dir,
        representative_docs_flag,
    )

    md_file_path = os.path.join(output_dir, f"{input_file_name}.md")
    create_md(
        vos_file_path,
        md_file_path,
    )

    html_file_path = os.path.join(output_dir, f"{input_file_name}.html")
    create_html(
        md_file_path,
        html_file_path,
    )


if __name__ == "__main__":
    asyncio.run(main())
