# FastAPI Test

A beginner-friendly REST API built using **Python**, **FastAPI**, and **Uvicorn**. The application provides a simple root endpoint and a greeting endpoint that accepts a name as a URL path parameter.

## Features

- Built with FastAPI
- Runs using Uvicorn
- Supports `GET /` root endpoint
- Supports `GET /greet/{name}` endpoint
- Uses path parameters
- Automatic interactive API documentation
- Lightweight and easy to understand
- All application code is contained in `main.py`

## Project Structure

```text
grade-system/
├── main.py
└── venv/
```

## Prerequisites

Install the required packages:

```bash
pip install fastapi uvicorn
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## API Endpoints

### Root Endpoint

```http
GET /
```

**Response**

```json
{
  "message": "Welcome to FastAPI Grade Calculator"
}
```

### Greeting Endpoint

```http
GET /greet/{name}
```

**Example Request**

```http
GET /greet/Gopi
```

**Response**

```json
{
  "message": "Hello Gopi"
}
```

## Interactive API Documentation

FastAPI automatically generates API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

## Output

When the server starts successfully, you should see output similar to:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
INFO:     Started server process
```

<img width="1496" height="743" alt="Screenshot 2026-08-27 at 7 31 41 PM" src="https://github.com/user-attachments/assets/9aa46bed-e497-4f09-9556-b5d6a530e6ab" />
<img width="1496" height="552" alt="Screenshot 2026-08-27 at 7 32 08 PM" src="https://github.com/user-attachments/assets/025b0ce7-76f5-4cb5-aa60-a301ad841769" />

# Streamlit Grade Calculator

A simple, clean, and user-friendly grade calculator built using **Python** and **Streamlit**. Enter a mark between 0 and 100, and the application automatically calculates and displays the corresponding letter grade.

## Features

- Built with Streamlit
- Simple and responsive user interface
- Accepts marks between 0 and 100
- Automatic grade calculation
- Clear and easy-to-read result display
- Progress indicator
- Grading scale reference table
- User-friendly success, information, warning, and error messages
- No database required
- All application logic is contained in `grade_system.py`

## Project Structure

```text
grade-system/
├── grade_system.py
├── requirements.txt
└── venv/
```

## Grading Scale

| Mark Range | Grade |
|------------|-------|
| 90 - 100 | A |
| 80 - 89 | B |
| 70 - 79 | C |
| 60 - 69 | D |
| 0 - 59 | E |

### Examples

```text
90 → A
80 → B
70 → C
60 → D
59 → E
```

## Prerequisites

Install Streamlit:

```bash
pip install streamlit
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run grade_system.py
```

The application will be available in your browser at:

```text
http://localhost:8501
```

## How It Works

1. Enter a mark between 0 and 100.
2. Click the calculate button (if implemented).
3. The application validates the input.
4. The corresponding letter grade is calculated.
5. The result is displayed along with the grading scale.

## Sample Output

### Input

```text
Mark: 95
```

### Output

```text
Grade: A
```

### Input

```text
Mark: 75
```

### Output

```text
Grade: C
```

<img width="635" height="642" alt="Screenshot 2026-08-27 at 7 27 13 PM" src="https://github.com/user-attachments/assets/4990a1ba-51b8-4e2c-ad29-9d2fbdc9b253" />

