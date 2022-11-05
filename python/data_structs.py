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
class threats:
    id: int
    name: str
    description: str
    stride: list()
    likelihood: float
    impact: float

@dataclass
class mitigation:
    id: int
    name: str
    description: str

