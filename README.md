# AI Assistant API (Flask + SQLite)

This is a simple REST API for an AI assistant built with **Flask** and **SQLite**.  
It allows you to:
- **Start a new chat** (`/new`)
- **Retrieve past chat messages** (`/chat/<chat-id>`)
- **Send a new message and get a response** (`/chat/<chat-id>`)

---

## **Installation and Setup**

### **1. Install Dependencies using pipenv**
```sh
pipenv install
```

### **2. Activate Virtual Environment**
```sh
pipenv shell
```

### **3. Run the Flask Server**
```sh
python app.py
```
The API will now be running at:  
📌 `http://127.0.0.1:5000`

---

## **How to Use the API**

### **1. Start a New Chat**
```sh
curl -X POST http://127.0.0.1:5000/new
```
#### **Response**
```json
{
  "chat_id": "some-uuid",
  "url": "http://127.0.0.1:5000/chat/some-uuid"
}
```

---

### **2. Retrieve an Existing Chat**
```sh
curl -X GET http://127.0.0.1:5000/chat/<chat-id>
```
#### **Response**
```json
{
  "chat_id": "<chat-id>",
  "messages": [
    {"role": "user", "content": "Hello AI!"},
    {"role": "assistant", "content": "Hello human!"}
  ]
}
```

---

### **3. Send a Message to a Chat**
```sh
curl -X POST http://127.0.0.1:5000/chat/<chat-id> \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello AI!"}'
```
#### **Response**
```json
{
  "chat_id": "<chat-id>",
  "messages": [
    {"role": "user", "content": "Hello AI!"},
    {"role": "assistant", "content": "Hello human!"}
  ],
  "response": "Hello human!"
}
```
