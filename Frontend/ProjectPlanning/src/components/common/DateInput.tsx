export function DateInput({ label,  id_mod } : { label:string, id_mod:number}){
    return (
        <>
            <label htmlFor={label+id_mod}>{label}</label>
            <input name={label+id_mod} id={label+id_mod} required type='date'/>
        </>
    )
}