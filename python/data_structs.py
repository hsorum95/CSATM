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
    severity: str
    likelihood: float
    impact: float
    # risk = likelihood * impact

@dataclass
class mitigation:
    id: int
    # mitagates: threats.id
    name: str
    description: str
    cost: float
    effectiveness: float
    # risk_reduction = cost * effectiveness

