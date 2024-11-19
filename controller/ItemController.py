from typing_extensions import Annotated
from model.Item import Item
from database import SessionDep
from fastapi import APIRouter, Depends
from security import oauth2_scheme

router = APIRouter(prefix="/item", tags=["items"], responses={404: {"description": "Not found"}})

@router.get("/{item_id}")
async def readItem(item_id: int, session: SessionDep):
    return session.get(Item, ident=item_id)

@router.post("/")
async def storeItem(token: Annotated[str, Depends(oauth2_scheme)],item: Item, session: SessionDep) -> Item:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item