
import os

def swap_filenames():
    folder = "."
    moves = []
    
    # Identify files to swap
    for filename in os.listdir(folder):
        if filename == "swap_filenames.py":
            continue
            
        if not os.path.isfile(os.path.join(folder, filename)):
            continue
            
        new_name = None
        # Handle the swap logic
        # Note: checking 'configurational' first. User also mentioned 'configuratinal' (typo), we handle both to be safe.
        if "configurational" in filename:
            new_name = filename.replace("configurational", "mutational")
        elif "mutational" in filename:
            new_name = filename.replace("mutational", "configurational")
        elif "configuratinal" in filename: # Handling potential typo in existing filenames
            new_name = filename.replace("configuratinal", "mutational")
            
        if new_name:
            original_path = os.path.join(folder, filename)
            temp_path = os.path.join(folder, filename + ".swaptmp")
            final_path = os.path.join(folder, new_name)
            moves.append((original_path, temp_path, final_path))
    
    if not moves:
        print("No files found matching the criteria.")
        return

    print(f"Found {len(moves)} files to rename.")

    # Phase 1: Rename to temp
    print("Phase 1: Renaming to temporary files...")
    successful_moves = []
    for orig, temp, final in moves:
        try:
            os.rename(orig, temp)
            successful_moves.append((orig, temp, final))
        except Exception as e:
            print(f"Error renaming {os.path.basename(orig)} to temp: {e}")

    # Phase 2: Rename temp to final
    print("Phase 2: Renaming to final names...")
    for orig, temp, final in successful_moves:
        try:
            os.rename(temp, final)
            print(f"Swapped: {os.path.basename(orig)} -> {os.path.basename(final)}")
        except Exception as e:
             print(f"Error renaming temp to {os.path.basename(final)}: {e}")
             # Attempt rollback if possible?
             # For now just log error.

if __name__ == "__main__":
    swap_filenames()
