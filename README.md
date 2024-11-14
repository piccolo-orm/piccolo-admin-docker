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

Creating a Docker image.

```bash
docker build -t piccolo_admin .
```

Running a Docker image (use the `--network=host` flag for an existing database from the local machine).

```bash
docker run --env-file .env -d --network=host --name admin_container piccolo_admin
```

After site is running log in as admin user on [localhost:8000](http://localhost:8000/admin/) and use legacy database.