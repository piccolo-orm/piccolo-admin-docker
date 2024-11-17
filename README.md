Dockerized Piccolo Admin to use existing (legacy) database.

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

### Additional Piccolo Admin configuration

Piccolo Admin has a flexible UI with lots of configuration options to display only the columns you want your users to see. More information on Piccolo Admin [docs](https://piccolo-admin.readthedocs.io/en/latest/index.html).

After Piccolo Admin is started with all the tables from the existing database, we can do additional configuration through the `config.yaml` file. 

Example of `config.yaml`:

```yaml
tables:
  # An example of additional Piccolo Admin configuration
  Actor:
    visible_columns:
      - first_name
    visible_filters:
      - actor_id
      - first_name
    menu_group: Movies
    link_column: first_name
  Address:
    visible_columns:
      - address_id
      - address
      - city_id
    visible_filters:
      - address_id
      - address
      - city_id
    menu_group: Location
    rich_text_columns: address
  City:
    visible_columns:
      - city_id
      - city
    visible_filters:
      - city_id
      - city
    menu_group: Location
  Country:
    visible_columns:
      - country_id
      - country
    visible_filters:
      - country_id
      - country
    menu_group: Location

sidebar_links:
  Piccolo Admin: https://piccolo-admin.readthedocs.io/en/latest/index.html
  Piccolo ORM: https://piccolo-orm.readthedocs.io/en/latest/index.html
```

For these changes to take effect, you must stop the container and rebuild it with.

```bash
docker-compose up -d --build
```