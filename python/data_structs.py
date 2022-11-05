from dataclasses import dataclass

@dataclass
class threats:
    uuid: int
    name: str
    description: str
    severity: str
    likelihood: float
    impact: float
    risk = likelihood * impact

@dataclass
class mitigation:
    uuid: int
    mitagates: threats.uuid
    name: str
    description: str
    cost: float
    effectiveness: float
    risk_reduction = cost * effectiveness

    