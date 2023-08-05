from typing import Dict, List

from .base import BaseService
from ..model.callback import Callback


class OssService(BaseService):

    # def batch_download(self, task_params_list: List[Dict] = None, callback: Callback = None, **kwargs):
    #     return self.celery_client.apply_group(task_name='oss.download_file', task_params_list=task_params_list, callback=callback, **kwargs)

    def zip(self, task_params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='oss.zip', task_params=task_params, callback=callback, **kwargs)

    # def download_file(self, task_params: Dict = None, callback: Callback = None, **kwargs):
    #     return self.celery_client.apply(task_name='oss.download_file', task_params=task_params, callback=callback, **kwargs)

    # def zip_and_upload(self, task_params: Dict = None, callback: Callback = None, **kwargs):
    #     return self.celery_client.apply(task_name='oss.zip_and_upload', task_params=task_params, callback=callback, **kwargs)
