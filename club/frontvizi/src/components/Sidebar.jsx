import { Link, useLocation } from "react-router-dom";

const menu = [
  { label: "Dashboard", path: "/" },
  { label: "Sócios", path: "/socios" },
  { label: "Dependentes", path: "/dependentes" },
  { label: "Locações", path: "/locacoes" },
  { label: "Financeiro", path: "/financeiro" },
  { label: "Escolas", path: "/escolas" },
  { label: "Importação", path: "/importacao" },
  { label: "Relatórios", path: "/relatorios" },
];

export default function Sidebar() {
  const { pathname } = useLocation();
  return (
    <aside className="w-64 bg-blue-900 text-white min-h-screen flex flex-col">
      <div className="p-6 font-bold text-2xl border-b border-blue-800">Clube Vizinorte</div>
      <nav className="flex-1 p-4">
        {menu.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`block py-2 px-3 rounded mb-1 hover:bg-blue-800 transition-colors ${
              pathname === item.path ? "bg-blue-800" : ""
            }`}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
