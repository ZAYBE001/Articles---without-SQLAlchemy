# lib/models/magazine.py
import sqlite3
from . import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
        else:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
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
        cursor.execute("""
            SELECT * FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        return cursor.fetchall()

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* 
            FROM authors a
            JOIN articles ON a.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        return cursor.fetchall()

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        return [row[0] for row in cursor.fetchall()]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.* FROM authors a
            JOIN articles ON a.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(articles.id) > 2
        """, (self.id,))
        return cursor.fetchall()

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazine_id, COUNT(*) as article_count
            FROM articles
            GROUP BY magazine_id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls.find_by_id(row[0])
        return None