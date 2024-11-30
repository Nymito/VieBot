import unittest
from client import get_payload, API_URL_OFFER
from utils import get_payload
import requests

class TestBusinessFranceAPI(unittest.TestCase):

    def test_fetch_offers_real_api_call(self):
        # Exemple de filtres
        example_filters = {"query": "dev", "location": "etats-unis"}

        # Générer le payload
        payload = get_payload(limit=10, filters=example_filters)

        # Effectuer un vrai appel à l'API
        response = requests.post(API_URL_OFFER, json=payload)

        # Vérifications
        self.assertEqual(response.status_code, 200, "Le code de statut n'est pas 200")
        result = response.json()

        # Vérifie si le résultat contient les clés attendues
        self.assertIn("result", result, "La réponse ne contient pas la clé 'result'")
        self.assertIn("count", result, "La réponse ne contient pas la clé 'count'")

        # Vérifie si les résultats ne sont pas vides
        self.assertGreater(len(result["result"]), 0, "La liste des résultats est vide")
        print("Les résultats de l'API :", result["result"][:3])  # Affiche les trois premiers résultats

        # Vérifie un champ d'un élément
        first_offer = result["result"][0]
        self.assertIn("id", first_offer, "L'offre ne contient pas de clé 'id'")
        self.assertIn("organizationName", first_offer, "L'offre ne contient pas de clé 'organizationName'")

if __name__ == "__main__":
    unittest.main()