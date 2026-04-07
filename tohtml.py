import json
from html import escape

# Load your chat data - no fluff, just works
with open("notool_chats.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def format_message(text):
    if not text or not text.strip():
        return ""
    return escape(text).replace("\n", "<br>")

# Build the HTML preview - clean, dark, scrollable chat UI with Tailwind
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notool Chat Preview</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&amp;display=swap');
        body { font-family: 'Inter', system_ui, sans-serif; }
        .chat-bubble-user { border-radius: 20px 20px 4px 20px; }
        .chat-bubble-ai { border-radius: 20px 20px 20px 4px; }
    </style>
</head>
<body class="bg-slate-950 text-slate-200">
    <div class="max-w-3xl mx-auto py-8 px-4">
        <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-x-3">
                <div class="w-8 h-8 bg-emerald-500 rounded-2xl flex items-center justify-center text-white text-xl font-bold">T</div>
                <div>
                    <h1 class="text-2xl font-semibold">Notool Chats</h1>
                    <p class="text-slate-400 text-sm">Conversation preview</p>
                </div>
            </div>
            <div class="text-xs bg-slate-800 px-3 py-1 rounded-3xl text-slate-400">Generated • Open in browser</div>
        </div>
        
        <div id="chat-container" class="bg-slate-900 rounded-3xl shadow-2xl p-6 h-[620px] overflow-y-auto flex flex-col gap-6">
"""

for entry in data:
    question = entry.get("question", "")
    teacher = entry.get("teacher", "")
    
    if question:
        html_content += f"""
            <div class="flex justify-end">
                <div class="max-w-[75%]">
                    <div class="bg-blue-600 text-white px-5 py-4 chat-bubble-user text-[15px] leading-relaxed">
                        {format_message(question)}
                    </div>
                    <div class="text-xs text-slate-500 mt-1 text-right">You</div>
                </div>
            </div>
        """
    
    if teacher:
        html_content += f"""
            <div class="flex justify-start">
                <div class="max-w-[75%]">
                    <div class="bg-slate-700 text-slate-200 px-5 py-4 chat-bubble-ai text-[15px] leading-relaxed">
                        {format_message(teacher)}
                    </div>
                    <div class="text-xs text-slate-500 mt-1">Teacher</div>
                </div>
            </div>
        """

html_content += """
        </div>
    </div>

    <script>
        const container = document.getElementById('chat-container');
        container.scrollTop = container.scrollHeight;
    </script>
</body>
</html>
"""

with open("chat_preview.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Done. chat_preview.html created in current folder. Open it. Looks sharp, zero dependencies.")