from sqlmodel import Field, SQLModel


class UserImage(SQLModel, table=True):
    __tablename__ = "Users_Images"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(..., nullable=False)
    image_id: int = Field(..., nullable=False)
