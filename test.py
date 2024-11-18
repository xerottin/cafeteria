from sqlalchemy.orm import Session

from database.db_user import get_user_archive, archive_order

with Session() as db:
    archive_order(order_id=1, db=db)

user_archive = get_user_archive(user_id=1)
print(user_archive)