from pydantic import BaseModel

class PostChapterOutline(BaseModel):
    title: str
    description: str

class PostOutline(BaseModel):
    chapters_outlines: list[PostChapterOutline]

    def parse_to_string(self) -> str:
        return "\n".join([f"{index + 1}. {chapter.title} \n\tdescription: {chapter.description}" for index, chapter in enumerate(self.chapters_outlines)])

class PostChapter(BaseModel):
    content: str

class Post(BaseModel):
    chapters: list[PostChapter]

    def to_string(self) -> str:
        return "\n\n".join([chapter.content for chapter in self.chapters])

class PostTeaser(BaseModel):
    teaser: str