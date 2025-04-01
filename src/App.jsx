import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/NavBar";
import Home from "./page/Home";
import RecipeDetails from "./page/RecipeDetails";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/recipe/:name" element={<RecipeDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
