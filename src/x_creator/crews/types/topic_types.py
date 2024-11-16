from pydantic import BaseModel

class Topic(BaseModel):
    topic: str
    description: str
    url: str

class TopicProposalList(BaseModel):
    topics: list[Topic]

    def parse_to_string(self) -> str:
        return "\n".join([f"{index + 1}. {topic.topic} \n\tdescription: {topic.description} \n\turl: {topic.url}" for index, topic in enumerate(self.topics)])

class SelectedTopic(BaseModel):
    topic: Topic
