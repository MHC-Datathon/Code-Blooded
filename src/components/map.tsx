import React, { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";

type props = {
  type: string // you can extend this to other types if needed
  monthYear: string
  overlay: boolean
};

export default function NYCMap({ type, monthYear, overlay }: props) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);

  const [start, setStart] = useState(0)

  // Initialize map once
  useEffect(() => {
    if (mapRef.current) return;

    const map = new maplibregl.Map({
      container: mapContainer.current!,
      style: "https://api.maptiler.com/maps/winter-v2/style.json?key=kMAXKYXvnrmw9q7gqZW7",
      center: [-74.006, 40.7128],
      zoom: 11,
      attributionControl: false,
      logoPosition: "bottom-right"
    });

    mapRef.current = map;

    map.on("load", () => {
      map.addSource("violations", {
          type: "geojson",
          data: "https://mhc-datathon.github.io/Code-Blooded/violations.geojson",
          generateId: true,
        });

      // Add a polygon overlay (example: a rectangle over part of NYC)
      map.addSource("overlay-area", {
        type: "geojson",
        data: {
          type: "FeatureCollection",
          features: [
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Polygon",
                coordinates: [
                  [
                    [-73.99371276716278, 40.77354631044223],   // Battery Park (southwest tip)
                    [-73.95815743495902, 40.758879659177346],   // Battery Park (southeast tip near Brooklyn Bridge)
                    [-73.97182631519334, 40.72958050239625],   // East River near Midtown Tunnel
                    [-73.97740530964424, 40.710943277946356],   // East River near 60th St
                    [-74.01392948725831, 40.700507864852696],   // Upper West Side near 60th St
                    [-74.01871454801953, 40.70812883403552],   // Hudson River near 60th St
                    [-74.01042115813762, 40.75105673272185]    // back to Battery Park
                  ]
                ]
              }
            }
          ]
        }
      });

      map.addLayer({
        id: "overlay-area-layer",
        type: "fill",
        source: "overlay-area",
        layout: {
          visibility: "none" // <-- start invisible
        },
        paint: {
          "fill-color": "#ff0000", // red
          "fill-opacity": 0.3       // semi-transparent
        }
      });

    const source = map.getSource("violations") as maplibregl.GeoJSONSource;

    // Preprocess features to add monthYear property
    
    fetch("/violations.geojson")
      .then(res => res.json())
      .then((data: GeoJSON.FeatureCollection) => {
        data.features.forEach(f => {
          if (!f.properties) return

          const dateStr = f.properties.last_occurrence; // e.g., "08/11/2025 06:01:09 PM"
          const [month, , year] = dateStr.split("/");    // ["08", "11", "2025 06:01:09 PM"]
          const yearOnly = year.split(" ")[0];           // "2025"
          f.properties.monthYear = `${month}/${yearOnly}`; // "08/2025"
        });
        source.setData(data);

        setStart(1)
        
      });


      // Single heatmap layer that we filter dynamically
      map.addLayer({
        id: "violations-heatmap",
        type: "heatmap",
        source: "violations",
        minzoom: 5,
        maxzoom: 22,
        paint: {
          "heatmap-weight": 0.01,
          "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 0, 0.5, 15, 2],
          "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 0, 1, 9, 10, 15, 20],
          "heatmap-opacity": 0.6,
          "heatmap-color": [
            "interpolate",
            ["linear"],
            ["heatmap-density"],
            0, "rgba(33,102,172,0)",
            0.2, "royalblue",
            0.4, "cyan",
            0.6, "lime",
            0.8, "yellow",
            1, "red"
          ],
        },
        layout: {
          visibility: "visible",
        },
        filter: ["==", "type", type], // <-- filter by "type" property in GeoJSON
      });
    });
  }, []);

  // Update filter whenever `type` changes
  useEffect(() => {

    const map = mapRef.current;
    if (!map || !map.isStyleLoaded()) return;

    console.log(monthYear)

    map.setFilter("violations-heatmap", [
      "all",
      ["==", "violation_type", type],
      ["==", "monthYear", monthYear] // monthYear = "08/2025"
    ]);

    console.log(overlay)

    map.setLayoutProperty(
      "overlay-area-layer",
      "visibility",
      overlay ? "visible" : "none"
    );
  }, [start, type, monthYear, overlay]);

  return <div ref={mapContainer} className="w-full h-screen" />;
}