export function AppendButton({ onClick } : { onClick:()=>void }){
    return (
        <>
        <button type='button' className='hover:scale-[1.02] transition-transform bg-black/40 backdrop-blur-2xl border border-white rounded-2xl relative aspect-[3/4] h-60 flex items-center justify-center cursor-pointer' onClick={onClick}><span className='relative rounded-full w-2/5 aspect-square bg-black/30 shadow-2xl before:content-[] before:absolute before:w-[60%] before:h-[15%] before:rounded-xl before:top-1/2 before:left-1/2 before:-translate-1/2 before:rotate-90 after:content-[] after:absolute after:w-[60%] after:h-[15%] after:rounded-xl after:top-1/2 after:left-1/2 after:-translate-1/2 after:bg-black/10 before:bg-[linear-gradient(to_right,rgba(0,0,0,0.1)_0%,rgba(0,0,0,0.1)_37.5%,rgba(0,0,0,0)_37.5%,rgba(0,0,0,0)_62.5%,rgba(0,0,0,0.1)_62.5%,rgba(0,0,0,0.1)_100%)]'></span></button>
        </>
    )
}