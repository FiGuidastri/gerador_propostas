import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom'; // Importa o hook useParams

const Propostas = () => {
  const { usuarioId } = useParams(); // Obtém o usuarioId da URL
  const [propostas, setPropostas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Função para buscar as propostas do backend
  const fetchPropostas = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/propostas/${usuarioId}`);
      setPropostas(response.data);
    } catch (error) {
      setError('Erro ao carregar propostas');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPropostas();
  }, [usuarioId]);

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Propostas</h1>
      <ul>
        {propostas.map((proposta) => (
          <li key={proposta.id}>
            <h3>{proposta.titulo}</h3>
            <p>{proposta.descricao}</p>
            <p>Cliente: {proposta.cliente}</p>
            <p>Preço: {proposta.preco}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Propostas;
