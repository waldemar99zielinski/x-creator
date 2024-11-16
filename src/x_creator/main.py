#!/usr/bin/env python
import os

from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from crews.topic_research.topic_research_crew import TopicResearchCrew
from crews.trends_validator.trends_validator_crew import TrendsValidatorCrew
from crews.post_outliner.post_outliner_crew import PostOutlinerCrew
from crews.post_writer.post_writer_crew import PostWriterCrew
from crews.post_teaser_writer.post_teaser_writer_crew import PostTeaserWriterCrew

from crews.types.topic_types import Topic, TopicProposalList
from crews.types.post_types import Post, PostChapter, PostOutline

from mocks.topics_proposal_mock import topic_proposal_mocks

class XCreatorState(BaseModel):
    topics_proposals: TopicProposalList = None
    selected_topic: Topic = None
    post_outline: PostOutline = None
    chapters: list[PostChapter] = None
    post: Post = None
    teaser: str = None


class XCreator(Flow[XCreatorState]):

    @start()
    def start_topics_research(self):
        print("Starting research")
        result = (
            TopicResearchCrew()
                .crew()
                .kickoff()
        )

        # result = {"topics": topic_proposal_mocks}

        self.state.topics_proposals = TopicProposalList(topics=result["topics"])

        print("Topics proposals", self.state.topics_proposals.parse_to_string())

    @listen(start_topics_research)
    def select_topic(self):
        print("Validating topics trends")
        
        result = (
            TrendsValidatorCrew()
                .crew()
                .kickoff(inputs={"topics": self.state.topics_proposals.parse_to_string()})
        )

        self.state.selected_topic = result["topic"]

        print("Selected topic", self.state.selected_topic)

    @listen(select_topic)
    def outline_post_chapters(self):
        print("Outlining post chapters")
        print("Selected topic", self.state.selected_topic)

        result = (
            PostOutlinerCrew()
                .crew()
                .kickoff(inputs={
                    "topic": self.state.selected_topic.topic,
                    "description": self.state.selected_topic.description,
                    "url": self.state.selected_topic.url
                })
        )

        self.state.post_outline = PostOutline(chapters_outlines=result["chapters_outlines"])

        print("Post outline", self.state.post_outline)

    @listen(outline_post_chapters)
    def write_post_chapters(self):
        print("Writing post chapters")
        print("Post outline", self.state.post_outline)

        chapters: list[PostChapter] = []

        print("post outlint: ", self.state.post_outline.parse_to_string())

    
        for index, chapter in enumerate(self.state.post_outline.chapters_outlines):
            print(f"Chapter {index + 1}: {chapter.title}")
            print(f"Description: {chapter.description}")

            result = (
                PostWriterCrew()
                    .crew()
                    .kickoff(inputs={
                            "topic": self.state.selected_topic.topic,
                            "chapter_title": chapter.title,
                            "chapter_description": chapter.description,
                            "post_outline": self.state.post_outline.parse_to_string(),
                            "previous_chapter_content": chapters[index - 1].content if index > 0 else "none",
                    })
            )

            print("Result", result)
            chapters.append(PostChapter(content=result["content"]))
        
        self.state.post = Post(chapters=chapters)

    @listen(write_post_chapters)
    def write_post_teaser(self):
        print("Writing post teaser")
        
        result = (
            PostTeaserWriterCrew()
                .crew()
                .kickoff(inputs={
                    "post_content": self.state.post.to_string()
                })
        )

        self.state.teaser = result["teaser"]

    @listen(write_post_teaser)
    def save_post(self):
        curpath = os.path.abspath(os.curdir)
        file_name = self.state.selected_topic.topic.replace(" ", "_").lower()

        with open(f"{curpath}/saved_posts/{file_name}.txt", mode="w") as file:
            file.write("Teaser:\n")
            file.write(self.state.teaser + "\n\n")
            file.write("Post:\n")
            for index, chapter in enumerate(self.state.post.chapters):
                file.write(f"Chapter {index + 1}:\n")
                file.write(chapter.content + "\n\n")

def kickoff():
    poem_flow = XCreator()
    poem_flow.kickoff()


def plot():
    poem_flow = XCreator()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
