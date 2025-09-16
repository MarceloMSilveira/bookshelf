import React from 'react';

import '../stylesheets/Book.css';

const starArray = [5, 4, 3, 2, 1];

const Book = ({ title, author, id, rating, deleteBook, changeRating }) => {
  return (
    <div className="book">
      <div className="cover">
        <div className="title">{title}</div>
      </div>
      <div className="author">{author}</div>
      <div className="rating">
        {starArray.map(num => (
          <div
            key={num}
            onClick={() => changeRating(id, num)}
            className={`star ${rating >= num ? 'active' : ''}`}
          />
        ))}
        <div className="delete" onClick={() => deleteBook(id)} />
      </div>
    </div>
  );
};

export default Book;