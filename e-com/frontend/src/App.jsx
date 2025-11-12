import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

export default function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/products/")
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((err) => console.error("Error fetching products:", err));
  }, []);

  const scrollToProducts = () => {
    document.getElementById("products").scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="bg-gray-50 min-h-screen font-sans">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-600 to-indigo-700 text-white h-[80vh] flex flex-col items-center justify-center text-center px-6">
        <motion.h1
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="text-5xl sm:text-6xl font-bold mb-4"
        >
          Welcome to Our Store 🛍️
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.3 }}
          className="text-lg sm:text-xl mb-6 max-w-2xl"
        >
          Explore exclusive products handpicked just for you.  
          Quality, style, and affordability — all in one place.
        </motion.p>

        <motion.button
          onClick={scrollToProducts}
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="px-8 py-3 bg-white text-blue-700 font-semibold rounded-full shadow-lg hover:bg-gray-200 transition"
        >
          Shop Now →
        </motion.button>
      </section>

      {/* Products Section */}
      <section id="products" className="py-16 px-5 sm:px-10">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-4xl font-bold text-center text-gray-800 mb-10"
        >
          Featured Products
        </motion.h2>

        {loading ? (
          <div className="flex items-center justify-center h-40">
            <div className="w-12 h-12 border-4 border-gray-300 border-t-blue-600 rounded-full animate-spin"></div>
          </div>
        ) : products.length === 0 ? (
          <p className="text-center text-gray-500">No products available.</p>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 1 }}
            viewport={{ once: true }}
            className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 max-w-7xl mx-auto"
          >
            {products.map((product, index) => (
              <motion.div
                key={product.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white shadow-lg rounded-2xl overflow-hidden transform transition hover:scale-105 hover:shadow-2xl"
              >
                {product.image ? (
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-56 object-cover"
                  />
                ) : (
                  <div className="w-full h-56 bg-gray-200 flex items-center justify-center text-gray-400 text-sm">
                    No Image
                  </div>
                )}

                <div className="p-5">
                  <h3 className="text-xl font-semibold text-gray-800">
                    {product.name}
                  </h3>
                  <p className="text-gray-500 text-sm mt-1 line-clamp-2">
                    {product.description}
                  </p>

                  <div className="flex items-center justify-between mt-4">
                    <span className="text-lg font-bold text-blue-600">
                      ₹{product.price}
                    </span>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                      Add to Cart
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </section>

      {/* Footer */}
      <footer className="text-center py-6 bg-gray-100 text-gray-600 mt-10">
        © {new Date().getFullYear()} MyStore. All rights reserved.
      </footer>
    </div>
  );
}
