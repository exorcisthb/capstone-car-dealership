import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const Dealers = () => {
  const [dealers, setDealers] = useState([]);
  const [state, setState] = useState('');
  useEffect(() => {
    const url = state ? `/djangoapp/dealers/state/${state}` : '/djangoapp/dealers';
    fetch(url, { credentials: 'include' })
      .then((r) => r.json())
      .then((d) => setDealers(d.dealers || []));
  }, [state]);
  return (
    <div>
      <h1>Dealers</h1>
      <div className="filter-section">
        <label>State:&nbsp;</label>
        <select value={state} onChange={(e) => setState(e.target.value)}>
          <option value="">All</option>
          <option value="KS">Kansas</option>
          <option value="CA">California</option>
          <option value="NY">New York</option>
          <option value="TX">Texas</option>
        </select>
      </div>
      <div className="dealers-grid">
        {dealers.map((d) => (
          <div key={d.id} className="dealer-card">
            <div className="dealer-info">
              <h3>{d.full_name}</h3>
              <p className="dealer-location">{d.city}, {d.state}</p>
              <Link to={`/dealer/${d.id}`} className="btn-primary">Review Dealer</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
export default Dealers;
