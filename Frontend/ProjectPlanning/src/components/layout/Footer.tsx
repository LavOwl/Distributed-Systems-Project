export function Footer(){
    return (
        <>
        <footer className="bg-gray-800 mt-30 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <h1 className='relative text-3xl scale-80 font-light mb-2 italic'>
                    Proj<span className='absolute top-4 transform scale-x-200 rotate-180 left-1'>🠀</span>
                    <span className='relative top-2 right-1 font-normal'>
                      Planning<span className='relative right-[2.6rem] bottom-[1.1rem] text-pink-400 text-[0.5rem]'>❤︎</span>
                    </span>
                  </h1>
              </div>
              <p className="text-gray-400 text-sm">
                Conectando ONGs para un mundo mejor.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Plataforma</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition">Características</a></li>
                <li><a href="#" className="hover:text-white transition">Precios</a></li>
                <li><a href="#" className="hover:text-white transition">Casos de Éxito</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Recursos</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition">Blog</a></li>
                <li><a href="#" className="hover:text-white transition">Guías</a></li>
                <li><a href="#" className="hover:text-white transition">Soporte</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition">Privacidad</a></li>
                <li><a href="#" className="hover:text-white transition">Términos</a></li>
                <li><a href="#" className="hover:text-white transition">Cookies</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-700 mt-8 pt-8 h-2 text-center text-sm text-gray-400">
            <p>&copy; 2025 Project Planning. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
        </>
    )
}