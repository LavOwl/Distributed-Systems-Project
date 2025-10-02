export function TextInput({ label,  id_mod } : { label:string, id_mod:number}){
    return (
        <>
            <input placeholder={label} className='bg-black/10 rounded-sm outline-none text-sm border-transparent border-2 px-2 py-[0.5rem] box-border focus:border-[#fb8500]' name={label+id_mod} id={label+id_mod} required type='text'/>
        </>
    )
}