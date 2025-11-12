export function ProjectList(){

    fetch("http://localhost:5000/v1/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "demo", password: "demo" }),
        credentials: "include"
    })
    .then(res => res.json())
    .then(data => console.log(data.message))
    .catch(console.error);

    return (
        <>
            <div className='w-3/5'>
                <h2 className='text-xl'>Proyectos</h2>
                <div className='w-full border-1 rounded-xl p-4'>
                    <div className='w-full bg-black/10 h-40 rounded-lg'>
                        <h3>Hola</h3>
                    </div>
                </div>
            </div>

        </>
    )
}