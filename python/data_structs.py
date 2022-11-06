from dataclasses import dataclass


@dataclass
class Resource:
    name: str
    type: str
    trust_boundry: str
    data_flows: list()

@dataclass
class DataFlow:
    source: Resource
    destination: Resource
    data_sensitivity: str

@dataclass
class Threat:
    id: int
    name: str
    description: str
    stride: list()
    impact: float

@dataclass
class Mitigation:
    id: int
    name: str
    CCMV4_ID: str
    remediation: bool
    description: str
    related_to: list()


