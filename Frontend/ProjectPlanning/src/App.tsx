import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from "./components/layout/Header";
import { Footer } from "./components/layout/Footer";
import { Login } from "./components/pages/Login";
import { ProjectListDirectives } from "./components/pages/ProjectListDirectives";
import { ProjectForm } from "./components/pages/ProjectForm"
import { ProjectObservations } from "./components/pages/ProjectObservations"
import { OwnedProjectList } from "./components/pages/OwnedProjectList"
import { ProjectListLenders } from './components/pages/ProjectListLenders';
import { StatsPage } from './components/pages/StatsPage';
import { useState, useEffect } from 'react';
import { LandingPage } from './components/pages/LandingPage';

interface UserPermissions {
  permissions?: string[];
  no_permissions?: string;
}

function App() {
  const [userPermissions, setUserPermissions] = useState<UserPermissions | null>(null);

  

  useEffect(() => {
    checkPermissions();
  }, []);

  const checkPermissions = async () => {
    try {
      const response = await fetch('http://localhost:5000/bonita/v1/permissions', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      
      setUserPermissions(data);
    } catch (error) {
      console.error('Error checking permissions:', error);
      setUserPermissions({ no_permissions: 'Error checking permissions' });
    };
  }

  return (
    <>
      <Router>
        <div className="flex flex-col min-h-screen">
          <Header 
            userPermissions={userPermissions} 
            onLogout={() => {setUserPermissions({}); document.cookie = 'JSESSIONID=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'; document.cookie = 'X-Bonita-API-Token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'; window.location.href='/';}}
          />

          <main className="flex min-h-120 justify-center w-full flex-1">
            <Routes>
              <Route path="/" element={<Login redirect={() => checkPermissions()} />} />
              <Route path="/login" element={<Login redirect={() => checkPermissions()} />} />
              <Route path="/landing" element={<LandingPage/>}/>
              
              {userPermissions?.permissions?.includes("consejo_directivo") && (
                <Route path="/projects" element={<ProjectListDirectives />} />
              )}
              
              {userPermissions?.permissions?.includes("ong_originante") && (
                <>
                  <Route path="/projects/new" element={<ProjectForm />} />
                  <Route path="/projects/observations" element={<ProjectObservations />} />
                </>
              )}
              
              {userPermissions?.permissions?.includes("ong_colaborativa") && (
                <>
                  <Route path="/projects/available" element={<ProjectListLenders />} />
                  <Route path="/projects/owned" element={<OwnedProjectList />} />
                </>
              )}
              
              {userPermissions?.permissions?.includes("perfil_gerencial") && (
                <Route path="/projects/stats" element={<StatsPage/>} />
              )}
            </Routes>
          </main>

          <Footer />
        </div>
      </Router>
    </>
  )
}

export default App