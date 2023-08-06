import gradio as gr
from paddlenlp import Taskflow
from sparrow import rel_to_abs

topN = 1
docprompt = Taskflow("document_intelligence", batch_size=3, lang="ch", topn=topN)


def image_mod(image_dir: str, prompt_text: str, topn: int):
    # image_dir = rel_to_abs("uploaded_image.jpg")
    # image.save(image_dir)
    global topN, docprompt
    if topn != topN:
        topN = topn
        print(topn)
        if topN <= 0:
            topN = 1
        docprompt = Taskflow("document_intelligence", batch_size=3, lang="ch", topn=int(topN))
        # docprompt.set_argument({'topn': topn})
    prompt_text = prompt_text.strip("")
    if prompt_text[0] == '[':
        prompt = eval(prompt_text)
    print(prompt)
    out_put = docprompt([{"doc": image_dir,
                          "prompt": prompt
                          }])
    out_markdown = ""
    for item in out_put:
        out_markdown += f"""#### {item['prompt']} \n\n"""
        for i in item['result']:
            out_markdown += f"""**{i['value']}**, *{i['prob']}*  \n"""
    return out_markdown


demo = gr.Interface(image_mod,
                    [
                        gr.Image(type="filepath"),
                        gr.inputs.Textbox(
                            lines=3,
                            default="""[
'五百丁本次想要担任的是什么职位?', 
'五百丁是在哪里上的大学?', 
'大学学的是什么专业?',
]"""
                        ),
                        gr.inputs.Number(1, "topN", )

                    ],
                    # "json",  # "list"?
                    # ["highlight", "json", "html"],
                    gr.Markdown(),
                    flagging_options=["blurry", "incorrect", "other"],
                    examples=[[rel_to_abs("test.png"),
                               """['五百丁本次想要担任的是什么职位?', \n'五百丁的兴趣爱好是?', \n'五百丁的年龄是?',]"""]]
                    )

if __name__ == "__main__":
    demo.launch(
        server_name='0.0.0.0',
        server_port=12345,
        # share=True,
    )
