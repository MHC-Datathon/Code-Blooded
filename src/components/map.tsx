import React, { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";

export default function NYCMap() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (mapRef.current) return; // initialize once

    const map = new maplibregl.Map({
      container: mapContainer.current!,
      style: "https://api.maptiler.com/maps/winter-v2/style.json?key=kMAXKYXvnrmw9q7gqZW7",
      center: [-74.006, 40.7128], // NYC
      zoom: 11,
    });

    mapRef.current = map;

    map.on("load", () => {
      // 1. Add your GeoJSON source
      map.addSource("violations", {
        type: "geojson",
        data: "/violations.geojson", // file in public/ folder
        tolerance: 1, // simplify geometry for lower zooms
      });

      // 2. Add a heatmap layer
      map.addLayer({
        id: "violations-heat",
        type: "heatmap",
        source: "violations",
        minzoom: 5,   // show from zoom 0
        maxzoom: 22,  // show up to max zoom
        paint: {
          "heatmap-weight": 0.01,
          "heatmap-intensity": [
            "interpolate", ["linear"], ["zoom"],
            0, 0.5,
            15, 2
          ],
          "heatmap-radius": [
            "interpolate", ["linear"], ["zoom"],
            0, 1,
            9, 10,
            15, 20
          ],
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
      });
    });
  }, []);

  return <div ref={mapContainer} className="w-full h-screen" />;
}