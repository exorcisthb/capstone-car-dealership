// React entry point
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import Home from './components/Home/Home';
import About from './components/About/About';
import Contact from './components/Contact/Contact';
import Register from './components/Register/Register';
import Login from './components/Login/Login';
import Dealers from './components/Dealers/Dealers';
import DealerDetail from './components/DealerDetail/DealerDetail';
import PostReview from './components/PostReview/PostReview';

function NavLink({ to, label }) {
  const loc = useLocation();
  const active = loc.pathname === to;
  return <Link to={to} className={active ? 'active' : ''}>{label}</Link>;
}

function App() {
  return (
    <BrowserRouter>
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/" className="nav-logo">CarDealership Reviews</Link>
          <ul className="nav-links">
            <li><NavLink to="/" label="Home" /></li>
            <li><NavLink to="/about" label="About Us" /></li>
            <li><NavLink to="/contact" label="Contact Us" /></li>
            <li><NavLink to="/dealers" label="Dealers" /></li>
            <li><NavLink to="/register" label="Sign Up" /></li>
            <li><NavLink to="/login" label="Login" /></li>
          </ul>
        </div>
      </nav>
      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dealers" element={<Dealers />} />
          <Route path="/dealer/:id" element={<DealerDetail />} />
          <Route path="/dealer/:id/postreview" element={<PostReview />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
