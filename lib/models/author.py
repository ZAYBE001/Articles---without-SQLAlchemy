# lib/models/author.py
import sqlite3
from . import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        else:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], name=row[1])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], name=row[1])
        return None

    def articles(self):
     from .article import Article
     conn = get_connection()
     cur = conn.cursor()
     rows = cur.execute("SELECT * FROM articles WHERE author_id=?", (self.id,)).fetchall()
     conn.close()
     return [Article(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]

    def magazines(self):
        with get_connection() as conn:
            from .magazine import Magazine
           
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.*
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
            return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]
        
    def add_article(self, magazine, title):
        from .article import Article
        
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article
       

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT category FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self.id,))
        topic_areas=[row[0] for row in cursor.fetchall()]
        conn.close()
        return topic_areas
    
    @classmethod
    def top_author(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT author_id, COUNT(*) as article_count
                FROM articles
                GROUP BY author_id
                ORDER BY article_count DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                from lib.models.author import Author
                return Author.find_by_id(row[0])
        return None