import psycopg2
from psycopg2.extras import Json
import json
from datetime import datetime
import uuid
from typing import Any, Dict, List, Optional, Union

class PostgresCursor:
    def __init__(self, collection, query, params):
        self.collection = collection
        self.query = query
        self.params = params
        self._sort = None
        self._limit = None

    def sort(self, key, direction=1):
        # direction 1 is ASC, -1 is DESC
        order = "ASC" if direction == 1 else "DESC"
        self._sort = f"doc->>'{key}' {order}"
        return self

    def limit(self, n):
        self._limit = n
        return self

    def _execute(self):
        query = self.query
        if self._sort:
            query += f" ORDER BY {self._sort}"
        if self._limit:
            query += f" LIMIT {self._limit}"
        
        with self.collection.db.conn.cursor() as cur:
            cur.execute(query, self.params)
            rows = cur.fetchall()
            docs = []
            for row in rows:
                doc = row[0]
                if isinstance(doc, str):
                    doc = json.loads(doc)
                docs.append(doc)
            return docs

    def __iter__(self):
        return iter(self._execute())

    def __getitem__(self, index):
        return self._execute()[index]

class PostgresCollection:
    def __init__(self, db, name: str):
        self.db = db
        self.name = name
        self._ensure_table()

    def _ensure_table(self):
        with self.db.conn.cursor() as cur:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.name} (id TEXT PRIMARY KEY, doc JSONB)")
            cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.name}_doc ON {self.name} USING GIN (doc)")
        self.db.conn.commit()

    def _json_serialize(self, doc):
        def default(o):
            if isinstance(o, datetime):
                return o.isoformat()
            if hasattr(o, "__str__") and "ObjectId" in str(type(o)):
                return str(o)
            return str(o)
        return json.dumps(doc, default=default)

    def insert_one(self, doc: Dict[str, Any]):
        if "_id" not in doc:
            import secrets
            doc["_id"] = secrets.token_hex(12)
        else:
            doc["_id"] = str(doc["_id"])
        
        doc_id = doc["_id"]
        json_doc = self._json_serialize(doc)
        
        with self.db.conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {self.name} (id, doc) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET doc = EXCLUDED.doc",
                (doc_id, json_doc)
            )
        self.db.conn.commit()
        
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return InsertResult(doc_id)

    def insert_many(self, docs: List[Dict[str, Any]]):
        ids = []
        with self.db.conn.cursor() as cur:
            for doc in docs:
                if "_id" not in doc:
                    import secrets
                    doc["_id"] = secrets.token_hex(12)
                else:
                    doc["_id"] = str(doc["_id"])
                
                doc_id = doc["_id"]
                ids.append(doc_id)
                json_doc = self._json_serialize(doc)
                cur.execute(
                    f"INSERT INTO {self.name} (id, doc) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET doc = EXCLUDED.doc",
                    (doc_id, json_doc)
                )
        self.db.conn.commit()
        
        class InsertManyResult:
            def __init__(self, inserted_ids):
                self.inserted_ids = inserted_ids
        return InsertManyResult(ids)

    def find_one(self, filter: Dict[str, Any], projection: Dict[str, int] = None):
        cursor = self.find(filter, projection)
        results = cursor.limit(1)._execute()
        return results[0] if results else None

    def find(self, filter: Dict[str, Any] = None, projection: Dict[str, int] = None):
        query = f"SELECT doc FROM {self.name}"
        params = []
        
        if filter:
            conditions, filter_params = self._build_where(filter)
            if conditions:
                query += " WHERE " + conditions
                params.extend(filter_params)

        cursor = PostgresCursor(self, query, params)
        cursor._projection = projection
        return cursor

    def _build_where(self, filter: Dict[str, Any]):
        conditions = []
        params = []
        
        # Support for $or
        if "$or" in filter:
            or_conditions = []
            for sub_filter in filter["$or"]:
                cond, p = self._build_where(sub_filter)
                if cond:
                    or_conditions.append(f"({cond})")
                    params.extend(p)
            if or_conditions:
                conditions.append("(" + " OR ".join(or_conditions) + ")")
        
        for k, v in filter.items():
            if k == "$or": continue
            
            # Handle nested dots (v1: only one level supported for now)
            field_ref = "id" if k == "_id" else f"doc->>'{k}'"
            if "." in k:
                parts = k.split(".")
                field_ref = f"doc->'{parts[0]}'"
                for p in parts[1:-1]:
                    field_ref += f"->'{p}'"
                field_ref += f"->>'{parts[-1]}'"

            if isinstance(v, dict):
                if "$ne" in v:
                    conditions.append(f"{field_ref} != %s")
                    params.append(str(v["$ne"]))
                elif "$in" in v:
                    placeholders = ",".join(["%s"] * len(v["$in"]))
                    conditions.append(f"{field_ref} IN ({placeholders})")
                    params.extend([str(x) for x in v["$in"]])
                elif "$gt" in v:
                    conditions.append(f"({field_ref})::numeric > %s")
                    params.append(v["$gt"])
            else:
                conditions.append(f"{field_ref} = %s")
                params.append(str(v))
        
        return " AND ".join(conditions), params

    def aggregate(self, pipeline: List[Dict[str, Any]]):
        """Very basic $group emulation for stats"""
        # For this prototype, we'll fetch then process in Python if it's a small dataset
        # In a real app, this would translate to SQL GROUP BY
        docs = list(self.find({}))
        
        for stage in pipeline:
            if "$group" in stage:
                group_config = stage["$group"]
                id_field = group_config["_id"]
                if isinstance(id_field, str) and id_field.startswith("$"):
                    id_key = id_field[1:]
                else:
                    id_key = id_field
                
                results = {}
                for doc in docs:
                    val = doc.get(id_key, "Unknown")
                    if val not in results:
                        results[val] = {"_id": val}
                        for k in group_config:
                            if k == "_id": continue
                            results[val][k] = 0
                    
                    # Handle simple $sum: 1 or $sum: {$cond: ...}
                    for k, op in group_config.items():
                        if k == "_id": continue
                        if "$sum" in op:
                            summ = op["$sum"]
                            if summ == 1:
                                results[val][k] += 1
                            elif isinstance(summ, dict) and "$cond" in summ:
                                # Very basic $cond emulation
                                cond = summ["$cond"]
                                if isinstance(cond, list) and len(cond) == 3:
                                    # [{$eq: ["$status", "completed"]}, 1, 0]
                                    eq = cond[0].get("$eq")
                                    if eq:
                                        f_key = eq[0][1:] if eq[0].startswith("$") else eq[0]
                                        if doc.get(f_key) == eq[1]:
                                            results[val][k] += cond[1]
                                        else:
                                            results[val][k] += cond[2]
                return list(results.values())
        return docs

    def update_one(self, filter: Dict[str, Any], update: Dict[str, Any]):
        doc = self.find_one(filter)
        if not doc:
            return None
        
        modified = False
        if "$set" in update:
            doc.update(update["$set"])
            modified = True
        if "$inc" in update:
            for k, v in update["$inc"].items():
                doc[k] = doc.get(k, 0) + v
            modified = True
        if "$push" in update:
            for k, v in update["$push"].items():
                if k not in doc or not isinstance(doc[k], list):
                    doc[k] = []
                doc[k].append(v)
            modified = True
        if "$addToSet" in update:
            for k, v in update["$addToSet"].items():
                if k not in doc or not isinstance(doc[k], list):
                    doc[k] = []
                if isinstance(v, dict) and "$each" in v:
                    for item in v["$each"]:
                        if item not in doc[k]:
                            doc[k].append(item)
                else:
                    if v not in doc[k]:
                        doc[k].append(v)
            modified = True
        
        if modified:
            doc["updated_at"] = datetime.now().isoformat()
            json_doc = self._json_serialize(doc)
            with self.db.conn.cursor() as cur:
                cur.execute(
                    f"UPDATE {self.name} SET doc = %s WHERE id = %s",
                    (json_doc, doc["_id"])
                )
            self.db.conn.commit()
            
        class UpdateResult:
            def __init__(self, modified_count):
                self.modified_count = modified_count
        return UpdateResult(1 if modified else 0)

    def count_documents(self, filter: Dict[str, Any]):
        query = f"SELECT COUNT(*) FROM {self.name}"
        params = []
        
        if filter:
            conditions, filter_params = self._build_where(filter)
            if conditions:
                query += " WHERE " + conditions
                params.extend(filter_params)

        with self.db.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()[0]

    def delete_many(self, filter: Dict[str, Any]):
        if not filter:
            query = f"DELETE FROM {self.name}"
            params = []
        else:
            conditions = []
            params = []
            for k, v in filter.items():
                if isinstance(v, dict) and "$ne" in v:
                    conditions.append(f"doc->>%s != %s")
                    params.extend([k, str(v["$ne"])])
                else:
                    conditions.append(f"doc->>%s = %s")
                    params.extend([k, str(v)])
            query = f"DELETE FROM {self.name} WHERE " + " AND ".join(conditions)
            
        with self.db.conn.cursor() as cur:
            cur.execute(query, params)
        self.db.conn.commit()

    def delete_one(self, filter: Dict[str, Any]):
        doc = self.find_one(filter)
        if doc:
            with self.db.conn.cursor() as cur:
                cur.execute(f"DELETE FROM {self.name} WHERE id = %s", (doc["_id"],))
            self.db.conn.commit()
            class DeleteResult:
                def __init__(self, count):
                    self.deleted_count = count
            return DeleteResult(1)
        return DeleteResult(0)

class PostgresDatabase:
    def __init__(self, conn):
        self.conn = conn

    def __getitem__(self, name: str):
        return PostgresCollection(self, name)

class PostgresClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.conn = psycopg2.connect(uri)
        # Create a mock 'admin' command for pinging
        self.admin = self

    def command(self, cmd: str):
        if cmd == 'ping':
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1")
            return {"ok": 1}
        return {}

    def __getitem__(self, name: str):
        return PostgresDatabase(self.conn)

    def close(self):
        self.conn.close()
