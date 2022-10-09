from dataclasses import dataclass, field



@dataclass
class User:
    name: str = field(default='')
    group: str = field(default='')
    units: str = field(default='')
