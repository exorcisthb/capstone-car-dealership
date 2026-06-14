import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

const DealerDetail = () => {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  useEffect(() => {
    fetch(`/djangoapp/dealer/${id}`, { credentials: 'include' })
      .then((r) => r.json())
      .then((d) => setDealer(d.dealer));
    fetch(`/djangoapp/reviews/dealer/${id}`, { credentials: 'include' })
      .then((r) => r.json())
      .then((d) => setReviews(d.reviews || []));
  }, [id]);
  if (!dealer) return <p>Loading...</p>;
  return (
    <div>
      <div className="dealer-detail-header">
        <h1>{dealer.full_name}</h1>
        <p className="dealer-meta">{dealer.city}, {dealer.state}</p>
      </div>
      <h2>Reviews</h2>
      {reviews.map((r) => (
        <div key={r.id} className="review-card">
          <div className="review-header">
            <strong>{r.name}</strong>
            <span className={`sentiment sentiment-${r.sentiment}`}>{r.sentiment}</span>
          </div>
          <p>{r.review}</p>
        </div>
      ))}
      <Link to={`/dealer/${id}/postreview`} className="btn-primary">Post Review</Link>
    </div>
  );
};
export default DealerDetail;
