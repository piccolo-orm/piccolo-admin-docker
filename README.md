Experimenting with using a dockerized Piccolo Admin with an existing (legacy) database.

### Usage

Clone repository.

```bash
git clone https://github.com/sinisaos/piccolo-admin-docker.git
```

Creating an `.env` file.

```bash
cd app
cp .env.example .env && rm .env.example
cd ..
```
Creating a Docker image.

```bash
docker build -t piccolo_admin .
```

Running a Docker image (using the `--network=host` flag because I'm using an existing database from the local machine).

```bash
docker run -d --network=host --name admin_container piccolo_admin
```

After site is running log in as admin user on [localhost:8000](http://localhost:8000/admin/) and use legacy database.