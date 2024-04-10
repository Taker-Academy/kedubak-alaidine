# Documentation de l'API, by Stephane

## Schéma de la base de données

### User 👤

Le schéma utilisateur définit la structure des données pour un utilisateur dans la base de données.

- **createdAt (Date):** Date de création de l'utilisateur (par défaut, la date actuelle).
- **email (String):** Adresse e-mail de l'utilisateur (unique et obligatoire).
- **firstName (String):** Prénom de l'utilisateur (obligatoire).
- **lastName (String):** Nom de famille de l'utilisateur (obligatoire).
- **password (String):** Mot de passe de l'utilisateur (obligatoire).
- **lastUpVote (Date):** Date du dernier vote (par défaut, la date actuelle - 1 minute).
- **_id (ObjectId):** ID de l'utilisateur généré par MongoDB.

### Post 🪧

Le schéma de publication définit la structure des données pour une publication dans la base de données.

- **createdAt (Date):** Date de création du post.
- **userId (String):** ID de l'utilisateur qui a créé le post.
- **firstName (String):** Prénom de l'utilisateur qui a créé le post.
- **title (String):** Titre du post.
- **content (String):** Contenu du post.
- **comments (Array):** Liste des commentaires associés au post.
    **createdAt (Date):** Date de création du commentaire, par défaut la date actuelle.
    **id (String):** ID du commentaire.
    **firstName (String):** Prénom de l'utilisateur qui a créé le commentaire.
    **content (String):** Contenu du commentaire.
- **upVotes (String)(Array):** Liste des ID des utilisateurs ayant donné un vote positif au post. (un seul vote utilisateur par post)

---

## Authentification 🔑

L'authentification est gérée par un token JWT (JSON Web Token) qui est généré lors de la connexion ou l'inscription d'un utilisateur.
Il doit être envoyé dans le header de chaque requête pour les routes protégées, sous forme de `"Bearer {TOKEN}"`.

> ℹ️ Le token est construit à partir de l'id de l'utilisateur *(_id)* pour une durée de 24h
---

# Routes

- 🔐 = La route nécessite un token JWT valide dans le header de la requête.

## Auth

> Prefix: `/auth`

### Endpoint [POST] `/register`

## Description

Cette route permet de créer un nouvel utilisateur dans la base de données, il chiffre également le mot de passe de l'utilisateur avant de le stocker dans la base de données. Si un utilisateur avec la même adresse e-mail existe déjà, la requête échouera.
Le serveur renvoie un token JWT qui permettra à l'utilisateur de s'authentifier sur les routes protégées.

## Paramètres

### Body

- **email (String, required):** Adresse e-mail de l'utilisateur.
- **password (String, required):** Mot de passe de l'utilisateur.
- **firstName (String, required):** Prénom de l'utilisateur.
- **lastName (String, required):** Nom de famille de l'utilisateur.

## Exemple de Requête

```json
{
    "email": "my.email@bip.com",
    "password": "myPassword123",
    "firstName": "John",
    "lastName": "Doe"
}
```


## Format de réponse (201 OK)

```json
{
    "ok": true,
    "data": {
        "token": "eg.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NzQzYWNmZWI0NjU3MTU0Yjg1Y2VjMyIsImlhdCI6MTcwMjExNjA0NywiZXhwIjoxNzAyMjAyNDQ3fQ.hQ2Om2eiNVPquH9npiCC9hOUy3hoizsFVt8QACCPolU",
        "user": {
            "email": "my.email@gmail.com",
            "firstName": "John",
            "lastName": "Doe"
        }
    }
}
```


## Réponse possible

- **201 OK:** Utilisateur créé avec succès.
- **400 Bad Request:** Mauvaise requête, paramètres manquants ou invalides.
- **401 Unauthorized:** Mauvais identifiants.
- **500 Internal Server Error:** Erreur interne du serveur.
--- 

### Endpoint [POST] `/login`

## Description

Cette route permet de connecter un utilisateur existant à l'application. Si les identifiants sont corrects, le serveur renvoie un token JWT qui permettra à l'utilisateur de s'authentifier sur les routes protégées.

## Paramètres

### Body

- **email (String, required):** Adresse e-mail de l'utilisateur.
- **password (String, required):** Mot de passe de l'utilisateur.

## Format de réponse (200 OK)

```json
{
    "ok": true,
    "data": {
        "token": "eg.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1NzQzYWNmZWI0NjU3MTU0Yjg1Y2VjMyIsImlhdCI6MTcwMjExNjA0NywiZXhwIjoxNzAyMjAyNDQ3fQ.hQ2Om2eiNVPquH9npiCC9hOUy3hoizsFVt8QACCPolU",
        "user": {
            "email": "my.email@gmail.com",
            "firstName": "John",
            "lastName": "Doe"
        }
    }
}
```


## Réponse possible

- **200 OK:** Connexion réussie.
- **400 Bad Request:** Mauvaise requête, paramètres manquants ou invalides.
- **401 Unauthorized:** Mauvais identifiants.
- **500 Internal Server Error:** Erreur interne du serveur.

---

## User

> Prefix: `/user`

### Endpoint [GET] `/me` 🔐

## Description

Cette route permet de récupérer les informations de l'utilisateur connecté.

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.


## Format de réponse (200 OK)

```json
{
    "ok": true,
    "data": {
        "email": "test@test.com",
        "firstName": "John",
        "lastName": "Doe"
    }
}
```

## Réponses Possibles
- **200 OK:** Utilisateur récupéré avec succès.
- **401 Unauthorized:** Mauvais token JWT.
- **500 Internal Server Error:** Erreur interne du serveur.


--- 

### Endpoint [PUT] `/edit` 🔐

## Description

Cette route permet à un utilisateur de modifier ses informations.

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.

### Body

- **firstName (String, optional):** Nouveau prénom de l'utilisateur.
- **lastName (String, optional):** Nouveau nom de famille de l'utilisateur.
- **email (String, optional):** Nouvelle adresse e-mail de l'utilisateur.
- **password (String, optional):** Nouveau mot de passe de l'utilisateur.

## Format de réponse (200 OK)

```json
{
    "ok": true,
    "data": {
        "email": "john.doe@example.com",
        "firstName": "John",
        "lastName": "Doe"
    }
}
```

## Réponses Possibles
- **200 OK:** Informations de l'utilisateur mises à jour avec succès.
- **401 Unauthorized:** Mauvais token JWT.
- **422 Unprocessable Entity:** Échec de validation des paramètres.
- **500 Internal Server Error:** Erreur interne du serveur.

---

### Endpoint [DELETE] `/remove` 🔐

## Description

Cette route permet à un utilisateur de supprimer son compte.

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.

## Format de réponse (200 OK)

```json
{
    "ok": true,
    "data": {
        "email": "john.doe@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "removed": true
    }
}
```

## Réponses Possibles
- **200 OK:** Compte utilisateur supprimé avec succès.
- **401 Unauthorized:** Mauvais token JWT.
- **404 Not Found:** Utilisateur non trouvé.
- **500 Internal Server Error:** Erreur interne du serveur.

---

## Post

> Prefix: `/post`

### Endpoint [GET] `/` 🔐

## Description

Cette route permet de récupérer la liste des éléments (posts).

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.

## Format de réponse (200 OK)

```json
{
    "ok": true,
    "data": [
        // Liste des éléments (posts)
        {
            "_id": "cfz5a15ae84a1z87",
            "createdAt": "2023-01-01T00:00:00.000Z",
            "userId": "user123",
            "firstName": "John",
            "title": "Titre du post",
            "content": "Contenu du post",
            "comments": [
                {
                    "id": "comment1",
                    "firstName": "Jane",
                    "content": "Super post!"
                },
                {
                    "id": "comment2",
                    "firstName": "Bob",
                    "content": "J'adore ce sujet!"
                }
            ],
            "upVotes": ["user456", "user789"]
        },
    ]
}
```

## Réponses Possibles
- **200 OK:** Liste des éléments récupérée avec succès.
- **401 Unauthorized:** Mauvais token JWT.
- **500 Internal Server Error:** Erreur interne du serveur.

--- 

### Endpoint [POST] `/` 🔐

## Description

Cette route permet à un utilisateur de créer un nouvel élément (post).

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.

### Body

- **title (String, required):** Titre du post.
- **content (String, required):** Contenu du post.

## Format de réponse (201 Created)

```json
{
    "ok": true,
    "data": {
        "_id": "cfz5a15ae84a1z87",
        "createdAt": "2023-01-01T00:00:00.000Z",
        "userId": "user123",
        "firstName": "John",
        "title": "Titre du post",
        "content": "Contenu du post",
        "comments": [],
        "upVotes": []
    }
}
```

## Réponses Possibles

- **201 Created:** Élément créé avec succès.
- **400 Bad Request:** Mauvaise requête, paramètres manquants ou invalides.
- **401 Unauthorized:** Mauvais token JWT.

---

### Endpoint [GET] `/me` 🔐

## Description

Cette route permet de récupérer la liste des éléments (posts) appartenant à l'utilisateur connecté.

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.

## Format de réponse (200 OK)

```json
{
    "ok": true,
    "data": [
        // Liste des éléments (posts) de l'utilisateur
        {
            "_id": "cfz5a15ae84a1z87",
            "createdAt": "2023-01-01T00:00:00.000Z",
            "userId": "user123",
            "firstName": "John",
            "title": "Titre du post",
            "content": "Contenu du post",
            "comments": [
                {
                    "id": "comment1",
                    "firstName": "Jane",
                    "content": "Super post!"
                },
                {
                    "id": "comment2",
                    "firstName": "Bob",
                    "content": "J'adore ce sujet!"
                }
            ],
            "upVotes": ["user456", "user789"]
        },
        // Autres éléments (posts) de l'utilisateur
    ]
}
```

## Réponses Possibles
- **200 OK:** Liste des éléments de l'utilisateur récupérée avec succès.
- **401 Unauthorized:** Mauvais token JWT.
- **500 Internal Server Error:** Erreur interne du serveur.

---

### Endpoint [GET] `/:id` 🔐

## Description

Cette route permet de récupérer les détails d'un élément (post) spécifique.

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.

### URL Paramètre

- **id (String, required):** ID de l'élément (post) à récupérer.

## Format de réponse (200 OK)

```json
{
    "ok": true,
    "data": {
        "_id": "cfz5a15ae84a1z87",
        "createdAt": "2023-01-01T00:00:00.000Z",
        "userId": "user123",
        "firstName": "John",
        "title": "Titre du post",
        "content": "Contenu du post",
        "comments": [
            {
                "id": "comment1",
                "firstName": "Jane",
                "content": "Super post!"
            },
            {
                "id": "comment2",
                "firstName": "Bob",
                "content": "J'adore ce sujet!"
            }
        ],
        "upVotes": ["user456", "user789"]
    }
}
```

## Réponses Possibles
- **200 OK:** Détails de l'élément récupérés avec succès.
- **400 Bad Request:** Mauvaise requête, paramètres manquants ou invalides.
- **401 Unauthorized:** Mauvais token JWT.
- **404 Not Found:** Élément non trouvé.
- **500 Internal Server Error:** Erreur interne du serveur.

---

### Endpoint [DELETE] `/:id` 🔐

## Description

Cette route permet à l'utilisateur propriétaire de supprimer un élément (post) spécifique.

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.

### URL Paramètre

- **id (String, required):** ID de l'élément (post) à supprimer.

## Format de réponse (200 OK)

```json
{
    "ok": true,
    "data": {
        "_id": "cfz5a15ae84a1z87",
        "createdAt": "2023-01-01T00:00:00.000Z",
        "userId": "user123",
        "firstName": "John",
        "title": "Titre du post",
        "content": "Contenu du post",
        "comments": [
            {
                "id": "comment1",
                "firstName": "Jane",
                "content": "Super post!"
            },
            {
                "id": "comment2",
                "firstName": "Bob",
                "content": "J'adore ce sujet!"
            }
        ],
        "upVotes": ["user456", "user789"],
        "removed": true
    }
}
```

## Réponses Possibles
- **200 OK:** Élément supprimé avec succès.
- **400 Bad Request:** Mauvaise requête, paramètres manquants ou invalides.
- **401 Unauthorized:** Mauvais token JWT.
- **403 Forbidden:** L'utilisateur n'est pas le propriétaire de l'élément.
- **404 Not Found:** Élément non trouvé.
- **500 Internal Server Error:** Erreur interne du serveur.

--- 

### Endpoint [POST] `/vote/:id` 🔐

## Description

Cette route permet à l'utilisateur de voter pour un élément (post) spécifique.

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.

### URL Paramètre

- **id (String, required):** ID de l'élément (post) à voter.

## Format de réponse (200 OK)

```json
{
    "ok": true,
    "message": "post upvoted"
}
```

## Réponses Possibles
- **200 OK:** Vote enregistré avec succès.
- **401 Unauthorized:** Mauvais token JWT.
- **403 Forbidden:** Vous ne pouvez voter que toutes les minutes.
- **404 Not Found:** Élément non trouvé.
- **409 Conflict:** Vous avez déjà voté pour ce post.
- **422 Unprocessable Entity:** ID invalide.
- **500 Internal Server Error:** Erreur interne du serveur.

---

## Comment

> Prefix: `/comment`

### Endpoint [POST] `/:id` 🔐

## Description

Cette route permet à un utilisateur de créer un nouveau commentaire sur un élément (post) spécifique.

## Paramètres

### Header

- **Authorization (String, required):** Token JWT pour l'authentification.

### URL Paramètre

- **id (String, required):** ID de l'élément (post) à commenter.

### Body

- **content (String, required):** Contenu du commentaire.

## Format de réponse (201 Created)

```json
{
    "ok": true,
    "data": {
        "firstName": "John",
        "content": "Contenu du commentaire"
        "createdAt": Date.now()
    }
}
```

## Réponses Possibles

- **201 Created:** Commentaire créé avec succès.
- **400 Bad Request:** Mauvaise requête, paramètres manquants ou invalides.
- **401 Unauthorized:** Mauvais token JWT.

---

# Erreurs

Toutes les erreurs renverront un objet JSON avec un message d'erreur approprié et un code d'état HTTP correspondant.

## Format de réponse

```json
{
    "ok": false,
    "error": "Description de l'erreur",
}
```
