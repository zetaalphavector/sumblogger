import asyncio
import time
from argparse import ArgumentParser
from typing import Dict

from dotenv import load_dotenv

from tools.experimentation.datasets.scitldr import load_scitldr_dataset
from tools.experimentation.datasets.types import FoldName
from tools.experimentation.run_intruction_tuned_llm import (
    summaries_csv_filename_from,
    summaries_df_from,
)

load_dotenv("./dev.env")


from tools.experimentation.finetuned_models.scitldr_models import (
    CattsScitldrFineTunedSummarizationModel,
    HFFineTunedSummarizationModel,
    PegasusFineTunedSummarizationModel,
    T5FineTunedSummarizationModel,
)

NAME_2_MODEL = {
    "scitldr_catts": CattsScitldrFineTunedSummarizationModel,
    "scitldr_pegasus": PegasusFineTunedSummarizationModel,
    "scitldr_t5": T5FineTunedSummarizationModel,
}


def parse_arguments() -> Dict[str, str]:
    parser = ArgumentParser()
    parser.add_argument(
        "--experiment-name",
        type=str,
        required=True,
        help="experiment to run",
    )
    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="Number of samples to evaluate",
    )
    parser.add_argument(
        "--offset",
        type=int,
        required=True,
        help="Offset of the samples to evaluate",
    )

    args = parser.parse_args()
    return args.__dict__


async def main():
    args = parse_arguments()
    experiment_name = args["experiment_name"] or "multi_xscience_twostep"
    model: HFFineTunedSummarizationModel = NAME_2_MODEL[experiment_name]()
    data_offset = int(args["offset"]) or 0
    data_size_limit = int(args["size"]) or 1

    dataset = load_scitldr_dataset(offset=data_offset, size_limit=data_size_limit)
    gold_summaries = dataset.fold_name2data[FoldName.TEST].gold_summaries
    input_documents = dataset.fold_name2data[FoldName.TEST].documents

    print(f"Running model {experiment_name}")
    generated_summaries = await model.execute(input_documents)
    print(f"Finished running model {experiment_name}")

    csv_filename = summaries_csv_filename_from(experiment_name)
    summaries_df = summaries_df_from(
        input_documents,
        gold_summaries,
        generated_summaries,
        csv_filename,
    )
    summaries_df.to_csv(csv_filename)


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
