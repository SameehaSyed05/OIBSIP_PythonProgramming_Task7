# OIBSIP_PythonProgramming_Task7
📦 Packages Used

tkinter → For building the chat GUI

ttk (from tkinter) → For styled widgets like scrollbars

datetime → To add timestamps to messages

threading → To simulate typing and message delivery delays

time → For managing delays in bot replies and message status

uuid → To assign unique IDs to messages

random → For varied bot responses and jokes

🎯 Objective

This project demonstrates an interactive chat interface built with Tkinter.
It simulates a messaging app experience with features like message bubbles, reactions, editing, deleting, searching, and bot replies.

🚀 Features

Send messages and see them appear in chat bubbles

Bot responses with typing indicator simulation

Message statuses: sending → sent → delivered

Edit / Delete / React (via right-click menu on messages)

Reactions with emoji support (👍 ❤️ 😂 😮 😢 👏)

Search bar to highlight matching messages

Quick replies (preset buttons like “Hello”, “Tell me a joke”)

Scroll support with a modern-looking chat window

Automatic timestamps on every message

🖥️ How It Works

Type a message and press Enter or click Send.

Your message is displayed with a sending → sent → delivered status.

The bot replies after a short simulated typing delay.

Right-click any message to edit, delete, or react with emojis.

Use the search bar to find messages quickly.

Use the quick reply buttons for instant interaction.

📂 File Information

chat_app.py → Main script containing GUI, bot logic, and message features.

▶️ How to Run

Install Python (3.x recommended).

Save the script as chat_app.py.

Run with:

python chat_app.py


The chat interface window will open.

🔑 Example Interactions

User: Hello

Bot: Hey! 👋 How can I help you today?

User: What time is it?

Bot: The current time is 14:22:10.

User: Tell me a joke

Bot: Why do programmers prefer dark mode? Because light attracts bugs 😂
