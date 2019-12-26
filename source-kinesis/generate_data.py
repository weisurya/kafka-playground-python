from faker import Faker
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class FakeLog:
    domain: str = None
    referer: str = None
    ip_address: str = None
    email: str = None
    user_agent: str = None
    description: str = None
    created: str = None

    def generate(self):
        fake = Faker()

        self.domain = fake.url()
        self.referer = fake.uri()
        self.ip_address = fake.ipv4()
        self.email = fake.free_email()
        self.user_agent = fake.user_agent()
        self.description = fake.text(max_nb_chars=200, ext_word_list=None)
        self.created = datetime.now().isoformat()

        return asdict(self)

    
if __name__ == "__main__":
    user = FakeLog().generate()

    print(user)
