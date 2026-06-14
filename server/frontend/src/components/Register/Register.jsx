import React, { useState } from 'react';

const Register = () => {
  const [form, setForm] = useState({
    userName: '',
    firstName: '',
    lastName: '',
    email: '',
    password: '',
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const resp = await fetch('/djangoapp/register', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await resp.json();
      if (data.status) {
        setMessage('Registration successful! Welcome ' + data.userName);
      } else {
        setMessage('Error: ' + (data.error || 'unknown'));
      }
    } catch (err) {
      setMessage('Network error: ' + err.message);
    }
  };

  return (
    <div className="auth-container">
      <h1>Sign Up</h1>
      {message && <div className="auth-error">{message}</div>}
      <form className="auth-form" onSubmit={handleSubmit}>
        <input
          name="userName"
          placeholder="Username"
          value={form.userName}
          onChange={handleChange}
          required
        />
        <input
          name="firstName"
          placeholder="First Name"
          value={form.firstName}
          onChange={handleChange}
          required
        />
        <input
          name="lastName"
          placeholder="Last Name"
          value={form.lastName}
          onChange={handleChange}
          required
        />
        <input
          name="email"
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />
        <button type="submit" className="btn-primary">Register</button>
      </form>
    </div>
  );
};

export default Register;
