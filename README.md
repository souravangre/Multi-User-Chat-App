---

# 🔗 TCP Chat App with Authentication

A simple **multi-client chat application** built using Python’s **socket programming** and **SQLite** for user authentication.
This project demonstrates core concepts of networking (TCP/IP), concurrency (threading), and authentication without relying on external frameworks like Flask/Django.

---

## 🚀 Features

* 🔐 **User Authentication**

  * Sign up with a username & password
  * Login before entering the chat room
  * Credentials securely stored in SQLite

* 💬 **Single Chat Room**

  * Multiple clients can connect to the same server
  * Messages broadcast to all connected users

* 🧵 **Multi-threaded Server**

  * Handles multiple client connections simultaneously

* 🛠 **Pure Python**

  * Built with only the standard library (`socket`, `threading`, `sqlite3`)

---

## 📂 Project Structure

```
Multi-User-Chat-App/
│── authserver.py        # Main server script with auth + chat handling
│── authclient.py        # Client script to connect and chat
│── chat_users.db        # SQLite database for user authentication
│── README.md            # Documentation
```

---

## ⚙️ How It Works

1. **Server starts** and listens for client connections.
2. On **client connect**, user is prompted to **login or register**.
3. Credentials are verified/stored in the SQLite database.
4. Once authenticated, the client joins the **shared chatroom**.
5. Messages are **broadcasted** to all connected users.

---

## 🖥️ Setup & Usage

### 1. Clone the repository

```bash
git clone https://github.com/souravangre/Multi-User-Chat-App.git
cd Multi-User-Chat-App
```

### 2. Start the server

```bash
python authserver.py
```

### 3. Run a client (open multiple terminals for multiple clients)

```bash
python authclient.py
```

### 4. Register/Login and start chatting 🎉

---

## 🧑‍💻 Example

**Client 1:**

```
Enter choice (login/register): register
Username: alice
Password: ****
[System]: alice has joined the chat
```

**Client 2:**

```
Enter choice (login/register): login
Username: bob
Password: ****
[System]: bob has joined the chat
alice: Hi Bob!
bob: Hey Alice!
```

---

## 📖 Learning Outcomes

✅ Understanding of **TCP sockets**
✅ Handling **concurrency with threads**
✅ Implementing a **basic authentication system**
✅ Designing without frameworks → **strong grasp of fundamentals**

---

## 🔮 Future Enhancements

* Multiple chat rooms / private chats
* End-to-end encryption for messages
* GUI client with Tkinter or PyQt
* Admin commands (kick/ban users)

---

## 🤝 Contribution

Feel free to fork, raise issues, or submit PRs if you’d like to enhance the project!

---

## 📜 License

MIT License – free to use and modify.

---

