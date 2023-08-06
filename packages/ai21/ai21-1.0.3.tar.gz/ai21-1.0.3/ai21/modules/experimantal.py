from ai21 import Completion
from ai21.modules.resources.nlp_task import NLPTask
from ai21.utils import validate_mandatory_field


class Experimental(NLPTask):

    @classmethod
    def _execute(cls, module: str, **params):
        url = f'{cls.get_base_url(**params)}/experimental/{module}'
        return super().execute(task_url=url, **params)

    @classmethod
    def rewrite(cls, **params):
        validate_mandatory_field(key='text', call_name="rewrite_experimental", params=params, validate_type=True, expected_type=str)
        url = cls.get_base_url(**params)
        url = f'{url}/experimental/rewrite'
        return super().execute(task_url=url, **params)

    @classmethod
    def summarize(cls, **params):
        validate_mandatory_field(key='text', call_name="summarize_experimental", params=params, validate_type=True, expected_type=str)
        url = cls.get_base_url(**params)
        url = f'{url}/experimental/summarize'
        return super().execute(task_url=url, **params)

    @classmethod
    def j1_grande_instruct(cls, **params):
        params["model"] = "j1-grande-instruct"
        return Completion.execute(experimental_mode=True, **params)
