import { useRef, useState } from "react";
import Papa from "papaparse";
import { isValidCPF, isValidEmail, validateRequired } from "../utils/validators";
import axios from "axios";

export default function ImportacaoCSV({ onImport }) {
  const fileInput = useRef();
  const [preview, setPreview] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [validation, setValidation] = useState([]);

  const handleFile = (e) => {
    setError("");
    setPreview([]);
    const file = e.target.files[0];
    if (!file) return;
    setLoading(true);
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        const previewData = results.data.slice(0, 10);
        setPreview(previewData);
        // Validação básica
        const valids = previewData.map((row, idx) => {
          const missing = validateRequired(row, ["cpf", "email", "nome_completo"]);
          return {
            idx,
            cpf: row.cpf && !isValidCPF(row.cpf) ? "CPF inválido" : null,
            email: row.email && !isValidEmail(row.email) ? "Email inválido" : null,
            missing,
          };
        });
        setValidation(valids);
        setLoading(false);
      },
      error: (err) => {
        setError("Erro ao processar arquivo: " + err.message);
        setLoading(false);
      },
    });
  };

  const handleImport = async () => {
    if (onImport && preview.length) {
      onImport(preview);
    }
    // Exemplo de envio para API (ajuste endpoint conforme backend)
    try {
      setLoading(true);
      await axios.post("http://localhost:8000/api/importar-clientes/", preview, {
        headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
      });
      alert("Importação concluída com sucesso!");
    } catch (err) {
      setError("Erro ao importar dados para o backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded shadow p-6 max-w-lg mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Importação de Dados (CSV)</h2>
      <input
        type="file"
        accept=".csv"
        ref={fileInput}
        onChange={handleFile}
        className="mb-4"
      />
      {loading && <div>Processando arquivo...</div>}
      {error && <div className="text-red-500 mb-2">{error}</div>}
      {preview.length > 0 && (
        <>
          <div className="mb-2 font-semibold">Prévia dos dados:</div>
          <div className="overflow-x-auto mb-2">
            <table className="min-w-full text-xs">
              <thead>
                <tr>
                  {Object.keys(preview[0]).map((col) => (
                    <th key={col} className="border p-1">{col}</th>
                  ))}
                  <th className="border p-1">Validação</th>
                </tr>
              </thead>
              <tbody>
                {preview.map((row, i) => (
                  <tr key={i}>
                    {Object.values(row).map((val, j) => (
                      <td key={j} className="border p-1">{val}</td>
                    ))}
                    <td className="border p-1 text-red-600">
                      {validation[i]?.missing?.length > 0 && (
                        <div>Faltando: {validation[i].missing.join(", ")}</div>
                      )}
                      {validation[i]?.cpf && <div>{validation[i].cpf}</div>}
                      {validation[i]?.email && <div>{validation[i].email}</div>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button
            onClick={handleImport}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            disabled={validation.some(v => v.cpf || v.email || (v.missing && v.missing.length))}
          >
            Importar Dados
          </button>
        </>
      )}
    </div>
  );
}
