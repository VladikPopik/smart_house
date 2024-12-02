import uuid
from datetime import time as d_time

from fastapi import APIRouter

from lib.db.mysql.monthly_plan import crud as p_crud

from .schemas import Budget, BudgetResponse, Response

plan_router = APIRouter()


# TODO @VladikPopik: CREATE PROPER TIMESTAMP FORMAT
@plan_router.post("/budget")
async def create_budget(
    ts_from: d_time, ts_to: d_time, plan_money: float, budget_type: str
) -> BudgetResponse:
    await p_crud.create_budget(
        ts_from,
        ts_to,
        plan_money,
        budget_type,
    )

    return BudgetResponse(
        status="OK",
        msg=Response(
            code=200,
            description="Everything is ok. Budget Created successfully",
        ),
    )


@plan_router.get("/budget")
async def read_budget(uuid: uuid.UUID) -> Budget:
    budget = await p_crud.read_budget(uuid=uuid)
    return Budget(budget)
