from abc import ABC


class Experiment(ABC):
    dataset = None

    def load_dataset(
        self,
        offset: int = 0,
        size_limit: int = 100,
    ):
        raise NotImplementedError

    def build_command(self):
        raise NotImplementedError

    def get_gold_summaries(self):
        raise NotImplementedError

    def get_input_documents(self):
        raise NotImplementedError
