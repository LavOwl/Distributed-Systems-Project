import type { ChangeEvent } from 'react';

export function DateInput({ label,  id_mod, min, onChange, value } : { label:string, id_mod:number, min?:string, onChange?:(e: ChangeEvent<HTMLInputElement>)=>void, value?:string}){
    return (
        <>
                <label className='text-sm' htmlFor={label+id_mod}>{label}</label>
                <input name={label+id_mod} {...(min ? { min: min } : {})} {...(onChange ? { onChange: onChange } : {})} {...(value ? { value: value } : {})} id={label+id_mod} className='bg-black/10 calendar-black p-2 font-["Work Sans"] rounded-sm text-sm border-transparent border-2 box-border focus:border-[#fb8500] outline-transparent' required type='date'/>
        </>
    )
}