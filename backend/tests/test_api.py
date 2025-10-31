import pytest
from httpx import AsyncClient
from backend import main
from backend import store as storemod

@pytest.fixture(autouse=True)
def reset_store():
    # reset before each test
    storemod.store.reset()
    yield
    storemod.store.reset()

@pytest.mark.anyio
async def test_tasks_crud():
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # create
        resp = await ac.post("/tasks/", json={"title":"T1","description":"d1"})
        assert resp.status_code == 200
        t = resp.json()
        tid = t["id"]

        # get
        resp = await ac.get(f"/tasks/{tid}")
        assert resp.status_code == 200

        # update
        resp = await ac.put(f"/tasks/{tid}", json={"title":"T1-upd","description":"d2"})
        assert resp.status_code == 200
        assert resp.json()["title"] == "T1-upd"

        # list
        resp = await ac.get("/tasks/")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        # delete
        resp = await ac.delete(f"/tasks/{tid}")
        assert resp.status_code == 200

        # not found
        resp = await ac.get(f"/tasks/{tid}")
        assert resp.status_code == 404

@pytest.mark.anyio
async def test_comments_crud():
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        # create task
        resp = await ac.post("/tasks/", json={"title":"TaskC","description":"d"})
        tid = resp.json()["id"]

        # add comment
        resp = await ac.post(f"/tasks/{tid}/comments/", json={"content":"c1"})
        assert resp.status_code == 200
        cid = resp.json()["id"]

        # list
        resp = await ac.get(f"/tasks/{tid}/comments/")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        # update comment
        resp = await ac.put(f"/comments/{cid}", json={"content":"c1-upd"})
        assert resp.status_code == 200
        assert resp.json()["content"] == "c1-upd"

        # delete comment
        resp = await ac.delete(f"/comments/{cid}")
        assert resp.status_code == 200

        # list now empty
        resp = await ac.get(f"/tasks/{tid}/comments/")
        assert resp.status_code == 200
        assert len(resp.json()) == 0
