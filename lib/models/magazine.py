from . import get_connection
from .article import Article
from .author import Author

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], name=row[1], category=row[2])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], name=row[1], category=row[2])
        return None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], name=row[1], category=row[2])
        return None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id = ?",
            (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4]) for row in rows]

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* 
            FROM authors a
            JOIN articles ON a.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(id=row[0], name=row[1]) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, COUNT(articles.id) as article_count
            FROM authors a
            JOIN articles ON a.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(id=row[0], name=row[1]) for row in rows]

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazine_id, COUNT(*) as count
            FROM articles
            GROUP BY magazine_id
            ORDER BY count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls.find_by_id(row[0])
        return None

    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING COUNT(DISTINCT a.author_id) > 1
        """)
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], category=row[2]) for row in rows]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT m.id, m.name, m.category, COUNT(a.id) as article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """).fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], category=row[2]) for row in rows]