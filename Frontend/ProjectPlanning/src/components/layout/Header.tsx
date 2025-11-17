import { useState, useEffect } from 'react';

interface UserPermissions {
  permissions?: string[];
  no_permissions?: string;
}

interface HeaderProps {
  userPermissions: UserPermissions | null;
  onLogout: () => void;
}

export function Header({ userPermissions, onLogout }: HeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const hasPermission = (permission: string) => {
    return userPermissions?.permissions?.includes(permission);
  };

  const getMenuItems = () => {
    const items = [];

    if (hasPermission("consejo_directivo")) {
      items.push({ path: "/projects", label: "Proyectos a Observar" });
    }

    if (hasPermission("ong_originante")) {
      items.push(
        { path: "/projects/new", label: "Nuevo Proyecto" },
        { path: "/projects/observations", label: "Observaciones" }
      );
    }

    if (hasPermission("ong_colaborativa")) {
      items.push(
        { path: "/projects/available", label: "Proyectos a Contribuir" },
        { path: "/projects/owned", label: "Mis Contribuciones" }
      );
    }

    if (hasPermission("perfil_gerencial")) {
      items.push({ path: "/projects/stats", label: "Estadísticas" });
    }

    return items;
  };

  const menuItems = getMenuItems();

  return (
    <header className='w-full h-16 bg-black/10 mb-6 flex items-center justify-between px-4'>
      <div className="flex items-center">
        <p className='relative text-3xl font-light mb-2 italic'>
          Proj<span className='absolute top-4 transform scale-x-200 rotate-180 left-1'>🠀</span>
          <span className='relative top-2 right-1 font-normal'>
            Planning<span className='relative right-[2.6rem] bottom-[1.1rem] text-pink-400 text-[0.5rem]'>❤︎</span>
          </span>
        </p>
      </div>

      <div className="flex items-center space-x-4">
        
        {(userPermissions != null) && (userPermissions?.permissions ? (
          <>
            <nav className="hidden md:flex space-x-4">
              {menuItems.map((item) => (
                <a
                  key={item.path}
                  href={item.path}
                  className="px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md transition duration-200"
                >
                  {item.label}
                </a>
              ))}
            </nav>

            <div className="md:hidden relative">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="p-2 rounded-md text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-amber-500"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>

              {isMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                  {menuItems.map((item) => (
                    <a
                      key={item.path}
                      href={item.path}
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      {item.label}
                    </a>
                  ))}
                  <button
                    onClick={() => {
                      onLogout();
                      setIsMenuOpen(false);
                    }}
                    className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                  >
                    Cerrar Sesión
                  </button>
                </div>
              )}
            </div>


            <button
              onClick={onLogout}
              className="hidden md:block px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-md transition duration-200"
            >
              Cerrar Sesión
            </button>
          </>
        ) : (

          <a
            href="/login"
            className="px-4 py-2 text-sm font-medium text-white bg-amber-500 hover:bg-amber-600 rounded-md transition duration-200"
          >
            Iniciar Sesión
          </a>
        ))}
      </div>
    </header>
  );
}