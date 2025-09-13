import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import time
import uuid
import random

messages = []
widgets = {}

def now_str():
    return datetime.now().strftime("%H:%M:%S")

def generate_bot_response(text):
    t = text.lower()
    if any(w in t for w in ("hi", "hello", "hey")):
        return random.choice(["Hey! 👋 How can I help you today?", "Hello — what's up?", "Hi there! Need something?"])
    if "how are you" in t:
        return "I'm code — feeling ready to help you 😊"
    if "help" in t or "how" in t:
        return "Sure — tell me what you need. I can show features, demo commands, or chat casually."
    if "time" in t:
        return f"The current time is {now_str()}."
    if "joke" in t:
        return random.choice(["Why do programmers prefer dark mode? Because light attracts bugs 😂", "I’d tell you a UDP joke, but you might not get it. 😅"])
    return random.choice([
        "Interesting — tell me more.",
        "I didn't get that fully, can you rephrase?",
        "Got it. Want some suggestions or examples?"
    ])

def add_message(sender, text, status="sending"):
    mid = str(uuid.uuid4())
    msg = {"id": mid, "sender": sender, "text": text, "time": now_str(), "status": status, "reactions": []}
    messages.append(msg)
    render_message(msg)
    return mid

def render_message(msg):
    side = "e" if msg["sender"] == "user" else "w"
    bg = "#DCF8C6" if msg["sender"] == "user" else "#FFFFFF"
    fg = "#000000"
    frame = tk.Frame(msg_container, bg=container_bg)
    frame.pack(anchor=side, pady=6, padx=10, fill="x")
    bubble = tk.Frame(frame, bg=bg, bd=1, relief="solid")
    bubble.pack(side="right" if msg["sender"] == "user" else "left", padx=5)
    text_lbl = tk.Label(bubble, text=msg["text"], justify="left", bg=bg, fg=fg, wraplength=380, padx=8, pady=6, font=("Arial", 11))
    text_lbl.pack()
    meta = tk.Frame(bubble, bg=bg)
    meta.pack(fill="x", padx=6, pady=(0,4))
    time_lbl = tk.Label(meta, text=msg["time"], bg=bg, fg="#555555", font=("Arial", 8))
    time_lbl.pack(side="left")
    status_lbl = tk.Label(meta, text=msg["status"], bg=bg, fg="#555555", font=("Arial", 8))
    status_lbl.pack(side="right")
    react_lbl = tk.Label(frame, text=" ".join(msg["reactions"]), bg=container_bg, fg="#333333", font=("Arial", 10))
    react_lbl.pack(anchor=side, padx=10, pady=(0,0))
    frame.message_id = msg["id"]
    frame.bind("<Button-3>", lambda e, f=frame: on_right_click(e, f))
    text_lbl.bind("<Button-3>", lambda e, f=frame: on_right_click(e, f))
    widgets[msg["id"]] = {"frame": frame, "text": text_lbl, "time": time_lbl, "status": status_lbl, "reactions": react_lbl}
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def simulate_send(mid):
    def job():
        time.sleep(0.4)
        root.after(0, lambda: update_status(mid, "sent"))
        time.sleep(0.4)
        root.after(0, lambda: update_status(mid, "delivered"))
    threading.Thread(target=job, daemon=True).start()

def update_status(mid, new_status):
    for m in messages:
        if m["id"] == mid:
            m["status"] = new_status
            break
    w = widgets.get(mid)
    if w:
        w["status"].config(text=new_status)

def user_send(event=None, quick_text=None):
    t = quick_text if quick_text is not None else entry.get().strip()
    if not t:
        return
    entry.delete(0, tk.END)
    mid = add_message("user", t, status="sending")
    simulate_send(mid)
    root.after(100, lambda: bot_reply_simulation(t))

def bot_reply_simulation(user_text):
    typing_id = "typing"
    typing_widget = tk.Label(msg_container, text="Bot is typing...", bg=container_bg, fg="#666666", font=("Arial", 9, "italic"))
    typing_widget.pack(anchor="w", padx=12)
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)
    def job():
        time.sleep(0.9 + random.random()*1.2)
        root.after(0, typing_widget.destroy)
        bot_text = generate_bot_response(user_text)
        mid = add_message("bot", bot_text, status="delivered")
        simulate_send(mid)
    threading.Thread(target=job, daemon=True).start()

def on_right_click(event, frame):
    mid = getattr(frame, "message_id", None)
    if mid is None:
        return
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Edit", command=lambda: edit_message(mid))
    menu.add_command(label="Delete", command=lambda: delete_message(mid))
    menu.add_command(label="React", command=lambda: react_message(mid))
    menu.tk_popup(event.x_root, event.y_root)

def edit_message(mid):
    for m in messages:
        if m["id"] == mid:
            current = m["text"]
            break
    else:
        return
    popup = tk.Toplevel(root)
    popup.title("Edit message")
    popup.geometry("400x120")
    tk.Label(popup, text="Edit text:").pack(anchor="w", padx=8, pady=(8,0))
    edit_entry = tk.Entry(popup, font=("Arial", 12))
    edit_entry.pack(fill="x", padx=8, pady=6)
    edit_entry.insert(0, current)
    def save():
        new = edit_entry.get().strip()
        if not new:
            popup.destroy()
            return
        for m in messages:
            if m["id"] == mid:
                m["text"] = new
                break
        w = widgets.get(mid)
        if w:
            w["text"].config(text=new)
            w["time"].config(text=now_str())
        popup.destroy()
    tk.Button(popup, text="Save", command=save, bg="#4CAF50", fg="#fff").pack(pady=6)

def delete_message(mid):
    for i,m in enumerate(messages):
        if m["id"] == mid:
            messages.pop(i)
            break
    w = widgets.pop(mid, None)
    if w:
        w["frame"].destroy()

def react_message(mid):
    popup = tk.Toplevel(root)
    popup.title("Add reaction")
    popup.geometry("300x80")
    emojis = ["👍","❤️","😂","😮","😢","👏"]
    def add(e):
        for m in messages:
            if m["id"] == mid:
                if e not in m["reactions"]:
                    m["reactions"].append(e)
                break
        w = widgets.get(mid)
        if w:
            w["reactions"].config(text=" ".join(m["reactions"]))
        popup.destroy()
    for e in emojis:
        b = tk.Button(popup, text=e, font=("Arial", 14), command=lambda ch=e: add(ch))
        b.pack(side="left", padx=6, pady=12)

def do_search(event=None):
    q = search_entry.get().strip().lower()
    for m in messages:
        mid = m["id"]
        w = widgets.get(mid)
        if not w:
            continue
        if q and q in m["text"].lower():
            w["text"].config(bg="#fff9c4")
        else:
            bg = "#DCF8C6" if m["sender"]=="user" else "#FFFFFF"
            w["text"].config(bg=bg)

root = tk.Tk()
root.title("Advanced Chat (demo)")
root.geometry("520x650")
container_bg = "#F0F0F0"
root.configure(bg=container_bg)

topbar = tk.Frame(root, bg=container_bg)
topbar.pack(fill="x", padx=10, pady=6)
search_entry = tk.Entry(topbar, font=("Arial", 10))
search_entry.pack(side="left", padx=(0,6), fill="x", expand=True)
search_entry.bind("<Return>", do_search)
tk.Button(topbar, text="Search", command=do_search).pack(side="left", padx=4)
tk.Button(topbar, text="Clear", command=lambda: (search_entry.delete(0,tk.END), do_search())).pack(side="left", padx=4)

canvas_frame = tk.Frame(root, bg=container_bg)
canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0,6))
canvas = tk.Canvas(canvas_frame, bg=container_bg, highlightthickness=0)
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
msg_container = tk.Frame(canvas, bg=container_bg)
canvas.create_window((0,0), window=msg_container, anchor="nw")
def on_config(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
msg_container.bind("<Configure>", on_config)

quick_frame = tk.Frame(root, bg=container_bg)
quick_frame.pack(fill="x", padx=10, pady=(0,6))
quick_replies = ["Hello", "Tell me a joke", "What time is it?", "Help me"]
for qr in quick_replies:
    b = tk.Button(quick_frame, text=qr, command=lambda t=qr: user_send(quick_text=t))
    b.pack(side="left", padx=6, pady=4)

entry_frame = tk.Frame(root, bg=container_bg)
entry_frame.pack(fill="x", padx=10, pady=8)
entry = tk.Entry(entry_frame, font=("Arial", 12))
entry.pack(side="left", fill="x", expand=True, padx=(0,6))
entry.bind("<Return>", user_send)
send_btn = tk.Button(entry_frame, text="Send", command=user_send, bg="#2196F3", fg="#fff")
send_btn.pack(side="right")

add_message("bot", "Welcome! I'm your assistant. Try typing 'joke', 'time', 'help', or say hi!", status="delivered")
root.mainloop()
