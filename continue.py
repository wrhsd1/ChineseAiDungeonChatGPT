from story_rewrite import StoryTeller


with open('chat_log.txt', 'r') as f:
                    lines = f.readlines()
                    last_line = lines[-1]
                    if last_line:
                        story_background = last_line


if __name__ == "__main__":
    chatter = StoryTeller(story_background)
    chatter.start_cli()
