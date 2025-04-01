import { Link } from "react-router-dom";

const recipes = [
  {
    name: "Spaghetti Bolognese",
    description: "A classic Italian pasta dish with a rich, meaty sauce.",
  },
  {
    name: "Chicken Curry",
    description: "A flavorful dish made with tender chicken and aromatic spices.",
  },
];

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-300 to-yellow-300 text-white p-10">
      <h1 className="text-4xl font-bold font-sans text-center mb-6 text-white-300">Recipes</h1>
      <div className="max-w-3xl mx-auto space-y-4">
        {recipes.map((recipe) => (
          <Link
            key={recipe.name}
            to={`/recipe/${recipe.name.replace(/\s+/g, "-").toLowerCase()}`}
            className="block bg-gradient-to-br from-blue-700 to-violet-700 p-4 rounded-lg hover:from-blue-900 hover:to-violet-900 transition"
          >
            <h2 className="text-2xl font-semibold text-black-400">{recipe.name}</h2>
            <p className="text-gray-300">{recipe.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Home;
