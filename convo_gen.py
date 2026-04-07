import json
from llama_cpp import Llama
import os
import re
from datetime import datetime
from random import randint

def format_date_nice(dt):
    base = dt.strftime("%A, %B %d, %Y")
    day = dt.day
    suffix = "th" if 11 <= day <= 13 else {1:"st", 2:"nd", 3:"rd"}.get(day % 10, "th")
    return base.replace(f"{day},", f"{day}{suffix},")

# INSTRUCTIONS
teacher_inst = open("teacher-instructions.txt", mode="r", encoding="utf-8").read()

OUTPUT_NOTOOLS = "notool_chats.json"
NOTOOL_INSTRUCT = ""
todaydate = ""
def set_instructions_and_date():
    while True:
        try:
            todaydate = format_date_nice(datetime(randint(2023, 2030), randint(1, 12), randint(1, 31)))
            break
        except:
            continue
    teacher_inst.replace("{CURRENT_DATE}", todaydate)
    NOTOOL_INSTRUCT = f"""Today is {todaydate}.
No tools available."""

# ROUTER SETUP
router = Llama(
    model_path="prithivMLmods_Qwen3-VL-8B-Instruct-abliterated-v2-GGUF_Qwen3-VL-8B-Instruct-abliterated-v2.Q5_K_M.gguf",
    chat_format=None,
    n_ctx=8192,
    verbose=False,
    n_gpu_layers=-1,
    n_batch=4096,
    n_threads=6,
    n_threads_batch=6,
    flash_attn=True,
)

def ask_teacher(message:str) -> str:
    router.reset()
    stream = router.create_chat_completion(
        messages = [
            {
                'role': 'system',
                'content': teacher_inst.strip()
            },
            {
                'role': 'user',
                'content': message.strip()
            }
        ],
        temperature=0.6,
        stream=True,
        repeat_penalty=1.2,
        frequency_penalty=0.3,
        present_penalty=0.2,
        penalty_last_n=256
    )

    full_text = ""
    num_chunks = 0
    for chunk in stream:
        delta = chunk["choices"][0]["delta"].get("content", "")
        if delta:
            full_text+=delta
            num_chunks += 1
            print(f"thinking... ({num_chunks} tokens)", end="\r")
            # print(delta, end="", flush=True)
    print("\n[ DONE ]")
    
    return full_text.strip()

os.system("cls")
with open("human_english.json", mode="r", encoding="utf-8") as inf:
    js = json.load(inf)

answers = []
if os.path.exists(OUTPUT_NOTOOLS):
    with open(OUTPUT_NOTOOLS, mode="r", encoding="utf-8") as loadf:
        answers = json.load(loadf)

total = len(js)
js = js[len(answers):]
for i, question in enumerate(js, len(answers)):
    preview = question.split('\n')[0][:50]
    progress = (i + 1) / total * 100
    print(f"## {i}. {preview} [total {total}, {progress:.2f}%]")
    set_instructions_and_date()

    try:
        full_resp = ask_teacher(question)
    except ValueError:
        print("TOO LONG.")
        continue

    answers.append({
        'system': NOTOOL_INSTRUCT,
        'teacher': full_resp,
        'question': question
    })

    with open(OUTPUT_NOTOOLS, mode="w", encoding="utf-8") as outf:
        json.dump(answers, outf)
        outf.flush()
    
    print()