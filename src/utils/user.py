from dataclasses import dataclass, field
from . import wks


@dataclass
class User:
    name: str = field(default="")
    group: str = field(default="")
    units: str = field(default="")
    vocation: str = field(default="")
    extra: str = field(default="")
    url: str = field(default="")

    async def save(self):
        length = int(len(wks.get_all_records())) + 2
        wks.update_value(f'A{length}', self.name)
        wks.update_value(f'B{length}', self.group)
        wks.update_value(f'C{length}', self.units)
        wks.update_value(f'D{length}', self.vocation)
        wks.update_value(f'E{length}', self.extra)
        wks.update_value(f'F{length}', self.url)
