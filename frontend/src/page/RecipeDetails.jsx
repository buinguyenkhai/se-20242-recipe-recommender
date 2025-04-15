import { useParams, Link } from "react-router-dom";

const recipes = [
  {
    name: "Spaghetti Bolognese",
    description: "A classic Italian pasta dish with a rich, meaty sauce.",
    ingredients: ["Spaghetti", "Ground beef", "Tomato sauce", "Onion", "Garlic"],
    instructions: "Cook spaghetti. Prepare sauce by sautéing onion, garlic, and meat.",
  },
  {
    name: "Chicken Curry",
    description: "A flavorful dish made with tender chicken and aromatic spices.",
    ingredients: ["Chicken", "Onion", "Garlic", "Ginger", "Curry powder"],
    instructions: "Cook onions, garlic, and ginger. Add chicken and spices, then coconut milk.",
  },
  {
    name: "Caprese Salad",
    description: "Basic salad",
    ingredients: ["Tomato", "Mozzarella", "Basil"],
    instructions: "Slice tomatoes, mozzarella and fresh basils onto a platter, drizzle with salt and olive oil.",
  },
];

const RecipeDetails = () => {
  let { name } = useParams();
  const formattedName = name.replace(/-/g, " ");
  const recipe = recipes.find((r) => r.name.toLowerCase() === formattedName.toLowerCase());

  if (!recipe) {
    return <h1 className="text-black text-2xl text-center mt-10">Recipe not found</h1>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white p-10">
      <div className="max-w-2xl mx-auto bg-gray-800 p-8 rounded-xl shadow-lg">
        <h1 className="text-4xl font-bold text-blue-400">{recipe.name}</h1>
        <p className="text-lg mt-2 text-gray-300">{recipe.description}</p>
        <h2 className="text-2xl font-semibold mt-4 text-yellow-300">Ingredients:</h2>
        <ul className="list-disc ml-5 text-gray-300">
          {recipe.ingredients.map((ingredient, index) => (
            <li key={index}>{ingredient}</li>
          ))}
        </ul>
        <h2 className="text-2xl font-semibold mt-4 text-yellow-300">Instructions:</h2>
        <p className="mt-2 text-gray-300">{recipe.instructions}</p>
        <Link
          to="/"
          className="block mt-6 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg text-center"
        >
          🔙 Back to Recipes
        </Link>
      </div>
    </div>
  );
};

export default RecipeDetails;
