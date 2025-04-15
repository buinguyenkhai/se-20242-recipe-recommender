import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import logo from "../assets/image.png"; 

const Navbar = () => {
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (search.trim()) {
      navigate(`/?search=${search.trim()}`);
    }
  };

  return (
    <nav className="bg-gradient-to-br from-blue-500 to-violet-700 p-4 shadow-lg">
      <div className="container mx-auto flex items-center justify-between">
        
        {/* Logo & Title */}
        <Link to="/" className="flex items-center space-x-3">
          <img src={logo} alt="Logo" className="h-12 rounded-full border-2 border-white" />
          <span className="text-xl font-bold text-white">Let Me Cook!</span>
        </Link>

        {/* Navigation Links */}
        <ul className="flex space-x-6 text-lg text-white">
          <li><Link to="/" className="hover:text-yellow-400">Home</Link></li>
          <li><Link to="/categories" className="hover:text-yellow-400">Categories</Link></li>
          <li><Link to="/about" className="hover:text-yellow-400">About</Link></li>
        </ul>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="flex">
          <input
            type="text"
            placeholder="Search recipes..."
            className="w-full px-4 py-2 rounded-l-lg text-white"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button type="submit" className="bg-yellow-400 px-4 py-2 rounded-r-lg text-black font-bold">
            🔍
          </button>
        </form>

      </div>
    </nav>
  );
};

export default Navbar;
