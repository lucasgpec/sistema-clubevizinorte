import { useEffect, useState } from "react";
import axios from "axios";

export default function ImportLog() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchLogs() {
      setLoading(true);
      setError("");
      try {
        // Ajuste a URL conforme seu backend
        const res = await axios.get("http://localhost:8000/api/import-logs/", {
          headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
        });
        setLogs(res.data.results || res.data);
      } catch (err) {
        setError("Erro ao carregar logs de importação");
      } finally {
        setLoading(false);
      }
    }
    fetchLogs();
  }, []);

  if (loading) return <div>Carregando logs de importação...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="bg-white rounded shadow p-6 max-w-2xl mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Logs de Importação</h2>
      <table className="min-w-full text-xs">
        <thead>
          <tr>
            <th className="border p-1">Data</th>
            <th className="border p-1">Usuário</th>
            <th className="border p-1">Registros</th>
            <th className="border p-1">Sucessos</th>
            <th className="border p-1">Erros</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, i) => (
            <tr key={i}>
              <td className="border p-1">{log.data}</td>
              <td className="border p-1">{log.usuario}</td>
              <td className="border p-1">{log.total}</td>
              <td className="border p-1 text-green-600">{log.sucessos}</td>
              <td className="border p-1 text-red-600">{log.erros}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
