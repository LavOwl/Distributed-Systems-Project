import { Link } from 'react-router-dom';

export function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="flex items-center">

                  <h1 className='relative text-3xl scale-170 font-light mb-2 italic'>
                    Proj<span className='absolute top-4 transform scale-x-200 rotate-180 left-1'>🠀</span>
                    <span className='relative top-2 right-1 font-normal'>
                      Planning<span className='relative right-[2.6rem] bottom-[1.1rem] text-pink-400 text-[0.5rem]'>❤︎</span>
                    </span>
                  </h1>
              </div>
            </div>
            
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Conectando <span className="text-indigo-600">ONGs</span> para un 
              <span className="text-indigo-600"> impacto mayor</span>
            </h2>
            
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              La plataforma que transforma la manera en que las organizaciones sin fines de lucro 
              colaboran, financian proyectos y maximizan su impacto social.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/landing" 
                className="bg-indigo-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-indigo-700 transition duration-300 shadow-lg"
              >
                Comenzar Ahora
              </Link>
              <button className="border-2 border-indigo-600 text-indigo-600 px-8 py-3 rounded-lg font-medium hover:bg-indigo-50 transition duration-300">
                Conocer Más
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Transformando la Colaboración entre ONGs
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Una solución integral para gestionar proyectos, encontrar financiamiento 
              y construir alianzas estratégicas.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Financiamiento Colaborativo</h3>
              <p className="text-gray-600">
                Conecta tu proyecto con ONGs colaboradoras dispuestas a financiar iniciativas 
                alineadas con sus objetivos de impacto social.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Gestión Eficiente</h3>
              <p className="text-gray-600">
                Planifica, programa y da seguimiento a tus proyectos con herramientas 
                diseñadas específicamente para el sector social.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Comunidad Activa</h3>
              <p className="text-gray-600">
                Únete a una red de organizaciones comprometidas con el cambio social 
                y descubre oportunidades de colaboración.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Impact Stats */}
      <section className="py-16 bg-gradient-to-r from-indigo-600 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">150+</div>
              <div className="text-indigo-100">ONGs Conectadas</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">€2.5M</div>
              <div className="text-indigo-100">En Proyectos Financiados</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">89%</div>
              <div className="text-indigo-100">Tasa de Éxito</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">42</div>
              <div className="text-indigo-100">Países Alcanzados</div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              ¿Cómo Funciona?
            </h2>
            <p className="text-lg text-gray-600">
              Tres simples pasos para transformar tu impacto social
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-indigo-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">1</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Registra tu Proyecto</h3>
              <p className="text-gray-600">
                Crea un perfil detallado de tu iniciativa con objetivos, presupuesto 
                y alcance definidos.
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-indigo-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">2</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Conecta con Financiadores</h3>
              <p className="text-gray-600">
                Nuestra plataforma empareja tu proyecto con ONGs interesadas 
                en financiar iniciativas como la tuya.
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-indigo-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">3</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Ejecuta y Reporta</h3>
              <p className="text-gray-600">
                Gestiona tu proyecto con nuestras herramientas y comparte 
                el impacto generado con tus colaboradores.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-6">
            ¿Listo para Amplificar tu Impacto?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Únete a la comunidad de ONGs que están transformando la manera 
            de colaborar y generar cambio social.
          </p>
          <Link 
            to="/login" 
            className="bg-indigo-500 text-white px-8 py-4 rounded-lg font-medium hover:bg-indigo-400 transition duration-300 text-lg inline-block"
          >
            Comenzar Mi Primer Proyecto
          </Link>
          <p className="text-gray-400 mt-4 text-sm">
            Totalmente gratuito para organizaciones sin fines de lucro registradas
          </p>
        </div>
      </section>
    </div>
  );
}