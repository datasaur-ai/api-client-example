from dataclasses import dataclass


@dataclass
class User:
    id: str
    email: str
    client_id: str
    client_secret: str


@dataclass
class LabelerAssignment:
    client_id: str
    client_secret: str
    email: str
    documents: str
