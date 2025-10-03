import type { ReactNode } from "react";
import { TextInput } from "../common/TextInput";
import { DateInput } from "../common/DateInput";
import DropDownInput from "../common/Dropdown";

export function ProjectTask({ children, taskNumber } : { children?:ReactNode, taskNumber:number }){
    return (
        <>
            <div className="flex h-75 flex-col w-50 border rounded-md relative box-border px-4 gap-1 py-8">
                <TextInput label='Nombre de Tarea' id_mod={taskNumber}/>
                <DateInput label='Fecha de Inicio' id_mod={taskNumber}/>
                <DateInput label='Fecha de Fin' id_mod={taskNumber}/>
                <DropDownInput texts={['Option 1', 'Option 2', 'Option 3']} label={'Categoría'} mod_id={taskNumber}/>
                {children}
            </div>
        </>
    )
}