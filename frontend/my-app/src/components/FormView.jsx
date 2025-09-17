import React, { useState } from 'react';

import '../stylesheets/FormView.css';

const url_bookshelf_server = 'http://localhost:5000';

const FormView = ({ searchBooks }) => {
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [rating, setRating] = useState(1);
  const [search, setSearch] = useState('');

  const submitBook = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch(`${url_bookshelf_server}/books`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          author,
          rating: parseInt(rating),
        }),
      });

      if (!response.ok) {
        throw new Error('Falha ao adicionar o livro.');
      }

      // Limpa os campos do formulário após o sucesso
      setTitle('');
      setAuthor('');
      setRating(1);
      
      // O reset do formulário não é mais necessário, já que o estado já foi limpo.
      // O formulário é atualizado pelo React (controlled components).

    } catch (error) {
      console.log(error)
      alert('Não foi possível adicionar o livro. Por favor, tente novamente.');
    }
  };

  const handleSearch = (event) => {
    event.preventDefault();
    searchBooks(search);
  };

  return (
    <div id="form-view">
      <div className="search" style={{ display: 'None' }}>
        <h2>Search</h2>
        <form className="FormView" id="search-form" onSubmit={handleSearch}>
          <input 
            type="text" 
            name="search" 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
      <h2>Add a New Book</h2>
      <form className="FormView" id="add-book-form" onSubmit={submitBook}>
        <label>
          Title
          <input 
            type="text" 
            name="title" 
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </label>
        <label>
          Author
          <input 
            type="text" 
            name="author" 
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
          />
        </label>
        <label>
          Rating
          <select 
            name="rating" 
            value={rating}
            onChange={(e) => setRating(e.target.value)}
          >
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </select>
        </label>
        <input type="submit" className="button" value="Submit" />
      </form>
    </div>
  );
};

export default FormView;