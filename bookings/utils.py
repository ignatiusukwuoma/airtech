import uuid


def generate_e_ticket():
    return uuid.uuid4().hex[:6].upper()


def generate_uuid():
    return uuid.uuid4().hex.upper()
