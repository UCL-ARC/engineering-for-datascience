from transformer import ORD_to_SQLAlchemy, file_to_model
from chemistry2 import session, add_items, create_tables, sqlite

model = file_to_model("ds_fix_1.pb.gz")

with sqlite() as db:
    create_tables(db)
    s = session(db)
    reactions = ORD_to_SQLAlchemy(model)
    add_items(reactions, s)
    s.commit()
