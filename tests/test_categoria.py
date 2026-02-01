import pytest
'''
pytest tests/test_categoria.py -v

'''
@pytest.mark.asyncio
async def test_crud_categoria(client):
    # POST /categoria
    response = await client.post("/categoria/", json={"nome": "Scale"})
    assert response.status_code == 201
    categoria = response.json()
    categoria_id = categoria["id"]

    # GET /categoria/{id}
    response = await client.get(f"/categoria/{categoria_id}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Scale"

    # PATCH /categoria/{id}
    response = await client.patch(f"/categoria/{categoria_id}", json={"nome": "Elite"})
    assert response.status_code == 200
    assert response.json()["nome"] == "Elite"

    # DELETE /categoria/{id}
    response = await client.delete(f"/categoria/{categoria_id}")
    assert response.status_code == 204
    #assert response.json()["mensagem"] == "categoria deletada com sucesso"

    # GET /categoria (lista)
    response = await client.get("/categoria/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
