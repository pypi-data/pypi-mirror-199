from datetime import datetime
from typing import Any, ClassVar, List, Optional

try:
    import constants
except ImportError:
    from . import constants

from pydantic import BaseModel


class AttendeeModel(BaseModel):
    first_names: str
    last_name: str
    name_badge: str
    cell: str
    email: str
    dietary: Optional[str]
    disability: Optional[str]
    mjf_lunch: bool
    pdg_dinner: bool
    beach_cleanup: bool
    lion: bool
    club: str = None
    lpe_breakfast: bool = None
    partner_program: bool = None
    auto_name_badge: bool = False
    full_name: Optional[str]
    attendee_num: Optional[int]

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.full_name = f"{self.first_names} {self.last_name}"
        if not self.name_badge:
            self.name_badge = self.full_name
            self.auto_name_badge = True


class RegistrationItems(BaseModel):
    reg: int = 0
    pins: int = 0


class Registration(BaseModel):
    reg_num: Optional[int]
    attendees: List[AttendeeModel]
    items: RegistrationItems
    timestamp: datetime
    cost: float = 0
    emails: Optional[list]
    names: Optional[str]
    attendee_nums: Optional[list]
    reg_num_string: Optional[str]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.cost:
            for field in ("reg", "pins"):
                self.cost += getattr(constants, f"COST_{field.upper()}", 0) * getattr(
                    self.items, field, 0
                )
        self.emails = list(set([attendee.email for attendee in self.attendees]))
        if not self.emails:
            self.emails = None
        self.names = " and ".join([attendee.full_name for attendee in self.attendees])
        self.attendee_nums = [attendee.attendee_num for attendee in self.attendees]
        if self.reg_num:
            self.reg_num_string = " & ".join(
                [
                    f"{self.reg_num:03}/{attendee.attendee_num}"
                    for attendee in self.attendees
                ]
            )


class Payment(BaseModel):
    reg_num: int
    amount: float
    timestamp: datetime
