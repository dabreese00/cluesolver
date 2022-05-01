from typing import Dict, Any

from sqlalchemy import select, insert

from cluesolver.db import get_db


class ObjectViewBase():
    relative_url: str = ''
    post_dict: Dict[str, Any] = {}
    model: Any = None
    list_key: str = ''

    def post(self, client, json):
        return client.post(self.relative_url, json=json)

    def get_detail(self, client, name):
        return client.get(self.relative_url + '/' + name)

    def get(self, client):
        return client.get(self.relative_url)

    def _list_via_direct_query(self, app):
        with app.app_context():
            db = get_db()
            sel = select(self.model.name)
            objects = list(db.execute(sel).fetchall())
        return objects

    def _create_via_direct_query(self, app, obj_dict):
        with app.app_context():
            db = get_db()
            ins = insert(self.model)
            result = db.execute(ins, obj_dict)
            db.commit()
        return result

    def test_create(self, app, client):
        r = self.post(client, self.post_dict)
        assert r.status_code == 201

        objects = self._list_via_direct_query(app)
        assert objects == [(self.post_dict['name'],)]

    def test_list(self, app, client):
        self._create_via_direct_query(app, self.post_dict)
        response = self.get(client)
        objects = response.json[self.list_key]
        assert response.status_code == 200
        assert objects == [self.post_dict]

    def test_get(self, app, client):
        self._create_via_direct_query(app, self.post_dict)
        response = self.get_detail(client, self.post_dict['name'])
        obj = response.json
        assert response.status_code == 200
        assert obj == self.post_dict

    def test_create_returns_401_if_noname(self, app, client):
        temp_post_dict = self.post_dict.copy()
        temp_post_dict.pop('name')
        r = self.post(client, temp_post_dict)
        assert r.status_code == 401

    def test_create_duplicate_returns_401(self, app, client):
        self._create_via_direct_query(app, self.post_dict)
        r = self.post(client, self.post_dict)
        assert r.status_code == 401

    def test_get_nonexistent_returns_404(self, app, client):
        r = self.get_detail(client, 'idontexist')
        assert r.status_code == 404
