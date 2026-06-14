import React, { useState } from 'react';
import { useParams } from 'react-router-dom';

const PostReview = () => {
  const { id } = useParams();
  const [form, setForm] = useState({ review: '', car_year: 2024, purchase: false });
  const [msg, setMsg] = useState('');
  const submit = async (e) => {
    e.preventDefault();
    const resp = await fetch('/djangoapp/reviews/add', {
      method: 'POST', credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dealer_id: parseInt(id, 10), ...form }),
    });
    const data = await resp.json();
    if (data.status) { setMsg(`Posted! Sentiment: ${data.sentiment}`); }
    else { setMsg('Error: ' + (data.error || '')); }
  };
  return (
    <div>
      <h1>Post a Review</h1>
      {msg && <div className="alert-banner">{msg}</div>}
      <form className="auth-form" onSubmit={submit}>
        <textarea name="review" rows="5" placeholder="Your review..." value={form.review}
          onChange={(e) => setForm({ ...form, review: e.target.value })} required />
        <input type="number" name="car_year" min="1990" max="2026" value={form.car_year}
          onChange={(e) => setForm({ ...form, car_year: parseInt(e.target.value, 10) })} />
        <label><input type="checkbox" name="purchase" checked={form.purchase}
          onChange={(e) => setForm({ ...form, purchase: e.target.checked })} /> I purchased a car</label>
        <button type="submit" className="btn-primary">Submit Review</button>
      </form>
    </div>
  );
};
export default PostReview;
