import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from "./components/layout/Header";
import { Footer } from "./components/layout/Footer";
import { Login } from "./components/pages/Login";
import { ProjectListDirectives } from "./components/pages/ProjectListDirectives";
import { ProjectForm } from "./components/pages/ProjectForm"
import { ProjectObservations } from "./components/pages/ProjectObservations"
import { OwnedProjectList } from "./components/pages/OwnedProjectList"

function App() {
  return (
    <>
      <Router>
        <div className="flex flex-col min-h-screen">
          <Header />

          <main className="flex justify-center w-full flex-1">
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/login" element={<Login />} />
                <Route path="/projects" element={<ProjectListDirectives />} />
                <Route path="/projects/new" element={<ProjectForm />} />
                <Route path="/projects/owned" element={<OwnedProjectList />} />
                <Route path="/projects/:id/observations" element={<ProjectObservations />} />
              </Routes>
          </main>

          <Footer />
        </div>
      </Router>
    </>
  )
}

export default App