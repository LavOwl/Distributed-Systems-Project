import { TextArea } from "../common/TextArea";
import { TextInput } from "../common/TextInput";
import { useState } from 'react';
import { apiService } from "../../services/api";

export function ObservationButton({project_id} : {project_id:number}){
    const [seeMsg, setSeeMsg] = useState<boolean>(false);
    const [message, setMessage] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        
        const formData = new FormData(e.currentTarget);
        const name = formData.get('Nombre0') as string;
        const description = formData.get('Descripción0') as string;

        try {
            await apiService.sendObservation({
                project_id: project_id,
                name: name,
                description: description
            });
            
            e.currentTarget?.reset();
            setSeeMsg(false);
        } catch (error: any) {
            if (error && typeof error === 'object' && 'message' in error) {
                setMessage(error.message);
            } else {
                setMessage('Ocurrió un error inesperado');
            }
        }
    };


    return (
        <>
            <button className="px-4 hover:bg-[#fb8500] hover:text-white cursor-pointer duration-200 h-9 border-2 border-amber-500 text-black text-sm rounded-sm" onClick={() => setSeeMsg(!seeMsg)}>Agregar Observación</button>
            {   seeMsg &&
            <div className='fixed top-0 left-0 w-full h-full'>
                <div className="fixed flex flex-col align-middle z-10 top-1/2 left-1/2 transform translate-x-[-50%] translate-y-[-50%] w-1/2 min-h-3/5 h-fit bg-white border border-gray-300 rounded-xl gap-4 py-16">
                    <h3 className='text-center text-xl font-semibold text-gray-800'>Observación</h3>
                    <form className="flex flex-col align-middle gap-4 mx-auto w-80" onSubmit={handleSubmit}>
                        <TextInput id_mod={0} label='Nombre'/>
                        <TextArea id_mod={0} label='Descripción'/>
                        {message && (
                            <div className={`text-sm p-2 roundedbg-red-100 text-red-800 border border-red-300`}>
                                {message}
                            </div>
                        )}
                        <button className="px-4 hover:bg-[#fb8500] hover:text-white cursor-pointer duration-200 h-9 border-2 border-amber-500 text-black text-sm rounded-sm">Agregar Observación</button>
                    </form>
                    
                </div>
                <button className='appearance-none fixed w-full h-full bg-black/30 z-0' onClick={() => setSeeMsg(!seeMsg)}></button>
            </div>
            }
        </>
    )
    
}