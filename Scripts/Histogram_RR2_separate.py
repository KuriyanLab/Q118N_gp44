import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.ticker import AutoMinorLocator

# Set global font to Arial
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Separate input files for WT and D86H
WT_FILE = 'RR2_WT_rep.xlsx'
D86H_FILE = 'RR2_D86H_rep.xlsx'

# Sheet name in each file
SHEET_NAME = 'Sheet1'

# Replicate Columns (same column names in both files)
REPLICATE_COLS = ['Enc_1', 'Enc_2', 'Enc_3', 'Enc_4', 'Enc_5']

# Column 8 (1-indexed) has the color for Active/Inactive
COLOR_COLUMN_INDEX = 8

# Histogram & Axis Settings
NUM_BINS = 50
X_AXIS_MIN = -3
X_AXIS_MAX = 3
MAX_ROW_STD = 0.8

# ==========================================
# 2. MAIN PROCESSING FUNCTION
# ==========================================
def plot_histogram(df_data, experiment_name, cols):
    print(f"Processing experiment: {experiment_name}...")
    
    # --- Clean Data ---
    # Only keep rows that are explicitly colored Green or Red
    df_clean = df_data[df_data['Template'].isin(['Active', 'Inactive'])].copy()
    df_clean = df_clean.dropna(subset=cols)
    
    # Calculate Standard Deviation across the replicate columns
    df_clean['row_std'] = df_clean[cols].std(axis=1)
    
    # Filter out rows that exceed our max Standard Deviation cutoff
    df_clean = df_clean[df_clean['row_std'] <= MAX_ROW_STD]

    # --- Data Restructuring (Melting) ---
    # Flatten the columns into a single column of values for the histogram
    df_melted = df_clean.melt(
        id_vars=['row_std', 'Template'], 
        value_vars=cols,
        var_name='Replicate',
        value_name='value'
    )
    
    df_active = df_melted[df_melted['Template'] == 'Active']
    df_inactive = df_melted[df_melted['Template'] == 'Inactive']

    print(f"{experiment_name} Active data points: {len(df_active)}")
    print(f"{experiment_name} Inactive data points: {len(df_inactive)}")

    if df_active.empty and df_inactive.empty:
        print(f"No valid data found after filtering for {experiment_name}. Skipping plot.")
        return

    # ==========================================
    # 3. PLOTTING
    # ==========================================
    fig, (ax_active, ax_inactive) = plt.subplots(2, 1, figsize=(10, 10), sharey=True)

    bins = np.linspace(X_AXIS_MIN, X_AXIS_MAX, NUM_BINS)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    
    # Colormap settings for bar gradient across X-axis
    cmap = plt.get_cmap('bwr')
    norm = mcolors.TwoSlopeNorm(vmin=X_AXIS_MIN, vcenter=0, vmax=X_AXIS_MAX)

    # ---------- TOP PLOT: ACTIVE ----------
    counts_active, _, patches_active = ax_active.hist(df_active['value'], bins=bins, edgecolor='black', linewidth=1.0)
    
    for patch, x in zip(patches_active, bin_centers):
        if patch.get_height() > 0:
            color = cmap(norm(x))
            patch.set_facecolor(color)
    
    ax_active.set_xlim(X_AXIS_MIN, X_AXIS_MAX)
    
    ax_active.set_xlabel('Individual Replicate Enrichment Value', fontsize=25)
    ax_active.set_ylabel('Frequency', fontsize=25, color='black')
    ax_active.tick_params(axis='both', labelsize=19, colors='black')
    ax_active.tick_params(axis='both', which='minor', length=4)
    ax_active.xaxis.set_minor_locator(AutoMinorLocator())
    ax_active.yaxis.set_minor_locator(AutoMinorLocator())
    ax_active.grid(axis='y', linestyle='--', alpha=0.4)
    
    # Active Aesthetics
    ax_active.axvline(x=0, color='black', linestyle=':', linewidth=2)

    # Right Y-Axis for Active
    df_active = df_active.copy()
    df_active['bin'] = pd.cut(df_active['value'], bins=bins, include_lowest=True)
    bin_avg_std_active = df_active.groupby('bin', observed=False)['row_std'].mean().values

    ax_active_tw = ax_active.twinx()
    ax_active_tw.plot(bin_centers, bin_avg_std_active, color='black', marker='o', markersize=4, 
             linestyle='None', label='Avg Row SD')
    ax_active_tw.set_ylabel('Average Row Standard Deviation', fontsize=25, color='black')
    ax_active_tw.set_ylim(0, 1)
    ax_active_tw.tick_params(axis='y', labelsize=19)
    ax_active_tw.tick_params(axis='y', which='minor', length=4)
    ax_active_tw.yaxis.set_minor_locator(AutoMinorLocator())


    # ---------- BOTTOM PLOT: INACTIVE ----------
    counts_inactive, _, patches_inactive = ax_inactive.hist(df_inactive['value'], bins=bins, edgecolor='black', linewidth=1.0)
    
    for patch, x in zip(patches_inactive, bin_centers):
        if patch.get_height() > 0:
            color = cmap(norm(x))
            patch.set_facecolor(color)
    
    ax_inactive.set_xlim(X_AXIS_MIN, X_AXIS_MAX)
    
    # Fix the y-axis limit for both subplots
    ax_active.set_ylim(0, 500)
    
    ax_inactive.set_xlabel('Individual Replicate Enrichment Value', fontsize=25)
    ax_inactive.set_ylabel('Frequency', fontsize=25, color='black')
    ax_inactive.tick_params(axis='both', labelsize=19, colors='black')
    ax_inactive.tick_params(axis='both', which='minor', length=4)
    ax_inactive.xaxis.set_minor_locator(AutoMinorLocator())
    ax_inactive.yaxis.set_minor_locator(AutoMinorLocator())
    ax_inactive.grid(axis='y', linestyle='--', alpha=0.4)
    
    # Inactive Aesthetics
    ax_inactive.axvline(x=0, color='black', linestyle=':', linewidth=2)

    # Right Y-Axis for Inactive
    df_inactive = df_inactive.copy()
    df_inactive['bin'] = pd.cut(df_inactive['value'], bins=bins, include_lowest=True)
    bin_avg_std_inactive = df_inactive.groupby('bin', observed=False)['row_std'].mean().values

    ax_inactive_tw = ax_inactive.twinx()
    ax_inactive_tw.plot(bin_centers, bin_avg_std_inactive, color='black', marker='o', markersize=4, 
             linestyle='None', label='Avg Row SD')
    ax_inactive_tw.set_ylabel('Average Row Standard Deviation', fontsize=25, color='black')
    ax_inactive_tw.set_ylim(0, 1)
    ax_inactive_tw.tick_params(axis='y', labelsize=19)
    ax_inactive_tw.tick_params(axis='y', which='minor', length=4)
    ax_inactive_tw.yaxis.set_minor_locator(AutoMinorLocator())

    plt.suptitle(f'156-167 {experiment_name}: Active vs. Inactive Templates', fontsize=23)
    plt.tight_layout()
    fig.subplots_adjust(hspace=0.15)
    
    output_filename = f'Histogram_gradient_{experiment_name}.png'
    plt.savefig(output_filename, dpi=300)
    print(f"Plot successfully saved to {output_filename}\n")
    
    # Close the figure to free memory
    plt.close()

# ==========================================
# 3. HELPER: LOAD AND TAG DATA
# ==========================================
def load_and_tag(file_name, sheet_name):
    """Load an Excel file, read cell colors to tag Active/Inactive."""
    print(f"\nLoading file: '{file_name}', sheet: '{sheet_name}'...")
    df = pd.read_excel(file_name, sheet_name=sheet_name)
    df.columns = df.columns.str.strip()
    
    # Load workbook to read cell colors
    wb = openpyxl.load_workbook(file_name, data_only=True)
    ws = wb[sheet_name]

    df['Template'] = 'Unknown'
    
    # Determine Active/Inactive based on color
    for i, row in df.iterrows():
        excel_row = i + 2  # Excel rows are 1-indexed and row 1 is the header
        fill = ws.cell(row=excel_row, column=COLOR_COLUMN_INDEX).fill
        color = fill.start_color.index if fill and fill.start_color else None
        
        # Supported Green colors for Active
        if color in [9, 'FF4EA72E', 'FF00B050']: 
            df.at[i, 'Template'] = 'Active'
        # Supported Red colors for Inactive
        elif color in [5, 'FFBE5014', 'FFFF0000']: 
            df.at[i, 'Template'] = 'Inactive'
    
    wb.close()
    return df

# ==========================================
# 4. EXECUTION
# ==========================================
if __name__ == "__main__":
    # Process WT file
    df_wt = load_and_tag(WT_FILE, SHEET_NAME)
    plot_histogram(df_wt, 'RR2WT', REPLICATE_COLS)
    
    # Process D86H file
    df_d86h = load_and_tag(D86H_FILE, SHEET_NAME)
    plot_histogram(df_d86h, 'D86H', REPLICATE_COLS)
