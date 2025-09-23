import NYCMap from "@/components/map";
import Slider from "@/components/slider";
import { useState } from "react";

export default function Home() {

  const [value, setValue] = useState(0)
  const [analysis, setAnalysis] = useState(false)



  return (
    <div className="relative w-full ">
      <NYCMap />
      
      
      <div className="absolute top-4 right-4 ">
        <button onClick={() => setAnalysis(!analysis)} className="bg-black text-white text-xl rounded-full w-32 h-12 cursor-pointer">
          Analysis ↓
        </button>
      </div>
      {
          analysis && (
            <div className="absolute top-16 right-4 text-lg w-50 h-50 bg-black text-white">
              info heredfdsf dsjf dsjhnf dsjnf jukdsnhfju dsj fsjufdshnjm fndsjmf hndsjmf hn
            </div>
          )
        }

      <div className="absolute bottom-45 text-2xl font-bold text-center left-1/2">
        {value}
      </div>
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 -translate-y-1/2 z-20 bg-black text-white text-3xl px-4 py-2 rounded">
        
        <input
          type="range"
          min="0"
          max="12"
          value={value}
          onChange={(e) => setValue(Number(e.target.value))}
          className="w-full accent-blue-600"
        />
        hello
      </div>
    </div>
  );
}
