from pydantic import BaseModel, Field, ConfigDict

class PromptRequest(BaseModel):
    story_prompt: str = Field(..., min_length=1, max_length=4000)
    character_name: str = Field(..., min_length=1, max_length=100)
    setting: str = Field(..., min_length=1, max_length=100)
    tone: str = Field(..., min_length=1, max_length=100)
    art_style: str = Field(..., min_length=1, max_length=100)
    model_config = ConfigDict(json_schema_extra={"example": {
        "story_prompt": "A brave fox exploring an enchanted forest",
        "character_name": "Finn", "setting": "forest", "tone": "dramatic", "art_style": "anime"
    }})
