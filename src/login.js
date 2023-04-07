import React from 'react'
import { useNavigate } from 'react-router-dom';
import './login.css';

export default function Login() {
    const navigate = useNavigate();

    // Handle login form submission and redirect to home page upon successful login.
    async function handleLogin (e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        let API_URL =  "https://nnyi01lnx6.execute-api.us-east-1.amazonaws.com/staging/";

        try {
            const response = await fetch(API_URL+"login", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            if (response.ok) {
                const data = await response.json();
                console.log("Status: ", data);

                // Rediredt to home page upon successful page
                navigate('/home', { state: { email } });

            } else {
                // Display message to user regarding incorrect login details
                alert("Incorrect login details. Please try again.");
            }
        } catch (error) {
            // Handle network error
            console.error('Error logging in:', error);
        }
    }

    // Render login form.
    return (
        <div>
            <div class="container">
                <form class="login-form" id="login-form" onSubmit={handleLogin}>
                    <input type="text" id="email" placeholder="Email" required></input>
                    <input type="password" id="password" placeholder="Password" required></input>
                    <button type="submit" id="login-btn">Login</button>
                    <a><button type="button" id="register-btn"
                        onClick={() => navigate('/register')}
                    >
                        Register</button></a>
                </form>
            </div>
        </div>
    )
}