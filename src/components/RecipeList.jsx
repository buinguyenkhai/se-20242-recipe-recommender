import { Link } from "react-router-dom";

const recipes = [
  { name: "Spaghetti Bolognese" },
  { name: "Chicken Curry" }
];

const RecipeList = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white p-10">
      <h1 className="text-4xl font-extrabold text-center mb-8 text-blue-400">
        🍽️ Cooking Recipes
      </h1>
      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {recipes.map((recipe, index) => (
          <li key={index} className="bg-gray-800 p-6 rounded-2xl shadow-lg hover:scale-105 transition-transform">
            <Link
              to={`/recipe/${recipe.name.toLowerCase().replace(/\s+/g, "-")}`}
              className="text-xl font-semibold text-blue-300 hover:text-blue-500"
            >
              {recipe.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RecipeList;
