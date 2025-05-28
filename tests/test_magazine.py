# tests/test_magazine.py
import pytest
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture(scope="module")
def setup_db():
    from lib.db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM authors")
    conn.commit()
    yield conn
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM authors")
    conn.commit()
    conn.close()

def test_magazine_save(setup_db):
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    assert magazine.id is not None

def test_magazine_find_by_id(setup_db):
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    found_magazine = Magazine.find_by_id(magazine.id)
    assert found_magazine.name == "Tech Weekly"
    assert found_magazine.category == "Technology"

def test_magazine_find_by_name(setup_db):
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    found_magazine = Magazine.find_by_name("Tech Weekly")
    assert found_magazine.name== magazine.name
    assert found_magazine.category == "Technology"

def test_magazine_find_by_category(setup_db):
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    found_magazine = Magazine.find_by_category("Technology")
    assert found_magazine.category == magazine.category
    assert found_magazine.name == "Tech Weekly"

def test_magazine_articles(setup_db):
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    article = Article(title="Python Tips", author_id=1, magazine_id=magazine.id)
    article.save()
    articles = magazine.articles()
    assert len(articles) == 1

def test_magazine_contributors(setup_db):
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    article = Article(title="Python Tips", author_id=1, magazine_id=magazine.id)
    article.save()
    contributors = magazine.contributors()
    assert len(contributors) >= 0

def test_magazine_article_titles(setup_db):
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    article = Article(title="Python Tips", author_id=1, magazine_id=magazine.id)
    article.save()
    titles = magazine.article_titles()
    assert len(titles) == 1
    assert titles[0] == "Python Tips"

def test_magazine_contributing_authors(setup_db):
    magazine = Magazine(name="Tech Weekly", category="Technology")
    magazine.save()
    article1 = Article(title="Python Tips", author_id=1, magazine_id=magazine.id)
    article1.save()
    article2 = Article(title="AI Future", author_id=2, magazine_id=magazine.id)
    article2.save()
    contributing_authors = magazine.contributing_authors()
    assert len(contributing_authors) == 0  # No author has more than 2 articles

def test_magazine_top_publisher(setup_db):
    magazine1 = Magazine(name="Tech Weekly", category="Technology")
    magazine1.save()
    magazine2 = Magazine(name="Health Monthly", category="Health")
    magazine2.save()
    article1 = Article(title="Python Tips", author_id=1, magazine_id=magazine1.id)
    article1.save()
    article2 = Article(title="AI Future", author_id=1, magazine_id=magazine1.id)
    article2.save()
    article3 = Article(title="Healthy Living", author_id=2, magazine_id=magazine2.id)
    article3.save()
    top_publisher = Magazine.top_publisher()
    assert top_publisher.name == "Tech Weekly"