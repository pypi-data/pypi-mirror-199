from typing import Dict

from .base import BaseService
from ..model.callback import Callback


class StaplesCatalogService(BaseService):

    def predict_catalog1(self, task_params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.staples1', task_params=task_params, callback=callback,
                                        **kwargs)

    def predict_catalog4(self, task_params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.staples4', task_params=task_params, callback=callback,
                                        **kwargs)

    def predict_catalog6(self, task_params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.staples6', task_params=task_params, callback=callback,
                                        **kwargs)


class JslinkCatalogService(BaseService):

    def predict_catalog1(self, task_params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.jslink1', task_params=task_params, callback=callback,
                                        **kwargs)

    def predict_catalog4(self, task_params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='catalog.jslink4', task_params=task_params, callback=callback,
                                        **kwargs)
