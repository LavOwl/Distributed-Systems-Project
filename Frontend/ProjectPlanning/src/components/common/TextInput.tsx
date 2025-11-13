export function TextInput({ label,  id_mod, type } : { label:string, id_mod:number, type?:string}){
    return (
        <>
            <input placeholder={label} {...(type ? { type: type }: {type:'text'})} className='bg-black/10 rounded-sm outline-none text-sm border-transparent border-2 px-2 py-[0.5rem] box-border focus:border-[#fb8500]' name={label+id_mod} id={label+id_mod} required/>
        </>
    )
}