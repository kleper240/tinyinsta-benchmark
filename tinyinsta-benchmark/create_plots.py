import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def clean_time_data(time_str):
    """Convertir '1457.25ms' en 1457.25 (float)"""
    if isinstance(time_str, str) and time_str.endswith('ms'):
        return float(time_str.replace('ms', ''))
    return float(time_str)

def create_plots():
    # Configuration pour les graphiques
    plt.style.use('seaborn-v0_8')
    
    # Graphique 1: Concurrence
    try:
        conc_df = pd.read_csv('out/conc.csv')
        conc_df['AVG_TIME_CLEAN'] = conc_df['AVG_TIME'].apply(clean_time_data)
        conc_agg = conc_df.groupby('PARAM')['AVG_TIME_CLEAN'].agg(['mean', 'std']).reset_index()
        
        plt.figure(figsize=(10, 6))
        plt.bar(conc_agg['PARAM'].astype(str), conc_agg['mean'], 
                yerr=conc_agg['std'], capsize=5, color='skyblue', alpha=0.7)
        plt.xlabel('Nombre d\'utilisateurs simultanés')
        plt.ylabel('Temps moyen (ms)')
        plt.title('Performance en fonction de la concurrence')
        plt.grid(True, alpha=0.3)
        plt.savefig('out/conc.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Graphique conc.png généré")
    except Exception as e:
        print(f"✗ Erreur avec conc.csv: {e}")
    
    # Graphique 2: Posts
    try:
        post_df = pd.read_csv('out/post.csv')
        post_df['AVG_TIME_CLEAN'] = post_df['AVG_TIME'].apply(clean_time_data)
        post_agg = post_df.groupby('PARAM')['AVG_TIME_CLEAN'].agg(['mean', 'std']).reset_index()
        
        plt.figure(figsize=(10, 6))
        plt.bar(post_agg['PARAM'].astype(str), post_agg['mean'], 
                yerr=post_agg['std'], capsize=5, color='lightgreen', alpha=0.7)
        plt.xlabel('Nombre de posts par utilisateur')
        plt.ylabel('Temps moyen (ms)')
        plt.title('Performance en fonction du nombre de posts')
        plt.grid(True, alpha=0.3)
        plt.savefig('out/post.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Graphique post.png généré")
    except Exception as e:
        print(f"✗ Erreur avec post.csv: {e}")
    
    # Graphique 3: Followers
    try:
        fanout_df = pd.read_csv('out/fanout.csv')
        fanout_df['AVG_TIME_CLEAN'] = fanout_df['AVG_TIME'].apply(clean_time_data)
        fanout_agg = fanout_df.groupby('PARAM')['AVG_TIME_CLEAN'].agg(['mean', 'std']).reset_index()
        
        plt.figure(figsize=(10, 6))
        plt.bar(fanout_agg['PARAM'].astype(str), fanout_agg['mean'], 
                yerr=fanout_agg['std'], capsize=5, color='lightcoral', alpha=0.7)
        plt.xlabel('Nombre de followers par utilisateur')
        plt.ylabel('Temps moyen (ms)')
        plt.title('Performance en fonction du nombre de followers')
        plt.grid(True, alpha=0.3)
        plt.savefig('out/fanout.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Graphique fanout.png généré")
    except Exception as e:
        print(f"✗ Erreur avec fanout.csv: {e}")

if __name__ == "__main__":
    create_plots()
