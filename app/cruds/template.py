from sqlalchemy.orm import Session
from app.schemas.template import TemplateCreate
from app.models.models import Slot,Template
def template_post(request:TemplateCreate,db:Session):
    slots=[]
    for slot_id in request.slots:
        slot=db.get(Slot,slot_id)
        if not slot:
            continue
        slots.append(slot)
    template=Template(name=request.name,slots=slots )
    db.add(template)
    db.commit()
    return template

