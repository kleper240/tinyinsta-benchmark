from google.cloud import datastore

def clean_all_data():
    client = datastore.Client()
    
    # Liste de tous les types d'entités à supprimer
    kinds = ['User', 'Post', 'Follow']
    
    total_deleted = 0
    
    for kind in kinds:
        print(f"Recherche des entités {kind}...")
        entities = list(client.query(kind=kind).fetch())
        
        print(f"Trouve {len(entities)} entités {kind}")
        
        if not entities:
            continue
        
        # Afficher un échantillon
        print(f"Echantillon {kind}:")
        for i, entity in enumerate(entities[:3]):
            if kind == 'User':
                print(f"   {i+1}. {entity.get('username', entity.key.name)}")
            elif kind == 'Post':
                print(f"   {i+1}. Post de {entity.get('author', 'N/A')}")
            elif kind == 'Follow':
                print(f"   {i+1}. {entity.get('follower', 'N/A')} -> {entity.get('followee', 'N/A')}")
        
        # Supprimer
        print(f"Suppression des {len(entities)} entités {kind}...")
        
        batch_size = 100
        deleted_count = 0
        
        for i in range(0, len(entities), batch_size):
            batch = entities[i:i + batch_size]
            
            with client.batch() as batch_operation:
                for entity in batch:
                    batch_operation.delete(entity.key)
            
            deleted_count += len(batch)
            print(f"   {deleted_count}/{len(entities)} {kind} supprimes")
        
        total_deleted += len(entities)
        print(f"Tous les {kind} supprimes\n")
    
    print(f"Nettoyage termine !")
    print(f"Total: {total_deleted} entités supprimees")

if __name__ == "__main__":
    confirm = input("Voulez-vous supprimer TOUTES les données (Users, Posts, Follows)? (oui/NON): ")
    if confirm.lower() in ['oui', 'o', 'yes', 'y']:
        clean_all_data()
    else:
        print("Operation annulee")
