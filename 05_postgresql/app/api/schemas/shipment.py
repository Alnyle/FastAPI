from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Relationship, SQLModel, Field
from database.models import DeliveryPartner, ShipmentStatus
from sqlalchemy import Column, DateTime
from database.models import Seller
from uuid import uuid4, UUID
from sqlalchemy.dialects import postgresql
# use for data validation and parsing and api Documentation and also used as database schema and api schema
class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25)
    destination: int



class Shipment(BaseShipment, table=True):
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    status: ShipmentStatus
    estimated_delivery: datetime = Field(
    sa_column=Column(DateTime(timezone=True))
    )

    # When I have a Shipment object, I also want a convenient way to access its Seller object.
    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    delivery_partner_id: UUID = Field(
        foreign_key="delivery_partner.id",
    )

    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class ShipmentRead(BaseShipment):

    id: UUID
    seller: Seller
    status: ShipmentStatus
    estimated_delivery: datetime

class ShipmentCreate(BaseShipment):
    pass
    

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
