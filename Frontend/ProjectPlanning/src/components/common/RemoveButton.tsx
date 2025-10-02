export function RemoveButton({ onClick } : { onClick:()=>void }){
    return (
        <>
        <button className="absolute top-1 right-1 cursor-pointer w-6 h-6 flex items-center justify-center rounded-full bg-black/10 hover:bg-black/20" type='button' onClick={onClick}><span className='text-xl text-center font-bold text-gray-700'>×</span></button>
        </>
    )
}
