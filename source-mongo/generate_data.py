from faker import Faker
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class FakeUser:
    first_name: str = None
    last_name: str = None
    last_location: list = None
    metadata: dict = None
    created: str = None
    updated: str = None

    def generate(self):
        fake = Faker()

        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.last_location = fake.local_latlng(country_code="US", coords_only=False)
        self.metadata = fake.pydict(10, True, 'str')
        self.created = datetime.now().isoformat()
        self.updated = datetime.now().isoformat()

        return asdict(self)

    
if __name__ == "__main__":
    user = FakeUser().generate()

    print(user)
