import { useState, type FormEvent } from "react";
import { ProjectTask } from "../forms/ProjectTask";
import { RemoveButton } from "../common/RemoveButton";
import { AppendButton } from "../common/AppendButton";
import { TextArea } from "../common/TextArea";

type ApiResponse = {
  id?: string;
  error?: string;
};

export function ProjectForm(){
    const [tasks, setTasks] = useState<{ id: number }[]>([]);
    const [warning, setWarning] = useState<{type:'SUCCESS' | 'FAILURE', message:string} | null>(null);

    const handleAppend = () => {
        setTasks([...tasks, { id: Date.now() }]);
    };

    const handleRemove = (id: number) => {
        setTasks(tasks.filter((task) => task.id !== id));
    };

    const formatDateForValidator = (dateString: string): string => {
    if (!dateString) return new Date().toISOString();
    
    const dateWithTime = new Date(dateString + 'T00:00:00');
    return dateWithTime.toISOString();
  };

    const initiateFlaskBonita = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);

        const processName = formData.get("projectName") as string;
        const desc = formData.get("Descripción0") as string;

        var projectTasks = tasks.map((task) => ({
        name: formData.get(`Nombre de Tarea${task.id}`) as string,
        start_date: formatDateForValidator(formData.get(`Fecha de Inicio${task.id}`) as string),
        description: '',
        end_date: formatDateForValidator(formData.get(`Fecha de Fin${task.id}`) as string),
        coverage_request: formData.get(`Categoría${task.id}`) as string,
        requires_contribution: !!formData.get(`Requiere contribución:${task.id}`)
        }));

        projectTasks.push({
        name: formData.get(`Nombre de Tarea0`) as string,
        start_date: formatDateForValidator(formData.get(`Fecha de Inicio0`) as string),
        description: '',
        end_date: formatDateForValidator(formData.get(`Fecha de Fin0`) as string),
        coverage_request: formData.get(`Categoría0`) as string,
        requires_contribution: !!formData.get(`Requiere contribución:0`),
        })


        const payload = {
        name: processName,
        description: desc,
        stages: projectTasks,
        };
        try {
        const response = await fetch(
            `http://localhost:5000/project/v1/create_project`,
            {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            body: JSON.stringify(payload),
            }
        );

        const data: ApiResponse = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Error en la petición");
        }
        setWarning({type:'SUCCESS', message:'Proyecto creado exitosamente!'});
        } catch (err: any) {
        setWarning({type:'FAILURE', message: err.message || 'Ocurrió un error al crear el proyecto.'});
        }
    };
  

  return (<>
        {warning && <div>
          <div className='fixed top-0 left-0 w-full h-full bg-black/20 z-10'></div>
          <div className={`border fixed top-1/2 left-1/2 transform -translate-1/2 z-20 rounded-md p-4 mb-4 ${
            warning.type === 'SUCCESS' 
              ? 'bg-green-50 border-green-200' 
              : 'bg-red-50 border-red-200'
          }`}>
            <div className="flex">
              <div className="flex-shrink-0">
                {warning.type === 'SUCCESS' ? (
                  <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                )}
              </div>
              <div className="ml-3">
                <h3 className={`text-sm font-medium ${
                  warning.type === 'SUCCESS' ? 'text-green-800' : 'text-red-800'
                }`}>
                  {warning.type === 'SUCCESS' ? 'Operación exitosa.' : 'Ha ocurrido un error confirmando la contribución.'}
                </h3>
                <div className={`mt-2 text-sm ${
                  warning.type === 'SUCCESS' ? 'text-green-700' : 'text-red-700'
                }`}>
                  <p>{warning.message}</p>
                </div>
                <div className="mt-4">
                  <button
                    type="button"
                    onClick={() => setWarning(null)}
                    className={`px-3 py-2 rounded text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                      warning.type === 'SUCCESS' 
                        ? 'bg-green-100 text-green-800 hover:bg-green-200 focus:ring-green-500' 
                        : 'bg-red-100 text-red-800 hover:bg-red-200 focus:ring-red-500'
                    }`}
                  >
                    Aceptar
                  </button>
                </div>
              </div>
            </div>
          </div>
          </div>
        }
      
        <form onSubmit={initiateFlaskBonita} className="flex flex-col w-4/5 py-4 px-4 rounded-2xl gap-2 h-fit">
          <h1 className='text-3xl'>Presentar Proyecto</h1>
          <hr/>
            <div className='flex flex-col text-nowrap'>
              <label className='text-xl' htmlFor='Nombre Proyecto'>Título</label>
              <input name='projectName' className='bg-black/10 rounded-sm w-80 outline-none text-sm border-transparent border-2 px-2 py-[0.5rem] box-border focus:border-[#fb8500] mb-4' id='Nombre Proyecto' required type='text'/>
              <TextArea label='Descripción' id_mod={1}/>
            </div>
            <h2 className='text-xl '>Tareas Adjuntas</h2>
            <div className='flex gap-4 flex-wrap'>
              <ProjectTask taskNumber={0} />
              {tasks.map((task) => (
                <ProjectTask key={task.id} taskNumber={task.id}>
                  <RemoveButton onClick={() => handleRemove(task.id)} />
                </ProjectTask>
              ))}
              <AppendButton onClick={handleAppend} />
            </div>
          <div className='w-full flex justify-end'>
            <button className='transition-all duration-500 cursor-pointer rounded-md w-fit px-6 py-2 border-2 border-black/10 text-black/50 hover:border-[#fb8500] hover:text-[#fb8500]'>Enviar</button>
          </div>
        </form>
      </>
  );
}