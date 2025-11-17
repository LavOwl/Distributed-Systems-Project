import { TextInput } from "../common/TextInput";
import { useState } from "react";
import { useNavigate } from 'react-router-dom';

export function Login({redirect}:{redirect:()=>void}) {
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);
    const navigate = useNavigate();
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setIsLoading(true);
        setMessage(null);

        const formData = new FormData(event.currentTarget);
        const username = formData.get('Usuario0') as string;
        const password = formData.get('Contraseña0') as string;

        try {
            const response = await fetch('http://localhost:5000/bonita/v1/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
                credentials: 'include'
            });

            const data = await response.json();

            if (response.ok) {
                redirect()
                navigate('/landing')
            } else {
                setMessage({ text: data.error, type: 'error' });
            }
        } catch (error) {
            setMessage({ text: 'Error de conexión con el servidor', type: 'error' });
            console.error('Login error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <> 
            <form 
                className="flex flex-col mt-18 w-1/5 min-w-60 h-70 p-8 pt-2 border-2 rounded-xl border-gray-300 shadow-xl justify-between"
                onSubmit={handleSubmit}
            >
                <div className='flex flex-col gap-3'>
                    <h2 className='text-center text-lg'>Iniciar Sesión</h2>
                    <TextInput label='Usuario' id_mod={0}/>
                    <TextInput type='password' label='Contraseña' id_mod={0}/>
                    
                    {message && (
                        <div className={`text-sm p-2 rounded ${
                            message.type === 'success' 
                                ? 'bg-green-100 text-green-800 border border-green-300' 
                                : 'bg-red-100 text-red-800 border border-red-300'
                        }`}>
                            {message.text}
                        </div>
                    )}
                </div>
                
                <button 
                    type="submit"
                    disabled={isLoading}
                    className={`w-full hover:bg-[#fb8500] cursor-pointer duration-200 h-9 bg-amber-500 text-white text-sm rounded-sm ${
                        isLoading ? 'opacity-50 cursor-not-allowed' : ''
                    }`}
                >
                    {isLoading ? 'Ingresando...' : 'Ingresar'}
                </button>
            </form>
        </>
    );
}