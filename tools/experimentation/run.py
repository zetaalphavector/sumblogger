import asyncio
import os
import time
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Union

import pandas as pd
from dotenv import load_dotenv

from tools.experimentation.pipelines.multi_xscience_onestep import (
    OneStepMultiXScienceExperiment,
)
from tools.experimentation.pipelines.scitldr_our_prompt import (
    OurTwoShotPromptSciTLDRExperiment,
    OurZeroShotPromptSciTLDRExperiment,
)
from tools.experimentation.pipelines.scitldr_vanilla_prompt import (
    VanillaSciTLDRExperiment,
)

load_dotenv("./dev.env")


from zav.message_bus import MessageBus

from src.adapters import text_completion_client  # noqa
from src.bootstrap import bootstrap
from src.controllers.v1.api_types import TextCompletionUsecasesItem
from tools.experimentation.pipelines import Experiment
from tools.experimentation.pipelines.multi_xscience_twostep import (
    TwoStepMultiXScienceExperiment,
)

NAME_2_EXPERIMENT = {
    "multi_xscience_twostep": TwoStepMultiXScienceExperiment,
    "multi_xscience_onestep": OneStepMultiXScienceExperiment,
    "scitldr_vanilla": VanillaSciTLDRExperiment,
    "scitldr_zero_shot": OurZeroShotPromptSciTLDRExperiment,
    "scitldr_two_shot": OurTwoShotPromptSciTLDRExperiment,
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
    experiment: Experiment = NAME_2_EXPERIMENT[experiment_name]()
    data_offset = int(args["offset"]) or 0
    data_size_limit = int(args["size"]) or 1
    message_bus = await startup_and_get_message_bus()

    experiment.load_dataset(offset=data_offset, size_limit=data_size_limit)
    command = experiment.build_command()
    gold_summaries = experiment.get_gold_summaries()
    input_documents = experiment.get_input_documents()

    responses = await message_bus.handle(command)
    response: TextCompletionUsecasesItem = responses.pop(0)

    generated_summaries_list = response["output_params_list"][0]["generated_summaries"]
    generated_summaries = [
        l[0] if isinstance(l, list) else l for l in generated_summaries_list
    ]

    csv_filename = summaries_csv_filename_from(experiment_name)
    summaries_df = summaries_df_from(
        input_documents,
        gold_summaries,
        generated_summaries,
        csv_filename,
    )
    summaries_df.to_csv(csv_filename)


async def startup_and_get_message_bus() -> MessageBus:
    await bootstrap.startup()
    return bootstrap.message_bus


def summaries_df_from(
    input_documents: Union[List[str], List[List[str]]],
    gold_summaries: List[str],
    generated_summaries: List[str],
    csv_filename: str,
) -> pd.DataFrame:

    if os.path.exists(csv_filename):
        print(f"Appending to {csv_filename}")
        summaries_df = pd.read_csv(csv_filename, index_col=0)
    else:
        print(f"Creating new {csv_filename}")
        summaries_df = pd.DataFrame(columns=["summaries", "gold_summaries", "docs"])

    current_summaries_df = pd.DataFrame(
        list(
            zip(
                generated_summaries,
                gold_summaries,
                input_documents,
            )
        ),
        columns=["summaries", "gold_summaries", "docs"],
    )

    summaries_df = pd.concat([summaries_df, current_summaries_df], ignore_index=True)

    return summaries_df


def summaries_csv_filename_from(experiment_name) -> str:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    experiments_dir = f"{current_dir}/results/summaries"
    Path(experiments_dir).mkdir(parents=True, exist_ok=True)

    return f"{experiments_dir}/{experiment_name}.csv"


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
