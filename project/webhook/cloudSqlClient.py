from models import Session, User


def find_user(line_id: str):
    with Session() as session:
        return session.query(User).filter_by(line_id=line_id).first()
