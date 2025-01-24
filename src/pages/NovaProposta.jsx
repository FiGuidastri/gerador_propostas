import React, { useState } from "react";
import axios from "axios";

function NovaProposta() {
  const [cliente, setCliente] = useState("");
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");
  const [preco, setPreco] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    const proposta = {
      cliente,
      titulo,
      descricao,
      preco: parseFloat(preco),
    };

    // Enviar os dados para o backend
    axios.post("http://localhost:5000/cadastro", proposta)
      .then((response) => {
        alert("Proposta criada com sucesso!");
      })
      .catch((error) => {
        console.error("Erro ao criar proposta:", error);
      });
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Criar Nova Proposta</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold">Cliente</label>
          <input
            type="text"
            className="w-full p-2 border rounded"
            value={cliente}
            onChange={(e) => setCliente(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-semibold">Título</label>
          <input
            type="text"
            className="w-full p-2 border rounded"
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-semibold">Descrição</label>
          <textarea
            className="w-full p-2 border rounded"
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm font-semibold">Preço</label>
          <input
            type="number"
            className="w-full p-2 border rounded"
            value={preco}
            onChange={(e) => setPreco(e.target.value)}
          />
        </div>
        <button
          type="submit"
          className="w-full p-3 bg-blue-500 text-white rounded mt-4"
        >
          Criar Proposta
        </button>
      </form>
    </div>
  );
}

export default NovaProposta;
