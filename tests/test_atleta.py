import pytest

'''
pytest tests/test_atleta.py -v

'''

@pytest.mark.asyncio
async def test_criar_atleta(client):
    # Primeiro cria a categoria
    response = await client.post("/categoria/", json={"nome": "Scale"})
    assert response.status_code == 201
    categoria = response.json()

    # Depois cria o centro de treinamento
    response = await client.post("/centro_treinamento/", json={
            "nome": "CT king",
            "endereco": "Rua x.0022",
            "proprietario": "Marcos2"
        })
    assert response.status_code == 201
    ct = response.json()

    # Agora cria o atleta
    response = await client.post("/atleta/", json={
        "nome": "Joao",
        "cpf": "12345678900",
        "idade": 25,
        "peso": 75.5,
        "altura": 1.7,
        "sexo": "M",
        "categoria": {"nome": categoria["nome"]},
        "centro_treinamento": {"nome": ct["nome"]}
    })
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Joao"
    assert data["cpf"] == "12345678900"
    assert data["categoria"]["nome"] == "Scale"
    assert data["centro_treinamento"]["nome"] == "CT king"
    assert "id" in data
    assert "created_at" in data

    atleta_id = data["id"]   # <- agora está ativo

    # GET /atleta/{id}
    response = await client.get(f"/atleta/{atleta_id}")
    assert response.status_code == 200
    assert response.json()["cpf"] == "12345678900"

    # PATCH /atleta/{id}
    response = await client.patch(f"/atleta/{atleta_id}", json={"peso": 80})
    assert response.status_code == 200
    assert response.json()["peso"] == 80

    # DELETE /atleta/{id}
    response = await client.delete(f"/atleta/{atleta_id}")
    assert response.status_code == 204
    #assert response.json()["message"] == "Atleta deletado com sucesso"

    # GET /atleta (lista)
    response = await client.get("/atleta/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

