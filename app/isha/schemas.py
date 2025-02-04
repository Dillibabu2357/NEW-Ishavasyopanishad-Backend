from pydantic import BaseModel

from app.utils import Language, Philosophy
from typing import Optional


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


class MeaningCreate(MeaningBase):
    pass


class MeaningOut(MeaningBase):
    id: int


class MeaningUpdate(MeaningBase):
    pass


class TransliterationBase(BaseModel):
    language: Language
    text: str


class TransliterationCreate(TransliterationBase):
    pass


class TransliterationOut(TransliterationBase):
    id: int


class TransliterationUpdate(TransliterationBase):
    pass


class InterpretationBase(BaseModel):
    language: Language
    text: str
    philosophy: Philosophy


class InterpretationCreate(InterpretationBase):
    pass


class InterpretationOut(InterpretationBase):
    id: int


class InterpretationUpdate(InterpretationBase):
    pass


class Audio(BaseModel):
    file_path: str


class Result(BaseModel):
    text: str
    sutra_no: int
    mode: str | None
    lang: str | None



# Base model for common fields
class BhashyamBase(BaseModel):
    language: Language
    text: str
    philosophy: Philosophy

class BhashyamCreate(BhashyamBase):
    sutra_id: int = None  # Optional since the sutra_no in the path is used.

class BhashyamUpdate(BaseModel):
    text: str = None
    philosophy: Philosophy = None

class BhashyamOut(BhashyamBase):
    sutra_id: int

    class Config:
        orm_mode = True