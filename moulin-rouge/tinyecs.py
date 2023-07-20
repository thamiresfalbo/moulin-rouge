import uuid
import json
from dataclasses import dataclass

@dataclass
class Entity():
    unique_id = str(uuid.uuid4)

class Component():
    pass

class System():
    pass
