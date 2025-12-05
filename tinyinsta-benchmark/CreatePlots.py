import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- Configuration et Utilitaires ---
os.makedirs('out', exist_ok=True)
PNG_DPI = 300

def clean_time_data(time_str):
    """Convertit '1457.25ms' en secondes (1.45725 float)"""
    if isinstance(time_str, str) and time_str.endswith('ms'):
        # Convertir en float et diviser par 1000 pour passer de ms à secondes (s)
        return float(time_str.replace('ms', '')) / 1000.0
    try:
        # Tente la conversion directe si 'ms' n'est pas là, et suppose que c'est en ms si > 1 (très simpliste)
        val = float(time_str)
        return val / 1000.0 if val > 0.01 else val
    except:
        return np.nan

def setup_plot(title, xlabel):
    """Configure le style du graphique pour coller à l'exemple du projet."""
    plt.figure(figsize=(10, 6))
    
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.xlabel(xlabel)
    plt.ylabel('Temps moyen par requête (s)')
    plt.title(title)

def create_plots():
    print("--- Génération des graphiques PNG ---")
    
    # ------------------------------------------------------------------
    # Graphique 1: Concurrence (conc.png)
    # ------------------------------------------------------------------
    try:
        conc_df = pd.read_csv('out/conc.csv')
        conc_df['AVG_TIME_CLEAN'] = conc_df['AVG_TIME'].apply(clean_time_data) 
        conc_agg = conc_df.groupby('PARAM')['AVG_TIME_CLEAN'].agg(['mean', 'std']).reset_index()
        
        setup_plot(
            title='Temps moyen par requête selon la concurrence',
            xlabel='Nombre d\'utilisateurs concurrents (PARAM)'
        )
        
        plt.bar(conc_agg['PARAM'].astype(str), conc_agg['mean'], 
                yerr=conc_agg['std'], capsize=5, color='cornflowerblue', edgecolor='black', alpha=0.8) 
        
        plt.savefig('out/conc.png', dpi=PNG_DPI, bbox_inches='tight')
        plt.close()
        print("✓ Graphique conc.png généré")
    except Exception as e:
        print(f"✗ Erreur lors du traitement de conc.csv: {e}")
    
    # ------------------------------------------------------------------
    # Graphique 2: Posts (post.png)
    # ------------------------------------------------------------------
    try:
        post_df = pd.read_csv('out/post.csv')
        post_df['AVG_TIME_CLEAN'] = post_df['AVG_TIME'].apply(clean_time_data) 
        post_agg = post_df.groupby('PARAM')['AVG_TIME_CLEAN'].agg(['mean', 'std']).reset_index()
        
        setup_plot(
            title='Performance en fonction du nombre de posts par utilisateur',
            xlabel='Nombre de posts par utilisateur (PARAM)'
        )
        
        plt.bar(post_agg['PARAM'].astype(str), post_agg['mean'], 
                yerr=post_agg['std'], capsize=5, color='mediumseagreen', edgecolor='black', alpha=0.8)
        
        plt.savefig('out/post.png', dpi=PNG_DPI, bbox_inches='tight')
        plt.close()
        print("✓ Graphique post.png généré")
    except Exception as e:
        print(f"✗ Erreur lors du traitement de post.csv: {e}")
    
    # ------------------------------------------------------------------
    # Graphique 3: Followers (fanout.png)
    # ------------------------------------------------------------------
    try:
        fanout_df = pd.read_csv('out/fanout.csv')
        fanout_df['AVG_TIME_CLEAN'] = fanout_df['AVG_TIME'].apply(clean_time_data) 
        fanout_agg = fanout_df.groupby('PARAM')['AVG_TIME_CLEAN'].agg(['mean', 'std']).reset_index()
        
        setup_plot(
            title='Performance en fonction du nombre de followees par utilisateur',
            xlabel='Nombre de followees par utilisateur (PARAM)'
        )
        
        plt.bar(fanout_agg['PARAM'].astype(str), fanout_agg['mean'], 
                yerr=fanout_agg['std'], capsize=5, color='indianred', edgecolor='black', alpha=0.8)
        
        plt.savefig('out/fanout.png', dpi=PNG_DPI, bbox_inches='tight')
        plt.close()
        print("✓ Graphique fanout.png généré")
    except Exception as e:
        print(f"✗ Erreur lors du traitement de fanout.csv: {e}")

if __name__ == "__main__":
    create_plots()
