import React from 'react'
import { useNavigate } from 'react-router-dom';
import './register.css';

export default function Register() {
    const navigate = useNavigate();

    // Handle registration form submission and redirect to login page upon successful registration.
    async function handleRegister (e) {
        const form = document.getElementById("registration-form");
        let API_URL =  "https://nnyi01lnx6.execute-api.us-east-1.amazonaws.com/staging/register";

        e.preventDefault();
        const email = document.getElementById('email').value;
        const username = document.getElementById('user_name').value;
        const password = document.getElementById('password').value;

        // Make a POST request to the API Gateway endpoint to register a new user.
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    user_name: username,
                    password: password
                })
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                // Rediredt to login page upon successful page
                navigate('/login');

            } else {
                // Email already exists
                alert("Email already exists. Please try again.");
            }
        } catch (error) {
            console.error('Error:', error);
            alert("Registration failed. Please try again.");
        }
    }
  
    // Render registration form.
    return (
    <div>
        <h1>Registration Form</h1>
        <form id="registration-form" onSubmit={handleRegister}>
            <label for="user_name">Username:</label>
            <input type="text" id="user_name" name="user_name"></input>

            <label for="email">Email Address:</label>
            <input type="email" id="email" name="email"></input>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password"></input>

            <input type="submit" value="Register"></input>
            <input type="submit" value="Return to login"
                onClick={() => navigate('/login')}
            >

            </input>
        
        </form>
    </div>
  )
}