# Code-Blooded · MTA Datathon 2025

This repository contains our project submission for the **MTA Datathon 2025**, where we analyzed **Automated Camera Enforcement (ACE) bus-lane violations** in relation to the launch of **congestion pricing** in Manhattan’s Central Business District (CBD).  

We built a **data analysis pipeline** (Python: pandas, numpy, matplotlib) and a **presentation website** (Next.js, TypeScript) to communicate our findings.  

---

## 🎥 Project Video Overview
Watch our project video overview below:
https://www.youtube.com/watch?v=x-W0gc3OESs

---
## Project website

https://mhc-datathon.github.io/Code-Blooded/

---

## 📊 Project Overview

**Challenge Question:**  
“Some automated camera-enforced routes travel within or cross Manhattan’s Central Business District. How have violations on these routes changed alongside the implementation of congestion pricing?”

**Key Findings:**
- **Violations increased overall:** Average monthly ACE violations rose sharply after congestion pricing began in January 2025.  
- **Camera rollout effect:** Much of this rise is explained by the **phased installation of new enforcement cameras** across routes in 2025.  
- **Shift in violation types:**  
  - Bus lane violations decreased by **71%** (showing cameras work for lanes).  
  - Bus stop violations increased by **61%**.  
  - Double-parked violations rose by **52%**.  
- **Route-level results:**  
  - CBD-only routes (M34+, M42) saw a **35.7% decrease**.  
  - Some Partial-CBD routes (M2, M4, M101, M15+) increased—but the effect is confounded by late camera installations.  

📄 Read the full draft report: [Datathon Research Paper (PDF)](./Datathon%20Research%20Paper.pdf)
🌐 Explore visuals and analysis on the deployed website.

---

## 🛠 Tech Stack

- **Frontend Website:** [Next.js](https://nextjs.org), TypeScript, Tailwind CSS  
- **Data Analysis:** Python (pandas, numpy, matplotlib)  
- **Collaboration:** GitHub (issues, commits, version control)  
- **Deployment:** [Vercel](https://vercel.com)  

---

## 🚀 Getting Started

Clone the repository:

    ```bash
    git clone https://github.com/MHC-Datathon/Code-Blooded.git
    cd Code-Blooded


## 📂 Repository Structure
```
├── backend/ # Python analysis pipeline
│ ├── cleaning.py # Cleans raw violations data
│ ├── analysis.py # Aggregates + generates figures
│ └── data/ # Input/output CSV files
│
├── frontend/ # Next.js website (presentation)
│ ├── pages/ # Website pages
│ ├── components/ # Reusable UI components
│ └── public/ # Static assets (charts, visuals)
│
├── docs/ # Draft report + supporting materials
└── README.md
```

---

## 🔄 Reproducibility

Our workflow can be replicated in two steps:

1. **Data Cleaning:**  
   ```bash
   python backend/cleaning.py

2. **Analysis & Figures**  
   ```bash
   python backend/analysis.py

## 📢 Team

Team Code-Blooded – Maruf Azad, Aabid Dewan, Farjan Halim, and Nahin Khan in the MTA Datathon 2025.
Built with ❤️ using Python, Next.js, and far too many cups of coffee ☕.

## 📜 License

This project is open-source and available under the [MIT License](./LICENSE).