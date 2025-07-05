import { useAuth } from "./auth/AuthContext";
import LoginForm from "./auth/LoginForm";
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import AppRoutes from "./routes/AppRoutes";

function App() {
  const { user } = useAuth();
  const [count, setCount] = useState(0)

  if (!user) return <LoginForm />;
  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <header className="bg-blue-900 text-white p-4 flex items-center justify-between">
          <span className="font-bold text-xl">Clube Vizinorte</span>
          <span>Bem-vindo, {user.username || user.email}</span>
        </header>
        <main className="flex-1 p-6">
          <h1 className="text-2xl font-bold mb-4">Dashboard (em construção)</h1>
          {/* Aqui virão os dashboards, menus e módulos */}
        </main>
      </div>
      <AppRoutes />
    </>
  )
}

export default App
