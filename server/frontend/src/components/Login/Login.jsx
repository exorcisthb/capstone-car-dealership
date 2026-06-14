import React, { useState } from 'react';

const Login = () => {
  const [form, setForm] = useState({ userName: '', password: '' });
  const [msg, setMsg] = useState('');
  const submit = async (e) => {
    e.preventDefault();
    const resp = await fetch('/djangoapp/login', {
      method: 'POST', credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    const data = await resp.json();
    setMsg(data.status ? `Welcome ${data.userName}` : 'Login failed');
  };
  return (
    <div className="auth-container">
      <h1>Login</h1>
      {msg && <div className="auth-error">{msg}</div>}
      <form className="auth-form" onSubmit={submit}>
        <input name="userName" placeholder="Username" value={form.userName} onChange={(e) => setForm({ ...form, userName: e.target.value })} required />
        <input name="password" type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        <button type="submit" className="btn-primary">Login</button>
      </form>
    </div>
  );
};

export default Login;
