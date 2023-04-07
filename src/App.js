import logo from './logo.svg';
import './App.css';
import Login from './login';
import Home from './home';
import Register from './register';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />}></Route>
          <Route path="/login" element={<Login />}></Route>
          <Route path="/home" element={<Home />}></Route>
          <Route path="/register" element={<Register/>}></Route>
        </Routes>
      </BrowserRouter>
    </div>
  ); 
}

export default App;
