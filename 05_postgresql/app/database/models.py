from typing import TYPE_CHECKING
from pydantic import EmailStr
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from datetime import datetime
from sqlalchemy.dialects import postgresql
from sqlalchemy import ARRAY, INTEGER
from uuid import uuid4, UUID

if TYPE_CHECKING:
    from api.schemas.shipment import Shipment

# model used to define the data in the fields
class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


# class Shipment(SQLModel, table=True):
    
    
#     __tablename__ = "shipment"
    
#     id: int = Field(default=None, primary_key=True)
#     content: str
#     weight: float = Field(le=25)
#     destination: int
#     status: ShipmentStatus
#     estimated_delivery: datetime
    


class User(SQLModel):

    name: str

    email: EmailStr
    password_hash: str


# SQLModel will handle creating table it will covert a class name it lowercase name and create the table for us

class Seller(User, table=True):

    __tablename__ = "seller"
    
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

    shipments: list["Shipment"] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class DeliveryPartner(User, table=True):


    __tablename__ = "delivery_partner"

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

    serviceable_zip_codes: list[int] = Field(
        sa_column=Column(ARRAY(INTEGER)),
    )

    max_handling_capacity: int 


    shipments: list["Shipment"] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def active_shipments(self):

        return [
            shipment 
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
        ]

    # The amount of shipments the deliver partner can handle currently
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments())