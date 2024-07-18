from ..crud.base import CRUDBase
from ..models import Process
from ..schemas import ProcessCreate, ProcessUpdate


class CRUDProcess(CRUDBase[Process, ProcessCreate, ProcessUpdate]):
    def __init__(self, model):
        super().__init__(model)


process = CRUDProcess(Process)
