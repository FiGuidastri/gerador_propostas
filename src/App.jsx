// Code: App.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";

//paginas
import Home from './pages/Home';
import Propostas from './pages/Propostas';
import NovaProposta from './pages/NovaProposta';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <header className="bg-blue-500 text-white p-4">
          <nav className="container mx-auto flex justify-between">
            <h1 className="text-xl font-bold">Gerador de Propostas</h1>
            <ul className="flex gap-4">
              <li><Link to="/" className="hover:underline">Home</Link></li>
              <li><Link to="/propostas/1" className="hover:underline">Propostas</Link></li> {/* Exemplo com usuarioId=1 */}
              <li><Link to="/nova-proposta" className="hover:underline">Nova Proposta</Link></li>
            </ul>
          </nav>
        </header>
        <main className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/propostas/:usuarioId" element={<Propostas />} /> {/* Rota com parametro */}
            <Route path="/nova-proposta" element={<NovaProposta />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
