# ChatGPT-developed Microservice

## Description

This service is composed of three containers: UI, Middleware, and PostgreSQL

```mermaid
graph LR;
  style[style=bold, color=blue];
  UI["UI Container"];
  
  style[style=bold, color=green];
  Middleware["Middleware Container"];
  
  style[style=bold, color=orange];
  Postgres["PostgreSQL Container"];
  
  UI -->|Requests| Middleware;
  Middleware -->|Database Operations| Postgres;
```

## Prerequisites

- Docker
- Python

## Getting Started

### Building Docker Images

```bash
# build images
make build

# start containers
make run

# stop and remove containers
make clean
```

Access the UI at [http://localhost:8080](http://localhost:8080).

## Service Architecture

- **UI Container:**
  - Image: ui-container
  - Port: 8080
  - Access the UI at [http://localhost:8080](http://localhost:8080).

- **Middleware Container:**
  - Image: middleware-container
  - Port: 5150
  - Access middleware API at [http://localhost:5150/api/data](http://localhost:5150/api/data).

- **PostgreSQL Container:**
  - Image: postgres-container
  - Port: 5432
  - Default Credentials:
    - User: myuser
    - Password: mypassword
    - Database: mydatabase

## Additional Configuration

- Adjust IP addresses and ports in the Makefile and Dockerfiles according to your requirements.
- Modify the database connection parameters in middleware/app.py if needed.

## Development and Testing

For development and testing, consider the following:

- Ensure Python dependencies are installed in your middleware and ui containers.
- Update the middleware/app.py and ui/app.py files as needed.
- Use Docker Compose for a more comprehensive development environment.

## Known Issues

Describe any known issues or limitations of your service.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
