# 🏨 Agentic AI Hotel Reservation & Intelligent Recommendation System

<p align="center">
  <img src="Banner.jpeg" alt="Project Banner" width="100%"/>
</p>

An intelligent hotel reservation and recommendation system powered by Agentic AI.

> Graduation Project -- FCAI -- BSNU

---

## 📁 Project Structure

```
├── src/
│   ├── main.py               
│   ├── .env                  
│   ├── .env.example           
│   ├── requirements.txt     
│   ├── helpers/
│   │   ├── __init__.py
│   │   └── config.py           
│   ├── enums/
│   │   ├── __init__.py
│   │   └── ResponseEnums.py   
│   └── routes/
│       ├── __init__.py
│       └── health.py          
├── postman/                    
├── LICENSE                    
└── README.md
```

---

## ⚙️ Prerequisites

- **Miniconda** (or Anaconda) — [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- **Git**

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/beshoy-osama/Agentic-AI-Hotel-Reservation-Intelligent-Recommendation-System.git
cd Agentic-AI-Hotel-Reservation-Intelligent-Recommendation-System
```

### 2. Create a Conda Environment

```bash
conda create -n hotel-ai python=3.11.16 -y
```

**Activate the environment:**

- **Linux / macOS:**
  ```bash
  conda activate hotel-ai
  ```
- **Windows:**
  ```cmd
  conda activate hotel-ai
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
