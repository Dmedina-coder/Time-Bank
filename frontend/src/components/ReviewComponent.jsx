import React from 'react';
import './ReviewComponent.css';

const StarRating = ({ rating, max = 5 }) => (
  <span className="star-rating" aria-label={`${rating} de ${max} estrellas`}>
    {Array.from({ length: max }, (_, i) => (
      <span key={i} className={i < rating ? 'star filled' : 'star'}>★</span>
    ))}
  </span>
);

const ReviewComponent = ({ review }) => {
  const date = review.created_at
    ? new Date(review.created_at).toLocaleDateString('es-ES', {
        day: '2-digit', month: 'short', year: 'numeric'
      })
    : null;

  return (
    <div className="review-card">
      <div className="review-header">
        <div className="review-meta">
          <span className="review-author">{review.reviewer_name || 'Usuario'}</span>
          {date && <span className="review-date">{date}</span>}
        </div>
        <StarRating rating={review.rating} />
      </div>
      {review.comment && <p className="review-comment">{review.comment}</p>}
    </div>
  );
};

export { StarRating };
export default ReviewComponent;
