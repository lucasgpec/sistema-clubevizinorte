import { useEffect, useState } from "react";
import axios from "axios";

export default function LocacoesList() {
  const [locacoes, setLocacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchLocacoes() {
      setLoading(true);
      setError("");
      try {
        // Ajuste a URL conforme seu backend
        const res = await axios.get("http://localhost:8000/api/locacoes/");
        setLocacoes(res.data.results || res.data);
      } catch (err) {
        setError("Erro ao carregar locações");
      } finally {
        setLoading(false);
      }
    }
    fetchLocacoes();
  }, []);

  if (loading) return <div>Carregando locações...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Locações</h2>
      <table className="min-w-full bg-white rounded shadow">
        <thead>
          <tr>
            <th className="p-2 border">Espaço</th>
            <th className="p-2 border">Cliente</th>
            <th className="p-2 border">Data</th>
            <th className="p-2 border">Status</th>
          </tr>
        </thead>
        <tbody>
          {locacoes.map((loc) => (
            <tr key={loc.id}>
              <td className="p-2 border">{loc.espaco?.nome}</td>
              <td className="p-2 border">{loc.cliente?.nome_completo}</td>
              <td className="p-2 border">{loc.data_agendamento}</td>
              <td className="p-2 border">{loc.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
