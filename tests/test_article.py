# tests/test_article.py
import pytest
from lib.models.article import Article

@pytest.fixture(scope="module")
def setup_db():
    from lib.db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    yield conn
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_article_save(setup_db):
    article = Article(title="Python Tips", author_id=1, magazine_id=1)
    article.save()
    assert article.id is not None

def test_article_find_by_id(setup_db):
    article = Article(title="Python Tips", author_id=1, magazine_id=1)
    article.save()
    found_article = Article.find_by_id(article.id)
    assert found_article.title == "Python Tips"
    assert found_article.author_id == 1
    assert found_article.magazine_id == 1

def test_article_find_by_title(setup_db):
    article = Article(title="Python Tips", author_id=1, magazine_id=1)
   