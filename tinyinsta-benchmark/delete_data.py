from google.cloud import datastore

def delete_entities_by_kind(client, kind):
    """Supprime toutes les entités d'un type donné."""
    print(f"## Suppression des entités {kind}")
    
    # Récupérer les clés uniquement pour une suppression plus efficace
    query = client.query(kind=kind)
    query.keys_only()
    
    keys = [entity.key for entity in query.fetch()]
    
    print(f"Trouve {len(keys)} entités {kind} a supprimer.")
    
    if not keys:
        print(f"Aucune entité {kind} trouvee. \n")
        return 0
    
    # Supprimer par lots
    batch_size = 500 
    deleted_count = 0
    
    print(f"Suppression de {len(keys)} entités {kind}...")
    
    for i in range(0, len(keys), batch_size):
        batch_keys = keys[i:i + batch_size]
        
        # client.delete_multi peut prendre une liste de clés
        client.delete_multi(batch_keys)
        
        deleted_count += len(batch_keys)
        print(f"   {deleted_count}/{len(keys)} {kind} supprimes...")
        
    print(f"Tous les {deleted_count} {kind} ont ete supprimes. \n")
    return deleted_count

def clean_data_selected(kinds_to_clean):
    """
    Nettoie les donnees de Datastore pour les types d'entites specifiés.
    :param kinds_to_clean: Liste des types d'entites (kinds) a supprimer.
    """
    if not kinds_to_clean:
        print("Aucun type d'entite selectionne pour le nettoyage.")
        return

    client = datastore.Client()
    total_deleted = 0
    
    print(f"Debut du nettoyage des donnees pour: {', '.join(kinds_to_clean)}")
    print("-" * 40)

    for kind in kinds_to_clean:
        try:
            total_deleted += delete_entities_by_kind(client, kind)
        except Exception as e:
            print(f"Erreur lors de la suppression du kind '{kind}': {e}")
            
    print("-" * 40)
    print("Nettoyage termine !")
    print(f"Total global: {total_deleted} entités supprimees.")

if __name__ == "__main__":
    
    ALL_KINDS = ['User', 'Post', 'Follow']
    
    print("--- Outil de Nettoyage Google Datastore ---")
    print("Selectionnez les types d'entites a supprimer (entrez les nombres separes par des virgules, ou 'tout'):")
    
    for i, kind in enumerate(ALL_KINDS):
        print(f"  {i+1}. {kind}")
        
    print(f"  {len(ALL_KINDS)+1}. Tout")

    choice_input = input("Votre choix (ex: 1,3 ou tout): ").strip().lower()

    kinds_to_process = []
    
    if choice_input in ['tout', 'all']:
        kinds_to_process = ALL_KINDS
    else:
        try:
            # Convertir les choix en indices, puis trouver le kind correspondant
            choices = [int(c.strip()) for c in choice_input.split(',') if c.strip()]
            
            for choice in choices:
                # Si l'utilisateur choisit 'Tout' par son numéro
                if choice == len(ALL_KINDS) + 1:
                    kinds_to_process = ALL_KINDS
                    break
                elif 1 <= choice <= len(ALL_KINDS):
                    kinds_to_process.append(ALL_KINDS[choice - 1])
                else:
                    print(f"Avertissement: Le choix {choice} n'est pas valide et sera ignore.")

            # Supprimer les doublons
            kinds_to_process = list(set(kinds_to_process))

        except ValueError:
            print("Entree invalide. Veuillez entrer des nombres separes par des virgules ou 'tout'.")

    if not kinds_to_process:
        print("Aucun type d'entite selectionne. Operation annulee.")
    else:
        print(f"\nVous avez selectionne la suppression des types: {', '.join(kinds_to_process)}")
        
        confirm = input("Etes-vous sur de vouloir supprimer ces donnees? (oui/NON): ")
        if confirm.lower() in ['oui', 'o', 'yes', 'y']:
            clean_data_selected(kinds_to_process)
        else:
            print("Operation annulee")
