<p align="center">
  <img src="https://app.hcdn.gob.ar/assets/img/logo-hcdn.png" height="100px"/>
</p>

# IADA

This study proposes a system that uses NLP technologies to facilitate access to legislative information in the Chamber of Deputies of the Nation Argentina. The system is based on an LLM and a user-centered design, and aims to improve transparency and citizen participation in the legislative process.

The academic paper can be found in the `/documents` directory.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Development](#development)
- [License](#license)
- [Contact](#contact)

## Installation

To install and run a Docker project, follow these steps:

1. Install Docker:

   - For Windows: Download and install Docker Desktop from the official Docker website.
   - For macOS: Download and install Docker Desktop from the official Docker website.
   - For Linux: Follow the instructions specific to your Linux distribution to install Docker.

2. Clone the project repository:

   ```
   git clone https://github.com/bartolomeoadrian/iada
   ```

3. Navigate to the project directory:

   ```
   cd iada
   ```

4. Run the Docker ecosystem:

   ```
   docker compose up
   ```

5. Access the application:
   Open a web browser and navigate to `http://localhost` to access the running Docker application.

That's it! You have successfully installed and run the Docker project. For more advanced configuration and usage, refer to the project's documentation.

## Configuration

To configure the project, create a `.env` file in the root directory of the project and add the following variables:

```
COMPOSE_PROJECT_NAME=iada
PORT=80
POSTGRES_URL=postgres://postgres:postgres@postgresql:5432/postgres
CHROMA_URL=http://chroma:8000
```

Make sure to replace the values of `POSTGRES_URL` and `CHROMA_URL` with the appropriate URLs for your PostgreSQL and Chroma instances.

Save the `.env` file and you're all set!

## Development

Containers you might need to develop

1. Chroma:

   ```
   docker run -p 8000:8000 chromadb/chroma:0.5.4
   ```

2. PostgreSQL:

   ```
   docker run -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres:16.3
   ```

To start developing the backend of the project using FastAPI and Python, follow these steps:

1. Make sure you have Python installed on your machine. You can download it from the official Python website.

2. Clone the project repository:

   ```
   git clone https://github.com/bartolomeoadrian/iada
   ```

3. Navigate to the project directory:

   ```
   cd iada
   ```

4. Navigate to the backend directory:

   ```
   cd docker/iada/src/backend
   ```

5. Create a new virtual environment for your project:

   ```shell
   python -m venv ./.venv
   ```

6. Activate the virtual environment:

   - For Windows:

     ```shell
     ./.venv/Scripts/activate
     ```

   - For macOS/Linux:

     ```shell
     source ./.venv/bin/activate
     ```

7. Install the project dependencies:

   ```shell
   pip install -r requirements.txt
   ```

8. Start the development server:

   ```shell
   uvicorn src.main:app --reload-dir ./src --port 3001
   ```

   This command will start the FastAPI development server and automatically reload the server whenever you make changes to your code. You can access the development server at `http://localhost:3001`.

9. Start coding!

   You can now start coding your backend endpoints and logic. Any changes you make will be automatically reflected in the server.

That's it! You have successfully set up the backend development environment using FastAPI and Python. Happy coding!

To start developing the frontend of the project, follow these steps:

1. Make sure you have Node.js installed on your machine. You can download it from the official Node.js website.

2. Clone the project repository:

   ```
   git clone https://github.com/bartolomeoadrian/iada
   ```

3. Navigate to the project directory:

   ```
   cd iada
   ```

4. Navigate to the frontend directory:

   ```
   cd docker/iada/src/frontend
   ```

5. Install the project dependencies:

   ```
   npm install
   ```

6. Start the development server:

   ```
   npm run dev
   ```

   This command will start the Vite development server and compile your frontend code. You can access the development server at `http://localhost:3000`.

7. Start coding!

   You can now start coding your frontend components and styles. Any changes you make will be automatically reflected in the browser.

That's it! You have successfully set up the frontend development environment using Vite. Happy coding!

## License

This project is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

You are free to:

- Share: Copy and redistribute the material in any medium or format.
- Adapt: Remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

- Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For more details, please refer to the [full license text](https://creativecommons.org/licenses/by/4.0/legalcode).

## Contact

If you have any questions or feedback regarding this project, feel free to reach out to me. You can contact me via email at [bartolomeoadriangonzalez@gmail.com](mailto:bartolomeoadriangonzalez@gmail.com) or through my GitHub repository at [github.com/bartolomeoadrian/iada](github.com/bartolomeoadrian/iada). I would be happy to assist you!
