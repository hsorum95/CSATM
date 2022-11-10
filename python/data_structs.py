from dataclasses import dataclass
from uuid import UUID, uuid4
import json

@dataclass()
class Resource:
    name: str
    type: str
    trust_boundry: str
    data_flows: list()
    public: bool
    data_processing: bool
    data_store: bool
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@dataclass
class DataFlow:
    source: Resource
    destination: Resource
    data_sensitivity: str
    encrypted: bool = True #The year is 2022. We treat all traffic as encrypted unless otherwise specified
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
@dataclass
class Threat:
    id: int
    name: str
    description: str
    stride: list()
    impact: float
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@dataclass
class Mitigation:
    id: int
    name: str
    CCMV4_ID: str
    remediation: bool
    description: str
    related_to: list()
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@dataclass
class Threat_Instance:
    threat: Threat
    mitigation: Mitigation
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)