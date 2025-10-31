from typing import Dict, Any
from threading import Lock

class InMemoryStore:
    def __init__(self):
        self._tasks: Dict[int, Dict[str, Any]] = {}
        self._comments: Dict[int, Dict[str, Any]] = {}
        self._task_comments: Dict[int, list] = {}
        self._task_id_seq = 1
        self._comment_id_seq = 1
        self._lock = Lock()

    def reset(self):
        with self._lock:
            self.__init__()

    # Tasks
    def create_task(self, title: str, description: str = None):
        with self._lock:
            tid = self._task_id_seq
            self._task_id_seq += 1
            task = {"id": tid, "title": title, "description": description}
            self._tasks[tid] = task
            self._task_comments[tid] = []
            return task

    def list_tasks(self):
        with self._lock:
            return list(self._tasks.values())

    def get_task(self, task_id: int):
        return self._tasks.get(task_id)

    def update_task(self, task_id: int, title: str, description: str = None):
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return None
            task["title"] = title
            task["description"] = description
            return task

    def delete_task(self, task_id: int):
        with self._lock:
            if task_id not in self._tasks:
                return False
            # delete its comments
            for cid in list(self._task_comments.get(task_id, [])):
                if cid in self._comments:
                    del self._comments[cid]
            self._task_comments.pop(task_id, None)
            del self._tasks[task_id]
            return True

    # Comments
    def create_comment(self, task_id: int, content: str):
        with self._lock:
            if task_id not in self._tasks:
                return None
            cid = self._comment_id_seq
            self._comment_id_seq += 1
            comment = {"id": cid, "task_id": task_id, "content": content}
            self._comments[cid] = comment
            self._task_comments.setdefault(task_id, []).append(cid)
            return comment

    def list_comments(self, task_id: int):
        with self._lock:
            ids = self._task_comments.get(task_id, [])
            return [self._comments[cid] for cid in ids if cid in self._comments]

    def get_comment(self, comment_id: int):
        return self._comments.get(comment_id)

    def update_comment(self, comment_id: int, content: str):
        with self._lock:
            comment = self._comments.get(comment_id)
            if not comment:
                return None
            comment["content"] = content
            return comment

    def delete_comment(self, comment_id: int):
        with self._lock:
            comment = self._comments.get(comment_id)
            if not comment:
                return False
            task_id = comment["task_id"]
            self._task_comments.get(task_id, []).remove(comment_id)
            del self._comments[comment_id]
            return True

# Shared global store
store = InMemoryStore()
