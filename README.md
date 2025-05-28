# Articles---without-SQLAlchemy
# Code Challenge

This project is a code challenge for managing authors, articles, and magazines using SQLAlchemy.

## Directory Structure

- `lib/`: Main code directory
  - `models/`: Model classes
    - `author.py`: Author class with SQL methods
    - `article.py`: Article class with SQL methods
    - `magazine.py`: Magazine class with SQL methods
  - `db/`: Database components
    - `connection.py`: Database connection setup
    - `seed.py`: Seed data for testing
    - `schema.sql`: SQL schema definitions
  - `controllers/`: Optional business logic
    - `__init__.py`
  - `debug.py`: Interactive debugging
- `tests/`: Test directory
  - `test_author.py`: Tests for Author class
  - `test_article.py`: Tests for Article class
  - `test_magazine.py`: Tests for Magazine class
- `scripts/`: Helper scripts
  - `setup_db.py`: Script to set up the database
  - `run_queries.py`: Script to run example queries
- `README.md`: Project documentation

## Getting Started

1. Clone the repository.
2. Run `scripts/setup_db.py` to set up the database.
3. Run tests using `pytest`.

## Contributing

Feel free to contribute by opening issues or pull requests.