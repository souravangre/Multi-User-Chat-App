
---

# 🖥 Multi-User Chat App (Python Sockets & Threading)

A **console-based chat application** built from scratch in Python using **TCP sockets and threading**. This project demonstrates **low-level networking, concurrency, and client-server architecture**. Users can connect to the server, chat with multiple clients simultaneously, and have their messages identified by **usernames**.

---

## 🚀 Features

* Multi-client chat in real-time.
* Each client has a **username**.
* Broadcast messages to **all connected clients**.
* Join/Leave notifications when clients connect or disconnect.
* Lightweight and easy to run locally.

---

## 🏗 Architecture

1. **Server (`server.py`)**

   * Accepts incoming TCP connections.
   * Handles each client in a **separate thread**.
   * Broadcasts messages to all clients except the sender.

2. **Client (`client.py`)**

   * Connects to the server and sends messages.
   * Sends username and prefixes each message with it.
   * Receives messages from other clients in **real-time**.
   * Supports clean exit (`/quit` or `/exit`).

---

## 🛠 Technologies Used

* Python 3.x
* `socket` library for networking
* `threading` for handling multiple clients
* Console-based interface (no GUI)

---

## 📋 Prerequisites

* Python 3 installed on your machine
* Basic understanding of **terminal commands**

---

## ⚡ Installation & Usage

1. **Clone the repository**

```bash
git clone https://github.com/souravangre/Multi-User-Chat-App.git
cd Multi-User-Chat-App
```

2. **Run the server**

```bash
python server.py
```

3. **Run one or more clients** (in separate terminal windows)

```bash
python client.py
```

4. **Enter your username** when prompted.
5. **Type messages** and press Enter to send.
6. **Exit chat** by typing `/quit` or `/exit`.

---

## 💡 Example Chat

```
[join] Sourav joined the chat
Sourav: Hello everyone
Nova: Hi Sourav!
[leave] Nova left the chat
```

---

## 📂 Project Structure

```
multi-user-chat-app/
├── server.py       # Chat server
├── client.py       # Chat client
└── README.md       # This documentation
```

---

## ✅ Key Learning Outcomes

* Understand **TCP sockets and networking basics**.
* Handle **multiple clients concurrently** using Python threads.
* Implement a **chat protocol** with usernames, join/leave notifications.
* Build a functional **networked Python application** from scratch.

---

## 🧩 Future Enhancements

* Add a **Tkinter GUI** for a desktop client.
* Implement **private messaging** between users.
* Convert to a **web-based chat app** using Flask + WebSockets for online access.

---

## 📜 License

MIT License © \[Sourav]

---

