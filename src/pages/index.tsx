import NYCMap from "@/components/map";
import { Slider } from "@/components/ui/slider";
import { useState } from "react";
import { TypeSelect } from "@/components/ui/typeSelect";
import { Switch } from "@/components/ui/switch";

import { Jost } from 'next/font/google';

const font1 = Jost(
  { 
   subsets: ['latin'],
   weight: ['400','500', '600', '700'] 
  }
);

let months = ["June 2024", "July 2024", "August 2024", "September 2024", "October 2024", "November 2024", "December 2024", "January 2025", "February 2025", "March 2025", "April 2025", "May 2025", "June 2025", "July 2025", "August 2025"]
let monthYear = ["06/2024", "07/2024", "08/2024", "09/2024", "10/2024", "11/2024", "12/2024", "01/2025", "02/2025", "03/2025", "04/2025", "05/2025", "06/2025", "07/2025", "08/2025"]

export default function Home() {

  const [value, setValue] = useState([0])
  const [analysis, setAnalysis] = useState(false)

  const [type, setType] = useState("MOBILE BUS LANE")
  const [overlay, setOverlay] = useState(false)

  return (
    <div className="relative w-full ">
      <NYCMap type={type} monthYear={monthYear[value[0]]} overlay={overlay}/>
      
      <div className="absolute bottom-26 left-4 w-45 bg-black h-12 text-white rounded-full flex justify-center items-center">
        <TypeSelect value={type} onChange={setType} />
      </div>

      <div className="absolute bottom-12 left-4 w-70 gap-x-3 h-12 bg-black text-white rounded-full flex justify-center items-center">
        <span className={`${font1.className}`}>Congestion pricing overlay</span> 
        <Switch  
        checked={overlay}
        onCheckedChange={(checked) => setOverlay(checked)}/>
      </div>
      
      <div className="absolute top-4 right-4 ">
        <button onClick={() => setAnalysis(!analysis)} className="bg-black text-white text-xl rounded-full w-32 h-12 cursor-pointer">
          <span className={`${font1.className} text-lg`}>Analysis ↓</span>
        </button>
      </div>
      
      {
          analysis && (
            <div className="absolute top-16 right-4 text-lg w-50 h-50 bg-black text-white">
              info heredfdsf dsjf dsjhnf dsjnf jukdsnhfju dsj fsjufdshnjm fndsjmf hndsjmf hn
            </div>
          )
        }

      <div className="absolute bottom-30 text-center left-1/2 -translate-x-1/2 bg-black w-55 h-12 flex items-center justify-center rounded-full">
        <span className={`${font1.className} text-2xl text-white font-medium`}>
          {months[value[0]]}
        </span>
      </div>
      <div className="absolute bottom-10 left-1/2 h-10 -translate-x-1/2 -translate-y-1/2 w-1/3 bg-black text-white text-3xl px-4 py-2 rounded-full flex items-center ">
        
        <Slider
        value={value}
        onValueChange={setValue} // receives a number[] even for single thumb
        max={14}
        step={1}
        className="w-full" />
      </div>
    </div>
  );
}
