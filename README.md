---

# Data Explainer API

This project is a **FastAPI-powered RESTful API** designed to fetch, cache, and explain data results in plain language. It connects to a **MySQL database**, utilizes **Redis** for caching, and integrates **Grok AI** for generative AI interactions.

The API provides tools to analyze crime statistics using sample data extracted from the [Crime Data from 2020 to Present](https://catalog.data.gov/dataset/crime-data-from-2020-to-present). This dataset offers insights into crime trends and patterns, making it easier to generate meaningful interpretations and explanations with the help of Grok AI integration.

## Features
- **FastAPI Framework** for scalable and modern Python API development.
- **MySQL Database** for data storage and querying.
- **Redis Cache Layer** to enhance performance by reducing database load.
- **Generative AI Integration** powered by Grok AI, enabling natural language explanations.
- **Dockerized Environment** for seamless deployment and consistency across systems.

---

## Prerequisites
- **Docker** and **Docker Compose** installed.
- A valid **Grok AI API Key**. Sign up for one at [Grok AI Documentation](https://docs.x.ai/docs).

---

## Getting Started

### Clone the Repository
```bash
git clone https://github.com/your-username/data-explainer-api.git
cd data-explainer-api
```

### Create a `.env` File
Create a `.env` file in the root directory with the following contents:
```dotenv
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=data_explainer_db
MYSQL_USER=default_user
MYSQL_PASSWORD=default_password
XAI_API_KEY=REPLACE_WITH_YOUR_API_KEY_HERE
```
- Replace `REPLACE_WITH_YOUR_API_KEY_HERE` with your **[Grok AI API Key](https://docs.x.ai/docs)**.

### Build and Start the Application
Run the following command to build and start the containers:
```bash
docker-compose up --build
```

In case you want to end the containers:
```bash
docker-compose down -v
```

The API will be available at: `http://localhost:8000`.

---

## API Endpoints

### Example Endpoints
For the complete list of endpoints and detailed documentation, visit the Swagger UI at `http://localhost:8000/docs`.
---

## Architecture

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: MySQL
- **Cache Layer**: Redis
- **Generative AI**: Grok AI
- **Containerization**: Docker and Docker Compose

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

