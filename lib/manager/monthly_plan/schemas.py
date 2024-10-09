import uuid
from datetime import time as d_time
from lib.conf.config import Base

class Response(Base):
    code: int
    description: str


class BudgetResponse(Base):
    status: str
    msg: Response

class Budget(Base):
    uuid: uuid.UUID
    ts_from: d_time
    ts_to: d_time
    plan_money: float
    budget_type: str
