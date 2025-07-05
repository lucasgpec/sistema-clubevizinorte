import { useEffect, useState } from "react";
import axios from "axios";

export default function SociosList() {
  const [socios, setSocios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchSocios() {
      setLoading(true);
      setError("");
      try {
        // Ajuste a URL conforme seu backend
        const res = await axios.get("http://localhost:8000/api/socios/");
        setSocios(res.data.results || res.data);
      } catch (err) {
        setError("Erro ao carregar sócios");
      } finally {
        setLoading(false);
      }
    }
    fetchSocios();
  }, []);

  if (loading) return <div>Carregando sócios...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Sócios</h2>
      <table className="min-w-full bg-white rounded shadow">
        <thead>
          <tr>
            <th className="p-2 border">Nome</th>
            <th className="p-2 border">CPF</th>
            <th className="p-2 border">Status</th>
            <th className="p-2 border">Plano</th>
          </tr>
        </thead>
        <tbody>
          {socios.map((socio) => (
            <tr key={socio.id}>
              <td className="p-2 border">{socio.cliente?.nome_completo}</td>
              <td className="p-2 border">{socio.cliente?.cpf}</td>
              <td className="p-2 border">{socio.status}</td>
              <td className="p-2 border">{socio.plano}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
