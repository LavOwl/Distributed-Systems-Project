import { useState, useRef, useEffect } from "react";

interface DropDownInputProps {
  texts: string[];
  label: string;
  mod_id: number;
}

function DropDownInput({ texts, label, mod_id }: DropDownInputProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState<string | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleSelect = (value: string) => {
    setSelected(value);
    setIsOpen(false);
  };

  return (
    <div className="relative w-full text-center" ref={dropdownRef}>
      <input type="hidden" name={label+mod_id} value={selected || ""} required />

      <div
        className="h-16 flex items-center justify-center w-full cursor-pointer hover:bg-black/20 select-none"
        onClick={() => setIsOpen(!isOpen)}
      >
        {selected || "Categoría"}
        <span
          className={`border-r-1 border-t-1 p-1 rotate-45 ml-2 transition-transform ${
            isOpen ? "rotate-135" : ""
          }`}
        ></span>
      </div>

      {isOpen && (
        <ul className="absolute left-0 bg-black/10 backdrop-blur-xl top-16 w-full m-auto flex flex-col z-50">
          {texts.map((value, index) => (
            <li
              key={index}
              className="flex items-center hover:bg-black/20 justify-center h-16 w-full cursor-pointer"
              onClick={() => handleSelect(value)}
            >
              {value}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default DropDownInput;