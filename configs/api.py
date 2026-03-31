from pydantic import BaseModel, field_validator

class ScheduleApi(BaseModel):
    date: str =  None
    lesson: int =  None
    started_at: str =  None
    finished_at: str =  None
    teacher_name: str =  None
    subject_name: str =  None
    room_name: str =  None

class Tokens(BaseModel):
    access_token: str = None
    refresh_token: str = None

