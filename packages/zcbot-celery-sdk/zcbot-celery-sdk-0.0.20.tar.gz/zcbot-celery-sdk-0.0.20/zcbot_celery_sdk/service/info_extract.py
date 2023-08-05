from typing import Dict

from .base import BaseService
from ..model.callback import Callback


class BrandNameModelExtractService(BaseService):

    def info_extract(self, task_params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='info_extract.bnm', task_params=task_params, callback=callback,
                                        **kwargs)
