from faker import Faker
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class FakeCard:
    card_number: str = None
    exp_month: str = None
    exp_year: str = None
    cvn: str = None

    def generate(self):
        fake = Faker()

        self.card_number = fake.credit_card_number(card_type=None)
        self.exp_month = fake.credit_card_expire(start="now", end="+5y", date_format="%m")
        self.exp_year = fake.credit_card_expire(start="now", end="+5y", date_format="%y")
        self.cvn = fake.credit_card_security_code(card_type=None)

        return asdict(self)

    
if __name__ == "__main__":
    card = FakeCard().generate()

    print(card)
