from pymatgen.core import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.ext.matproj import MPRester
import os

# Replace with your NEW Materials Project API key
MATERIALS_PROJECT_API_KEY = "H0XbrfDs0BYaDbuGHkj56BaRhGeqbz9T"  # Keep this private!

# Initialize the Materials Project API
mpr = MPRester("H0XbrfDs0BYaDbuGHkj56BaRhGeqbz9T")

# Initialize StructureMatcher
matcher = StructureMatcher()

# Your local path to CIF files
cif_folder = r"C:\Users\Leon\Downloads\UW-Madison-25\tmp_results\7.0"

# Check if folder exists
if not os.path.exists(cif_folder):
    print(f"\n❌ Error: The folder path '{cif_folder}' does not exist.")
    exit()

# List all CIF files
cif_files = [f for f in sorted(os.listdir(cif_folder)) if f.endswith(".cif")]

if not cif_files:
    print("\n❌ Error: No CIF files found in the specified folder.")
    exit()

print(f"\n📂 Found {len(cif_files)} CIF files. Processing the first 3...")

# Read and process CIF files
pymatgen_structures = {}
extracted_formulas = []

for cif_file in cif_files[:128]:  # Process first 3 files as a test
    file_path = os.path.join(cif_folder, cif_file)
    print(f"📖 Reading {cif_file}...")

    try:
        structure = Structure.from_file(file_path)
        formula = structure.composition.alphabetical_formula  # Standardized formula
        pymatgen_structures[cif_file] = structure
        extracted_formulas.append(formula)
        print(f"✅ Successfully loaded {cif_file} | Extracted Formula: {formula}")
    except Exception as e:
        print(f"❌ Error loading {cif_file}: {e}")

# Print extracted formulas before querying Materials Project
print("\n🔍 Extracted formulas for lookup:", extracted_formulas)

# Query Materials Project database for each formula INDIVIDUALLY
if extracted_formulas:
    matched_results = {}

    for formula in extracted_formulas:
        try:
            print(f"\n🔎 Searching for: {formula} in Materials Project...")
            existing_materials = mpr.get_structures(formula)

            if existing_materials:
                print(f"✅ Match found for {formula}")
                matched_results[formula] = existing_materials[0].composition.formula
            else:
                print(f"❌ No match found for {formula}")

        except Exception as e:
            print(f"\n❌ Error querying {formula}: {e}")

# Print final results
if matched_results:
    print("\n✅ Matching structures found in Materials Project:")
    for formula, matched_formula in matched_results.items():
        print(f"{formula} → {matched_formula}")
else:
    print("\n❌ No matches found in Materials Project.")
