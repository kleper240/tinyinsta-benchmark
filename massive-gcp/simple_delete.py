from google.cloud import datastore

client = datastore.Client()

print("Recherche des utilisateurs...")
users = list(client.query(kind='User').fetch())

print(f"Trouvé {len(users)} utilisateurs")

if users:
    print("Suppression en cours...")
    for user in users:
        client.delete(user.key)
    print("Terminé !")
else:
    print("Aucun utilisateur trouvé")
