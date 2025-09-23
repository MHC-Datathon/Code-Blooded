import React, { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";

export default function NYCMap() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (mapRef.current) return; // initialize once

    mapRef.current = new maplibregl.Map({
      container: mapContainer.current!,
      style: "https://api.maptiler.com/maps/winter-v2/style.json?key=kMAXKYXvnrmw9q7gqZW7",
      center: [-74.006, 40.7128], // NYC
      zoom: 11,
    });
  }, []);

  return <div ref={mapContainer} className="w-full h-screen" />;
}