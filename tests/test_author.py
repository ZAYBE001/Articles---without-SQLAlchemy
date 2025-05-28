# tests/test_author.py
import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
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

def test_author_save(setup_db):
    author = Author(name="John Doe")
    author.save()
    assert author.id is not None

def test_author_find_by_id(setup_db):
    author = Author(name="John Doe")
    author.save()
    found_author = Author.find_by_id(author.id)
    assert found_author.name == "John Doe"

def test_author_find_by_name(setup_db):
    author = Author(name="John Doe")
    author.save()
    found_author = Author.find_by_name("John Doe")
    assert found_author.name == author.name

def test_author_articles(setup_db):
    author = Author(name="John Doe")
    author.save()
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    article = Article(title="Python Tips", author_id=author.id, magazine_id=magazine.id)
    article.save()
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0][1] == "Python Tips"

def test_author_magazines(setup_db):
    author = Author(name="John Doe")
    author.save()
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    article = Article(title="Python Tips", author_id=author.id, magazine_id=magazine.id)
    article.save()
    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0][1] == "Tech Weekly"

def test_author_add_article(setup_db):
    author = Author(name="John Doe")
    author.save()
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    author.add_article(magazine, "Python Tips")
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0][1] == "Python Tips"

def test_author_topic_areas(setup_db):
    author = Author(name="John Doe")
    author.save()
    magazine1 = Magazine(name="Tech Weekly", category="Technology")
    magazine1.save()
    magazine2 = Magazine(name="Health Monthly", category="Health")
    magazine2.save()
    author.add_article(magazine1, "Python Tips")
    author.add_article(magazine2, "Healthy Living")
    topic_areas = author.topic_areas()
    assert len(topic_areas) == 2
    assert "Technology" in topic_areas
    assert "Health" in topic_areas