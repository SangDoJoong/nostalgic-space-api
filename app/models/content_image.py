from sqlmodel import Field, SQLModel


class ContentImage(SQLModel, table=True):
    __tablename__ = "Contents_Images"

    id: int | None = Field(default=None, primary_key=True)
    content_id: int = Field(..., nullable=False)
    image_id: int = Field(..., nullable=False)
