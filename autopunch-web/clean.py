from app import models
from app.models import *
from app import check
for i in db.session.query(user).filter().all():
    if check.check(i.username,i.password)==False:
        print i
        delete_user=i
        db.session.delete(delete_user)
        db.session.commit()

