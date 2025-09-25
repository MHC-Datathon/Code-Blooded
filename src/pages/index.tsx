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

      <div className="absolute bottom-40 left-8 text-black rounded-full flex justify-center items-center">
        <span className={`${font1.className} text-lg font-medium`}> Violation type:</span>
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
            <div className="absolute p-5 mt-2 h-7/8 top-16 right-4 text-lg w-110 overflow-auto bg-black text-white rounded-2xl custom-scroll">
              <span className={`${font1.className}`}>
                <span className="flex justify-center text-2xl">Analysis:</span>

                When congestion pricing began in Manhattan’s CBD in January 2025, the number of automated camera enforcement (ACE) violations jumped. Monthly averages went from about 6,000 to nearly 18,000. On the surface, that looks like a big spike.

                But much of this increase came from the MTA rolling out more cameras in 2025. Routes like the M2 and M4 only started recording violations once cameras were installed, so their “increase” isn’t about worse behavior—it’s about new enforcement.

                <br />

                Bus lanes: Down over 70%—a clear sign that cameras discouraged drivers from using them.

                <br />
                Bus stops: Up 61%.

                <br />
                Double-parking: Up 52%.
                This suggests fewer lane intrusions but more problems at curbs and bus stops.

                <br />
                Route Differences:

                In CBD-only routes (M34+, M42), Violations dropped (−35.7%).

                Partial-CBD routes (M2, M4, M15+, M101) exhibited mixed results. Some increased, but their numbers are skewed because of the date at which cameras were added.

                <br />
                <span className="flex justify-center text-xl">Takeaway:</span>
                <br />

                Violation counts are higher after congestion pricing, but that’s mostly due to expanded enforcement. The real behavioral change is that drivers are avoiding bus lanes while shifting to blocking stops and curbs instead.

                <br />
                <br />
                We highly recommend reading our paper for a more in depth analysis <a className="text-blue-400 underline" href="/Code-Blooded/paper.pdf" target="_blank" rel="noopener noreferrer">Here</a>
              </span>
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
