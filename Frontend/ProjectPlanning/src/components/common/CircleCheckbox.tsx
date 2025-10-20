import type { ChangeEvent } from 'react';

export function CircleCheckbox({ label,  id_mod, onChange } : { label:string, id_mod:number, onChange:(e: ChangeEvent<HTMLInputElement>)=>void}){
    return (
        <>
            <div className='flex'>
                <label className='text-xs text-nowrap' htmlFor={label+id_mod}>{label}</label>
                <input onChange={onChange} className='appearance-none relative block shrink-0 w-4 h-4 rounded-full border checked:border-[#fb8500] border-black checked:bg-[#fb8500] after:absolute after:content-[] after:top-1/2 after:left-1/2 after:-translate-1/2 after:border-3 after:rounded-full after:border-white after:p-1 after:pointer-events-none ml-4' name={label+id_mod} id={label+id_mod} type='checkbox'/>
            </div>
        </>
    )
}