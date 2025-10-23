import type { ReactNode } from "react";
import {useState} from "react"
import { TextInput } from "../common/TextInput";
import { DateInput } from "../common/DateInput";
import DropDownInput from "../common/Dropdown";
import { CircleCheckbox } from "../common/CircleCheckbox";

export function ProjectTask({ children, taskNumber } : { children?:ReactNode, taskNumber:number }){
    const [requiresContribution, setRequiresContribution] = useState(false);
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    
    return (
        <>
            {startDate && endDate && (startDate > endDate ? setEndDate(startDate) : '')}
            <div className="flex h-75 flex-col w-50 border rounded-md relative box-border px-4 gap-1 py-8">
                <TextInput label='Nombre de Tarea' id_mod={taskNumber}/>
                <DateInput label='Fecha de Inicio' id_mod={taskNumber} onChange={(e) => setStartDate(e.target.value)}/>
                <DateInput label='Fecha de Fin' id_mod={taskNumber} {...((startDate && endDate) ? { value: (startDate > endDate) ? startDate : endDate} : {})} min={startDate || Date.now.toString()}  onChange={(e) => setEndDate(e.target.value)}/>
                <CircleCheckbox label='Requiere contribución:' id_mod={taskNumber} onChange={(e) => setRequiresContribution(e.target.checked)}/>
                {requiresContribution && (<DropDownInput texts={['Dinero', 'Materiales', 'Mano de obra']} label={'Categoría'} mod_id={taskNumber}/>)}
                {children}
            </div>
        </>
    )
}