import httpx
from typing import Any, Dict, Optional, Set
from ..settings import BASE_URL_API


class APIClient:
    def __init__(self, base_url: str = BASE_URL_API):
        self.base_url = base_url

    async def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None,
                       params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        if params is not None:
            url += "?" + "&".join(list(map(lambda x: f"{x[0]}={x[1]}", params.items())))
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, json=data)
            response.raise_for_status()
            return response.json()

    async def create_user(self, tg_id: int, username: str) -> Dict[str, Any]:
        data = {
            "tg_id": tg_id,
            "username": username,
        }
        return await self._request("POST", "/user/", data)

    async def get_user(self, user_id: int) -> Dict[str, Any]:
        return await self._request("GET", f"/user/{user_id}")

    async def update_user(self, user_id: int, tg_id: Optional[int] = None, username: Optional[str] = None) -> Dict[
        str, Any]:
        data = {}
        if tg_id is not None:
            data["tg_id"] = tg_id
        if username is not None:
            data["username"] = username
        return await self._request("PUT", f"/user/{user_id}", data)

    async def delete_user(self, user_id: int) -> Dict[str, Any]:
        return await self._request("DELETE", f"/user/{user_id}")

    async def get_filter_users(self, tg_id: Optional[int] = None) -> Dict[str, Any]:
        params = {}
        if tg_id is not None:
            params["tg_id"] = tg_id
        return await self._request("GET", "/user/", params=params)

    async def create_role(self, role_name: str) -> Dict[str, Any]:
        data = {
            "role_name": role_name
        }
        return await self._request("POST", "/role/", data)

    async def get_role(self, role_id: int) -> Dict[str, Any]:
        return await self._request("GET", f"/role/{role_id}")

    async def update_role(self, role_id: int, role_name: Optional[str] = None) -> Dict[str, Any]:
        data = {}
        if role_name is not None:
            data["role_name"] = role_name
        return await self._request("PUT", f"/role/{role_id}", data)

    async def delete_role(self, role_id: int) -> Dict[str, Any]:
        return await self._request("DELETE", f"/role/{role_id}")

    async def get_filter_roles(self, role_name: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if role_name is not None:
            params["role_name"] = role_name
        return await self._request("GET", "/role/", params=params)

    async def assign_role_to_user(self, user_id: int, role_id: int) -> Dict[str, Any]:
        data = {
            "user_id": user_id,
            "role_id": role_id
        }
        return await self._request("POST", "/user_role/", data)

    async def get_user_roles(self, user_id: int) -> Dict[str, Any]:
        return await self._request("GET", f"/user_role/{user_id}")

    async def get_filter_user_roles(self, user_id: Optional[int] = None, role_id: Optional[int] = None) -> Dict[
        str, Any]:
        params = {}
        if user_id is not None:
            params["user_id"] = user_id
        if role_id is not None:
            params["role_id"] = role_id
        return await self._request("GET", "/user_role/", params=params)

    async def remove_role_from_user(self, user_id: int, role_id: int) -> Dict[str, Any]:
        return await self._request("DELETE", f"/user_role/{user_id}/{role_id}")

    async def get_processes(self) -> Dict[str, Any]:
        return await self._request("GET", f"/process/")

    async def create_process(self, pid: int, command: str, log_filename: str, status: bool = 1) -> Dict[str, Any]:
        data = {
            "pid": pid,
            "command": command,
            "log_filename": log_filename,
            "status": status
        }
        return await self._request("POST", "/process/", data)

    async def get_process(self, process_id: int) -> Dict[str, Any]:
        return await self._request("GET", f"/process/{process_id}")

    async def update_process(self, process_id: int, status: Optional[bool]) -> Dict[str, Any]:
        data = {
            "status": status
        }
        return await self._request("PUT", f"/process/{process_id}", data)

    async def delete_process(self, process_id: int) -> Dict[str, Any]:
        return await self._request("DELETE", f"/process/{process_id}")
