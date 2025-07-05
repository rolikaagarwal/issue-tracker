from pydantic import BaseModel, ConfigDict, computed_field

class AttachmentRead(BaseModel):
    id: int
    filename: str
    filepath: str

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def url(self) -> str:
        normalized_path = self.filepath.replace("\\", "/")
        return f"/{normalized_path}"
