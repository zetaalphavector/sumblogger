from src.bootstrap import pass_through_text_completion_service


class PassThroughTextCompletionServiceDependency:
    def __init__(self, service) -> None:
        self.service = service

    def __call__(self):
        return self.service


pass_through_text_completion_service_dependency = (
    PassThroughTextCompletionServiceDependency(pass_through_text_completion_service)
)


def get_pass_through_text_completion_service():
    sentinel_bus = object()
    return sentinel_bus
