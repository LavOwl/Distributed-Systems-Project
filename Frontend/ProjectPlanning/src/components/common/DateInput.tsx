export function DateInput({ label,  id_mod } : { label:string, id_mod:number}){
    return (
        <>
            <label className='text-sm' htmlFor={label+id_mod}>{label}</label>
            <input name={label+id_mod} id={label+id_mod} className='bg-[#fb8500] p-2 font-["Work Sans"] rounded-sm text-sm' required type='date'/>
        </>
    )
}