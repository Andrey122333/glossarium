from pydantic import BaseModel, Field


class TermAddSchema(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    definition: str = Field(min_length=1)


class TermSchema(TermAddSchema):
    id: int

    class Config:
        orm_mode = True
