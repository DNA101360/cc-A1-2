import './navbar.css';
import { useNavigate } from 'react-router-dom';

function NavBar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Navigate to the login page
    navigate('/login');
  };

  return (
    <nav>
      <ul>
        <li><a onClick={handleLogout}>Log Out</a></li>
      </ul>
    </nav>
  );
}

export default NavBar;
