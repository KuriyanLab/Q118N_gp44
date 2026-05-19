import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 24, 'font.family': 'sans-serif', 'font.sans-serif': ['Arial']})

codon_table = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
}

def translate_dna(seq):
    if not isinstance(seq, str): return ""
    protein = ""
    for i in range(0, len(seq), 3):
        codon = seq[i:i+3]
        if len(codon) == 3:
            protein += codon_table.get(codon, 'X')
    return protein

# Read the excel file
df = pd.read_excel('156167_RR2.xlsx', sheet_name='156167_RR2')

TARGET_SEQ = "QFGKADQSDKIN"
RESIDUE_NUMBERS = list(range(156, 168))

def extract_region(seq):
    # The DNA sequences in this file have a 13-AA prefix before the target region in frame 1.
    if not isinstance(seq, str) or len(seq) < 100:
        return None
    
    # Translate starting from index 1 (frame 1)
    prot = translate_dna(seq[1:])
    
    # The target region is at amino acids 13 to 24 (0-indexed 13:25)
    region = prot[13:25]
    if len(region) < len(TARGET_SEQ):
        return None
    return region

df['Region_156_167'] = df['Sequence'].apply(extract_region)

# Custom order for Y-axis requested by the user. '_' represents 'Stop' from the translation.
custom_order = ['K','R','E','D','N','Q','H','T','S','C','A','V','L','I','M','F','Y','W','G','P','_']

def calculate_frequencies(sequence_series):
    seq_list = [list(seq) for seq in sequence_series if seq and len(seq) == len(TARGET_SEQ)]
    if not seq_list:
        return pd.DataFrame()
        
    df_seqs = pd.DataFrame(seq_list)
    freq_df = pd.DataFrame(index=custom_order)
    
    for col in df_seqs.columns:
        counts = df_seqs[col].value_counts(normalize=True)
        freq_df[col] = counts
        
    freq_df = freq_df.fillna(0)
    
    # Rename '_' to 'Stop'
    freq_df.index = freq_df.index.map(lambda x: 'Stop' if x == '_' else x)
    
    return freq_df

def plot_combined_heatmaps(data1, title1, colormap1, data2, title2, colormap2, filename):
    if data1.empty and data2.empty:
        print("No data to plot")
        return
        
    num_rows = max(len(data1) if not data1.empty else 0, len(data2) if not data2.empty else 0)
    fig_height = max(6, num_rows * 0.5 + 4)
    # Wide figure to accommodate both heatmaps side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(28, fig_height))
        
    x_labels = [f"{num}\n{aa}" for num, aa in zip(RESIDUE_NUMBERS, TARGET_SEQ)]
    
    if not data1.empty:
        data_pct1 = data1 * 100
        annot_data1 = data_pct1.map(lambda x: f"{int(round(x))}" if x > 0 else "")
        sns.heatmap(data_pct1, cmap=colormap1, annot=annot_data1, fmt="", 
                    cbar_kws={'label': 'Percentage'}, linewidths=1.5, linecolor='black', ax=ax1)
        ax1.set_title(title1, fontsize=32, pad=20)
        ax1.set_xlabel('Residue Position (WT Amino Acid)', fontsize=28, labelpad=15)
        ax1.set_ylabel('Mutated Amino Acid', fontsize=28, labelpad=15)
        ax1.set_xticks(np.arange(len(x_labels)) + 0.5)
        ax1.set_xticklabels(x_labels, rotation=0, fontsize=24)
        ax1.tick_params(axis='y', rotation=0, labelsize=24)
        
        cbar = ax1.collections[0].colorbar
        cbar.ax.tick_params(labelsize=20)
        cbar.set_label('Percentage', size=28)
    else:
        ax1.set_visible(False)
    
    if not data2.empty:
        data_pct2 = data2 * 100
        annot_data2 = data_pct2.map(lambda x: f"{int(round(x))}" if x > 0 else "")
        sns.heatmap(data_pct2, cmap=colormap2, annot=annot_data2, fmt="", 
                    cbar_kws={'label': 'Percentage'}, linewidths=1.5, linecolor='black', ax=ax2)
        ax2.set_title(title2, fontsize=32, pad=20)
        ax2.set_xlabel('Residue Position (WT Amino Acid)', fontsize=28, labelpad=15)
        ax2.set_ylabel('Mutated Amino Acid', fontsize=28, labelpad=15)
        ax2.set_xticks(np.arange(len(x_labels)) + 0.5)
        ax2.set_xticklabels(x_labels, rotation=0, fontsize=24)
        ax2.tick_params(axis='y', rotation=0, labelsize=24)
        
        cbar = ax2.collections[0].colorbar
        cbar.ax.tick_params(labelsize=20)
        cbar.set_label('Percentage', size=28)
    else:
        ax2.set_visible(False)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Saved {filename}")

if 'Average' in df.columns and 'Average.1' in df.columns:
    better_rr2wt = df[df['Average'] > 0.1]
    worse_rr2wt = df[df['Average'] < -0.1]
    
    better_d86h = df[df['Average.1'] > 0.1]
    worse_d86h = df[df['Average.1'] < -0.1]
    
    freq_better_rr2wt = calculate_frequencies(better_rr2wt['Region_156_167'])
    freq_worse_rr2wt = calculate_frequencies(worse_rr2wt['Region_156_167'])
    
    freq_better_d86h = calculate_frequencies(better_d86h['Region_156_167'])
    freq_worse_d86h = calculate_frequencies(worse_d86h['Region_156_167'])
    
    # Plot RR2WT
    if not freq_better_rr2wt.empty and not freq_worse_rr2wt.empty:
        combined_mask_rr2wt = (freq_better_rr2wt != 0).any(axis=1) | (freq_worse_rr2wt != 0).any(axis=1)
        freq_better_rr2wt = freq_better_rr2wt.loc[combined_mask_rr2wt]
        freq_worse_rr2wt = freq_worse_rr2wt.loc[combined_mask_rr2wt]
        
    plot_combined_heatmaps(
        freq_better_rr2wt, "RR2WT: Better than WT (>0.3)", "Reds",
        freq_worse_rr2wt, "RR2WT: Worse than WT (< -0.3)", "Blues",
        "RR2WT_Better_and_Worse_156_167_frequency.png"
    )
    print("Generated single combined figure RR2WT_Better_and_Worse_156_167_frequency.png.")
    
    # Plot D86H
    if not freq_better_d86h.empty and not freq_worse_d86h.empty:
        combined_mask_d86h = (freq_better_d86h != 0).any(axis=1) | (freq_worse_d86h != 0).any(axis=1)
        freq_better_d86h = freq_better_d86h.loc[combined_mask_d86h]
        freq_worse_d86h = freq_worse_d86h.loc[combined_mask_d86h]
        
    plot_combined_heatmaps(
        freq_better_d86h, "D86H: Better than WT (>0.3)", "Reds",
        freq_worse_d86h, "D86H: Worse than WT (< -0.3)", "Blues",
        "D86H_Better_and_Worse_156_167_frequency.png"
    )
    print("Generated single combined figure D86H_Better_and_Worse_156_167_frequency.png.")
else:
    print("Average columns not found.")
