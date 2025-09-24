const fs = require("fs");
const csv = require("csvtojson");
const path = require("path");

csv()
  .fromFile("/home/shartokyo/websites/datathon/backend/data/violations_with_period.csv")
  .then((rows) => {
    const geojson = {
      type: "FeatureCollection",
      features: rows
        .filter((r) => r["Violation Latitude"] && r["Violation Longitude"])
        .map((r) => ({
          type: "Feature",
          properties: {
            last_occurrence: r["Last Occurrence"],
            violation_type: r["Violation Type"],
          },
          geometry: {
            type: "Point",
            coordinates: [
              parseFloat(r["Violation Longitude"]),
              parseFloat(r["Violation Latitude"]),
            ],
          },
        })),
    };

    // Save into frontend/public so React can fetch it
    fs.writeFileSync(
      path.join(__dirname, "../violations.geojson"),
      JSON.stringify(geojson)
    );

    console.log("✅ Wrote violations.geojson with", geojson.features.length, "features");
  });