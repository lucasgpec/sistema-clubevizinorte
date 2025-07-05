import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import LoginForm from "../auth/LoginForm";
import Dashboard from "../features/Dashboard";
// Importe outros módulos conforme forem criados

export default function AppRoutes() {
  const { user } = useAuth();
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginForm />} />
        <Route
          path="/"
          element={user ? <Dashboard /> : <Navigate to="/login" replace />}
        />
        {/* Outras rotas protegidas e públicas */}
      </Routes>
    </BrowserRouter>
  );
}
