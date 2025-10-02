export function TextInput({ label,  id_mod } : { label:string, id_mod:number}){
    return (
        <>
            <label htmlFor={label+id_mod}>{label}</label>
            <input className='bg-gray-300 rounded-sm outline-none border-transparent border-2 px-2 py-[0.1rem] box-border focus:border-[#fb8500]' name={label+id_mod} id={label+id_mod} required type='text'/>
        </>
    )
}