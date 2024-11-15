Experimenting with using a dockerized Piccolo Admin with an existing (legacy) database.

### Usage

Clone repository.

```bash
git clone https://github.com/piccolo-orm/piccolo-admin-docker.git
```

Creating an `.env` file.

```bash
cp .env.example .env && rm .env.example
```

Run the Docker container.

```bash
docker-compose up -d
```

After site is running log in as admin user on [localhost:8000](http://localhost:8000) and use legacy database.

Stop the Docker container.

```bash
docker-compose down
```