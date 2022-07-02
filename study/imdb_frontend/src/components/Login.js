import Navbar from "./Navbar"
import React, { useState } from 'react';



async function LoginUser(credentials) {

    return fetch('http://localhost:8000/auth/token/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    })
        .then(data => data.json())
}

const Login = () => {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    const handleSubmit = async e => {
        e.preventDefault();
        const response = await LoginUser({
            username,
            password
        });

        if ('auth_token' in response) {
            console.log(response)
            localStorage.setItem('auth_token', response['auth_token']);
            window.location.href = '/';

        } else {
            alert('Error')
        }
    }

    return (
        <div className="Login">
            <Navbar />
            <div className="login-form">
                <form onSubmit={handleSubmit}>
                    <div className="input-container">
                        <label>Логин </label>
                        <input type="text" name="username" onChange={e => setUserName(e.target.value)} required />


                    </div>
                    <div className="input-container">
                        <label>Пароль </label>
                        <input type="password" name="password" onChange={e => setPassword(e.target.value)} required />

                    </div>
                    <div className="button-container">
                        <input type="submit" />
                    </div>
                </form>
            </div>

        </div>
    )
}

export default Login
