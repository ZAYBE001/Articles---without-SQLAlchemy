# lib/db/seed.py
from .connection import get_connection
from ..models.author import Author
from ..models.magazine import Magazine
from ..models.article import Article

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Create authors
    author1 = Author(name="John Doe")
    author1.save()

    author2 = Author(name="Jane Smith")
    author2.save()

    # Create magazines
    magazine1 = Magazine(name="Tech Weekly", category="Technology")
    magazine1.save()

    magazine2 = Magazine(name="Health Monthly", category="Health")
    magazine2.save()

    # Create articles
    article1 = Article(title="Python Tips", author_id=author1.id, magazine_id=magazine1.id)
    article1.save()

    article2 = Article(title="AI Future", author_id=author1.id, magazine_id=magazine1.id)
    article2.save()

    article3 = Article(title="Healthy Living", author_id=author2.id, magazine_id=magazine2.id)
    article3.save()

    conn.close()

if __name__ == "__main__":
    seed_data()