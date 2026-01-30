import pytest
'''
pytest tests/test_centro_treinamento.py -v
'''
@pytest.mark.asyncio
async def test_crud_centro_treinamento(client):
    # POST /centro_treinamento
    response = await client.post("/centro_treinamento/", json={
        "nome": "CT king",
        "endereco": "Rua x.002",
        "proprietario": "Marcos"
    })
    assert response.status_code == 201
    centro = response.json()
    centro_id = centro["id"]

    # GET /centro_treinamento/{id}
    response = await client.get(f"/centro_treinamento/{centro_id}")
    assert response.status_code == 200
    assert response.json()["nome"] == "CT king"

    # PATCH /centro_treinamento/{id}
    response = await client.patch(f"/centro_treinamento/{centro_id}", json={
        "nome": "CT Elite",
        "endereco": "Rua x.002",
        "proprietario": "Marcos"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "CT Elite"

    # DELETE /centro_treinamento/{id}
    response = await client.delete(f"/centro_treinamento/{centro_id}")
    assert response.status_code == 204
    #assert response.json()["mesagem"] == "centro de treinamento deletado com sucesso"

    # GET /centro_treinamento (lista)
    response = await client.get("/centro_treinamento/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
