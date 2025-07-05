import { useEffect, useState } from "react";
import axios from "axios";

export default function DependentesList() {
  const [dependentes, setDependentes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchDependentes() {
      setLoading(true);
      setError("");
      try {
        // Ajuste a URL conforme seu backend
        const res = await axios.get("http://localhost:8000/api/dependentes/");
        setDependentes(res.data.results || res.data);
      } catch (err) {
        setError("Erro ao carregar dependentes");
      } finally {
        setLoading(false);
      }
    }
    fetchDependentes();
  }, []);

  if (loading) return <div>Carregando dependentes...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Dependentes</h2>
      <table className="min-w-full bg-white rounded shadow">
        <thead>
          <tr>
            <th className="p-2 border">Nome</th>
            <th className="p-2 border">Sócio Titular</th>
            <th className="p-2 border">Parentesco</th>
            <th className="p-2 border">Data Nasc.</th>
            <th className="p-2 border">Ensino Sup.</th>
            <th className="p-2 border">PcD</th>
          </tr>
        </thead>
        <tbody>
          {dependentes.map((dep) => (
            <tr key={dep.id}>
              <td className="p-2 border">{dep.nome_completo}</td>
              <td className="p-2 border">{dep.socio_titular?.cliente?.nome_completo}</td>
              <td className="p-2 border">{dep.parentesco}</td>
              <td className="p-2 border">{dep.data_nascimento}</td>
              <td className="p-2 border text-center">{dep.cursando_ensino_superior ? "Sim" : "Não"}</td>
              <td className="p-2 border text-center">{dep.pcd ? "Sim" : "Não"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
