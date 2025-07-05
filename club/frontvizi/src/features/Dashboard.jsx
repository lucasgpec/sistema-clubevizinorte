import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import SociosList from "./SociosList";
import DependentesList from "./DependentesList";
import LocacoesList from "./LocacoesList";
import ImportacaoCSV from "./ImportacaoCSV";
import ImportLog from "./ImportLog";
import FinanceiroResumo from "./FinanceiroResumo";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 p-6">
          <h1 className="text-2xl font-bold mb-4">Dashboard Principal</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {/* Cards de resumo financeiro, sócios, locações, escolas */}
            <div className="bg-white rounded shadow p-4">Financeiro</div>
            <div className="bg-white rounded shadow p-4">Sócios</div>
            <div className="bg-white rounded shadow p-4">Locações</div>
            <div className="bg-white rounded shadow p-4">Escolas</div>
          </div>
          <SociosList />
          <div className="mt-8" />
          <DependentesList />
          <div className="mt-8" />
          <LocacoesList />
          <div className="mt-8" />
          <ImportacaoCSV onImport={(dados) => {}} />
          <div className="mt-8" />
          <ImportLog />
          <div className="mt-8" />
          <FinanceiroResumo />
        </main>
      </div>
    </div>
  );
}
