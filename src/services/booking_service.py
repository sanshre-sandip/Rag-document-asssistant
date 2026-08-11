from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Booking
from src.services.booking import BookingDetails


async def create_booking(
    db: AsyncSession,
    details: BookingDetails,
) -> Booking:

    if not details.name:
        raise ValueError("Booking name is required.")

    if not details.email:
        raise ValueError("Booking email is required.")

    if not details.booking_date:
        raise ValueError("Booking date is required.")

    if not details.booking_time:
        raise ValueError("Booking time is required.")

    booking = Booking(
        name=details.name,
        email=str(details.email),
        booking_date=details.booking_date,
        booking_time=details.booking_time,
    )

    db.add(booking)

    await db.commit()
    await db.refresh(booking)

    return booking