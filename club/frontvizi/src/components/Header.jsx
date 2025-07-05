import { useAuth } from "../auth/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();
  return (
    <header className="bg-white shadow flex items-center justify-between px-6 py-3 border-b">
      <div className="flex items-center gap-2">
        {/* Substitua pelo logo real do clube se disponível */}
        <span className="font-bold text-blue-900 text-xl">Clube Vizinorte</span>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-gray-700">{user?.username || user?.email}</span>
        <button
          onClick={logout}
          className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
        >
          Sair
        </button>
      </div>
    </header>
  );
}
