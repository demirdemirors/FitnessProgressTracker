# Fitness Progress Calculator

A modern, slick desktop app to log, visualize, and analyze your workout progress. Built with Python and CustomTkinter for a beautiful, responsive experience.

---

## 🚀 Features

- **Add New Entry:**
  - Log exercise name, date, weight, and reps.
  - Fast entry form with validation.
- **View Progress:**
  - Table of all workout entries.
  - Filter by exercise or date range.
  - See max, average, and Epley 1RM stats.
- **Visualize:**
  - Plot weight and 1RM estimate over time.
  - Switch between graph types.
- **Save/Load:**
  - Auto-saves to CSV.
  - Import/export to Excel and Markdown.
- **Polished UI:**
  - Light/dark mode toggle.
  - Hover effects, status bar, and modern fonts.
  - (Optional) App icon and splash screen.

---

## 🛠️ Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/demirdemirors/FitnessProgressTracker.git
   cd FitnessProgressTracker
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or install manually:
   ```bash
   pip install customtkinter pandas matplotlib openpyxl
   ```
3. **(Optional, macOS users):**
   If you see a blank window, use Anaconda Python or Homebrew Python instead of the system Python.

---

## 🖥️ Usage

1. **Run the app:**
   ```bash
   python fitness_progress_calculator.py
   ```
2. **Add your workout entries:**
   - Fill in exercise, date, weight, and reps.
   - Click "Add Entry".
3. **Filter and analyze:**
   - Use the filter controls to view specific exercises or date ranges.
   - See stats and plots update instantly.
4. **Export/Import:**
   - Export your data to Excel or Markdown.
   - Import previous logs from CSV/Excel.
5. **Switch themes:**
   - Use the toggle in the top right for light/dark/system mode.


---

## ⚙️ File Structure

- `fitness_progress_calculator.py` — Main app code
- `requirements.txt` — Python dependencies
- `README.md` — This file
- `workout_data.csv` — Your saved workout data (auto-generated)

---

## 🧩 Tech Stack
- Python 3.8+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- pandas
- matplotlib
- openpyxl

---

## 🙏 Credits
- App by Demir Demirörs, 2025
- UI inspired by modern fitness and productivity apps
- Thanks to the open-source Python community!

---

## 📝 License
MIT License. See LICENSE file for details. 