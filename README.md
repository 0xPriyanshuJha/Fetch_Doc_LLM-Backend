## Fetch_Doc_LLM-Backend
This project uses MySQL, Python (FastAPI), and many web technologies to build a web scraping and retrieval system. Hacker News is the source of the news data that is scraped, stored in a database, and made available for retrieval and manipulation. The application is containerized using Docker, which facilitates deployment.
### Table of Contents
## Table of Contents
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Database Configuration](#database-configuration)
- [Environment Variables](#environment-variables)
- [Citing Open-Source Code](#citing-open-source-code)
- [Challenges and Solutions](#challenges-and-solutions)

## Project Structure
- app/: Contains application-specific logic.
- models/: Includes the Python models for database interactions.
- services/: Services such as web scraping and data retrieval.
- venv/: Python virtual environment for dependency management.
- docker-compose.yml: Config file for running the app and MySQL in Docker containers.
- Dockerfile: Docker build instructions for the Python app.
- requirements.txt: Python package dependencies.
  
## Technologies Used
* Python 3.11
* MySQL: For database storage.
* BeautifulSoup: For web scraping.
* Docker & Docker-Compose: For containerizing the application.
* Streamlit: For the frontend.


## Setup Instructions
Clone the Repository:

```bash
git clone https://github.com/0xPriyanshuJha/Fetch_Doc_LLM-Backend
cd Fetch_Doc_LLM-Backend
```
Set Up Virtual Environment:
``` bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

```pip install -r requirements.txt```

* Configure the Environment: Ensure you have a .env file in the root directory containing:

### makefile
```bash
MYSQL_ROOT_PASSWORD=<your_password>
MYSQL_DATABASE=<db_name>
MYSQL_USER=<username>
MYSQL_PASSWORD=<password>
```

Run the Application using Docker: Make sure you have Docker installed.
```bash
docker-compose up --build
```
* This will set up the MySQL database, web scraper, and the app in their respective containers.

## Database Configuration:
- This project uses MySQL as the database. The connection details are provided in the docker-compose.yml file. The MySQL container is initialized with the environment variables you define.

## Environment Variables:
- Must configure environment variables in a .env file. This ensures that sensitive data (like passwords) is not committed to the repository.


## Citing Open-Source Code
This project uses the following open-source repositories:
- [Faiss](https://github.com/facebookresearch/faiss)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)


## Challenges and Solutions
* Handling Data Scraping: The scraper needed to be optimized for rate-limiting to avoid IP bans. Implemented threading and added a sleep timer between requests.

* Error Handling in Web Scraping: Using try-except blocks for handling HTTP errors and incorrect HTML structures prevented the scraper from breaking when it encountered issues.

* Containerization with Docker: Docker allowed us to avoid environment-related issues. By containerizing both the app and the MySQL database, Able to ensure consistency between development and production environments.

* SQL Password Management: Passwords for the database are stored securely in environment variables, and not committed to GitHub, ensuring security best practices are followed.
