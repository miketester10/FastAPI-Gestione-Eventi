from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import get_async_session
from src.events.models import Event
from src.reservations.models import Reservation
from src.reservations.schemas import (
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate,
)
from src.security import JWTBearer

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
)


@router.get("/", response_model=Optional[List[ReservationResponse]])
async def get_reservations(
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(JWTBearer()),
):
    query = select(Reservation).where(Reservation.user_id == user_id)
    query_result = await session.scalars(query)
    result = query_result.all()
    return result


@router.post("/", response_model=ReservationResponse, status_code=201)
async def create_reservation(
    payload: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),  # la sessione viene gestita da FastAPI
    user_id: int = Depends(JWTBearer()),                 # otteniamo l'id dell'utente dal JWT
):
    # ---------------------------------------------
    # 1️⃣ Inizio una transazione esplicita
    # Questo blocco garantisce che tutte le operazioni
    # qui dentro siano atomiche: commit se tutto va bene,
    # rollback automatico se c'è un errore
    # ---------------------------------------------
    async with session.begin():  
        
        # ---------------------------------------------
        # 2️⃣ Seleziono l'evento e applico un lock di tipo FOR UPDATE
        # Questo impedisce ad altre transazioni di modificare
        # lo stesso record fino a quando non finiamo questa transazione
        # ---------------------------------------------
        query = select(Event).where(Event.id == payload.event_id).with_for_update()
        event = (await session.scalars(query)).first()  # prendo il primo risultato

        # ---------------------------------------------
        # 3️⃣ Controllo se l'evento esiste
        # Se non esiste, lanciamo un'eccezione HTTP 404
        # ---------------------------------------------
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # ---------------------------------------------
        # 4️⃣ Calcolo il numero di posti già prenotati
        # Sommo tutti i num_guests delle prenotazioni esistenti
        # ---------------------------------------------
        query = select(Reservation.num_guests).where(
            Reservation.event_id == payload.event_id
        )
        reservations = await session.scalars(query)
        current_reservations = sum(reservations.all())

        # ---------------------------------------------
        # 5️⃣ Controllo se ci sono abbastanza posti disponibili
        # Se la somma dei posti già prenotati + quelli richiesti
        # supera la capacità dell'evento, lanciamo un errore
        # ---------------------------------------------
        if current_reservations + payload.num_guests > event.capacity:
            raise HTTPException(status_code=400, detail="Not enough seats available")

        # ---------------------------------------------
        # 6️⃣ Creo la nuova prenotazione
        # Non serve fare commit qui: la transazione esplicita
        # lo farà automaticamente alla fine del blocco
        # ---------------------------------------------
        new_reservation = Reservation(
            num_guests=payload.num_guests,
            user_id=user_id,
            event_id=payload.event_id
        )
        session.add(new_reservation)  # aggiungiamo l'oggetto alla sessione

    # ---------------------------------------------
    # 7️⃣ Fine del blocco `async with session.begin()`
    # - se tutto va bene → commit automatico
    # - se c'è un errore → rollback automatico
    # La sessione verrà chiusa automaticamente da Depends(get_async_session)
    # ---------------------------------------------

    return new_reservation


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(JWTBearer()),
):
    query = select(Reservation).where(
        Reservation.id == reservation_id, Reservation.user_id == user_id
    )
    query_result = await session.scalars(query)
    result = query_result.first()

    if result is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return result


@router.patch("/{reservation_id}", response_model=ReservationResponse)
async def update_reservation(
    reservation_id: int,
    payload: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(JWTBearer()),
):
    query = select(Reservation).where(
        Reservation.id == reservation_id, Reservation.user_id == user_id
    )
    query_result = await session.scalars(query)
    result = query_result.first()

    if result is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    for field, value in payload.model_dump().items():
        if value is not None:
            setattr(result, field, value)

    await session.commit()
    return result


@router.delete("/{reservation_id}", status_code=204)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(JWTBearer()),
):
    query = select(Reservation).where(
        Reservation.id == reservation_id, Reservation.user_id == user_id
    )
    query_result = await session.scalars(query)
    result = query_result.first()

    if not result:
        return HTTPException(status_code=404, detail="Reservation not found")

    await session.delete(result)
    await session.commit()
    return None
