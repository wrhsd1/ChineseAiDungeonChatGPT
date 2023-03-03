import gradio as gr
import os

from story_rewrite import StoryTeller

def generate_story(story_background):
    chatter = StoryTeller(story_background)
    return chatter.start()

story_background_input = gr.inputs.Textbox(label="请输入故事背景", placeholder="你在树林里冒险，指不定会从哪里蹦出来一些奇怪的东西，你握紧手上的手枪，希望这次冒险能够找到一些值钱的东西，你往树林深处走去。")
output_text = gr.outputs.Textbox(label="故事输出")

gr.Interface(fn=generate_story, inputs=story_background_input, outputs=output_text, title="故事改写器").launch(debug = True)
