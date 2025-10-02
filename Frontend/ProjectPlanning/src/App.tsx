import { useState, type FormEvent } from "react";
import { Header } from "./components/layout/Header";
import { Footer } from "./components/layout/Footer";
import { ProjectTask } from "./components/forms/ProjectTask";
import { RemoveButton } from "./components/common/RemoveButton";
import { AppendButton } from "./components/common/AppendButton";

type ApiResponse = {
  id?: string;
  error?: string;
};


function App() {
  const [tasks, setTasks] = useState<{ id: number }[]>([]);
  const [result, setResult] = useState<ApiResponse | null>(null);

  const handleAppend = () => {
    setTasks([...tasks, { id: Date.now() }]);
  };

  const handleRemove = (id: number) => {
    setTasks(tasks.filter((task) => task.id !== id));
  };

    const initiateFlaskBonita = async (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      const formData = new FormData(e.currentTarget);

      const processName = formData.get("projectName") as string;

      var projectTasks = tasks.map((task) => ({
        name: formData.get(`Nombre de Tarea${task.id}`) as string,
        startDate: formData.get(`Fecha de Inicio${task.id}`) as string,
        endDate: formData.get(`Fecha de Fin${task.id}`) as string,
        category: formData.get(`Categoría${task.id}`) as string,
      }));

      projectTasks.push({
        name: formData.get(`Nombre de Tarea0`) as string,
        startDate: formData.get(`Fecha de Inicio0`) as string,
        endDate: formData.get(`Fecha de Fin0`) as string,
        category: formData.get(`Categoría0`) as string,
      })

      const payload = {
        title: processName,
        tasks: projectTasks,
      };

      try {
        const response = await fetch(
          `http://127.0.0.1:5000/APIbonita/v1/iniciar_proyecto`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          }
        );

        const data: ApiResponse = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Error en la petición");
        }

        setResult({ id: data.id });
      } catch (err: any) {
        setResult({ error: err.message });
      }
    };
  

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex justify-center w-full flex-1">
        <form onSubmit={initiateFlaskBonita} className="flex flex-col w-4/5 py-4 px-4 rounded-2xl gap-6 h-fit">
          <h1 className='text-3xl'>Presentar Proyecto</h1>
          <hr/>
            <div className='flex flex-col text-nowrap'>
              <label className='text-xl' htmlFor='Nombre Proyecto'>Título</label>
              <input name='projectName' className='bg-black/10 rounded-sm w-80 outline-none text-sm border-transparent border-2 px-2 py-[0.5rem] box-border focus:border-[#fb8500]' id='Nombre Proyecto' required type='text'/>
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
      </main>

      <Footer />
    </div>
  );
}

export default App