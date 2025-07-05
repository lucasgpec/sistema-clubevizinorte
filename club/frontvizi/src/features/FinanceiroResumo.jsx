import { useEffect, useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function FinanceiroResumo() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchResumo() {
      setLoading(true);
      setError("");
      try {
        // Ajuste a URL conforme seu backend
        const res = await axios.get("http://localhost:8000/api/financeiro/resumo/", {
          headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
        });
        setData(res.data);
      } catch (err) {
        setError("Erro ao carregar resumo financeiro");
      } finally {
        setLoading(false);
      }
    }
    fetchResumo();
  }, []);

  if (loading) return <div>Carregando resumo financeiro...</div>;
  if (error) return <div className="text-red-500">{error}</div>;
  if (!data) return null;

  const chartData = {
    labels: data.meses,
    datasets: [
      {
        label: "Receitas",
        data: data.receitas,
        backgroundColor: "#2563eb",
      },
      {
        label: "Inadimplência",
        data: data.inadimplencia,
        backgroundColor: "#dc2626",
      },
    ],
  };

  return (
    <div className="bg-white rounded shadow p-6 max-w-2xl mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Resumo Financeiro</h2>
      <Bar data={chartData} />
    </div>
  );
}
