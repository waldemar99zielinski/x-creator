import os

curpath = os.path.abspath(os.curdir)

topic = "AI-Driven Cancer Diagnostic Tool Outperforms Human Analysis"

file_name = topic.replace(" ", "_").lower()

with open(f"{curpath}/saved_posts/{file_name}.txt", mode="w") as file:
            file.write("Teaser:\n")
            file.write("lol" + "\n\n")
            file.write("Post:\n")
