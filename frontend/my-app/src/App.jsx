// app.jsx
import { useEffect, useState, useCallback } from 'react';
import './stylesheets/App.css';
import FormView from './components/FormView';
import Book from './components/Book';

const PAGE_SIZE = 5;

export default function App() {
  const [page, setPage] = useState(1);
  const [totalBooks, setTotalBooks] = useState(0);
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);

  const getBooks = useCallback(async (targetPage = 1) => {
    try {
      setLoading(true);
      const res = await fetch(`/books?page=${targetPage}`, { credentials: 'same-origin' });
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();

      setTotalBooks(data.total_books ?? 0);
      setBooks(Array.isArray(data.books) ? data.books : []);
      setPage(targetPage);
    } catch (err) {
      console.error(err);
      alert('Unable to load books. Please try your request again');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    getBooks(1);
  }, [getBooks]);

  const deleteBook = async (id) => {
    if (!window.confirm('Are you sure you want to delete the book?')) return;
    try {
      const res = await fetch(`/books/${id}`, { method: 'DELETE', credentials: 'same-origin' });
      if (!res.ok) throw new Error('Delete failed');
      await getBooks(page);
    } catch (err) {
      console.error(err);
      alert('Unable to delete the book.');
    }
  };

  const changeRating = async (id, rating) => {
    try {
      const res = await fetch(`/books/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ rating }),
      });
      if (!res.ok) throw new Error('Patch failed');

      // Atualiza somente o item alterado
      setBooks((prev) => prev.map((b) => (b.id === id ? { ...b, rating } : b)));
    } catch (err) {
      console.error(err);
      alert('Unable to update the rating.');
    }
  };

  const searchBooks = async (search) => {
    try {
      setLoading(true);
      const res = await fetch('/books', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ search }),
      });
      if (!res.ok) throw new Error('Search failed');

      const data = await res.json();
      setTotalBooks(data.total_books ?? 0);
      setBooks(Array.isArray(data.books) ? data.books : []);
      setPage(1);

      // Se seu FormView ainda usa id="search-form", isso mantém o comportamento antigo:
      const form = document.getElementById('search-form');
      if (form) form.reset();
    } catch (err) {
      console.error(err);
      alert('Unable to complete search. Please try your request again');
    } finally {
      setLoading(false);
    }
  };

  const selectPage = (num) => {
    getBooks(num);
  };

  const createPagination = () => {
    const maxPage = Math.max(1, Math.ceil(totalBooks / PAGE_SIZE));
    return Array.from({ length: maxPage }, (_, i) => i + 1).map((i) => (
      <div
        key={i}
        className={`page-num ${i === page ? 'active' : ''}`}
        onClick={() => selectPage(i)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => (e.key === 'Enter' ? selectPage(i) : null)}
      >
        {i}
      </div>
    ));
  };

  return (
    <div className="App">
      <div id="main-view">
        {loading && <div className="loading">Loading…</div>}
        <div className="bookshelf-container">
          {books.map((book) => (
            <Book
              key={book.id}
              deleteBook={deleteBook}
              changeRating={changeRating}
              {...book}
            />
          ))}
        </div>
        <div className="pagination-menu">{createPagination()}</div>
      </div>
      <FormView searchBooks={searchBooks} />
    </div>
  );
}
