# 🏨 Agentic AI Hotel Reservation & Intelligent Recommendation System

An intelligent hotel reservation and recommendation system powered by Agentic AI.

> Graduation Project — Built with FastAPI & Python.

---

## 📁 Project Structure

```
├── src/
│   ├── main.py                 # Application entry point (FastAPI)
│   ├── .env                    # Environment variables (not tracked by Git)
│   ├── .env.example            # Environment variables template
│   ├── requirements.txt        # Python dependencies
│   ├── helpers/
│   │   ├── __init__.py
│   │   └── config.py           # Application settings (Pydantic Settings)
│   ├── enums/
│   │   ├── __init__.py
│   │   └── ResponseEnums.py    # Response message constants
│   └── routes/
│       ├── __init__.py
│       └── health.py           # Health check endpoint
├── postman/                    # Postman collections for API testing
├── LICENSE                     # Apache 2.0 License
└── README.md
```

---

## ⚙️ Prerequisites

- **Python** 3.10+
- **pip** (Python package manager)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/beshoy-osama/Agentic-AI-Hotel-Reservation-Intelligent-Recommendation-System.git
cd Agentic-AI-Hotel-Reservation-Intelligent-Recommendation-System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

**Activate the virtual environment:**

- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```

### 3. Install Dependencies

```bash
pip install -r src/requirements.txt
```

### 4. Set Up Environment Variables

Copy the `.env.example` file to `.env` inside the `src` directory:

```bash
cp src/.env.example src/.env
```

### 4. Run the Server

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see output similar to:

```
Application is starting up...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 📖 Interactive API Documentation

Once the server is running, you can access the interactive docs at:

| Docs       | URL                              |
|------------|----------------------------------|
| Swagger UI | http://localhost:8000/docs       |
| ReDoc      | http://localhost:8000/redoc      |

---

## 🧪 Testing with Postman

The project includes ready-to-use Postman collections in the `postman/` directory. Import them into Postman to test the API endpoints directly.

---

## 🛠️ Tech Stack

| Technology         | Description                                      |
|-------------------|-------------------------------------------------- |
| FastAPI           | High-performance web framework for building APIs  |
| Uvicorn           | ASGI server for running FastAPI applications      |
| Pydantic Settings | Application settings management via env variables |
| python-dotenv     | Load environment variables from `.env` files      |

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).
