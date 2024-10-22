from pydantic import BaseModel

from app.isha.routers.utils import Language, Philosophy


class SutraBase(BaseModel):
    number: int
    text: str


class SutraCreate(SutraBase):
    pass


class SutraOut(SutraBase):
    id: int


class SutraListOut(BaseModel):
    id: int
    number: int


class SutraUpdate(SutraBase):
    pass


class MeaningBase(BaseModel):
    language: Language
    text: str
    sutra_id: int


class MeaningCreate(MeaningBase):
    pass


class MeaningOut(MeaningBase):
    id: int


class MeaningUpdate(MeaningBase):
    pass


class TransliterationBase(BaseModel):
    language: Language
    text: str
    sutra_id: int


class TransliterationCreate(TransliterationBase):
    pass


class TransliterationOut(TransliterationBase):
    id: int


class TransliterationUpdate(TransliterationBase):
    pass


class InterpretationBase(BaseModel):
    language: Language
    text: str
    sutra_id: int
    philosophy_type: Philosophy


class InterpretationCreate(InterpretationBase):
    pass


class InterpretationOut(InterpretationBase):
    id: int


class InterpretationUpdate(InterpretationBase):
    pass
