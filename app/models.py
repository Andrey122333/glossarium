from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class TermModel(Base):
    __tablename__ = "terms"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    definition: Mapped[str]
