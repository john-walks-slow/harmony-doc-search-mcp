from __future__ import annotations

import datetime as _dt
import json
import logging
import os
from typing import Any

import httpx
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

SEARCH_API_URL = (
    "https://svc-drcn.developer.huawei.com/community/servlet/consumer/"
    "partnerCommunityService/developer/search"
)
DEFAULT_TIMEOUT_SECONDS = 15.0
DEFAULT_LANGUAGE = os.getenv("HARMONY_DOC_LANGUAGE", "zh")
DEFAULT_COUNTRY = os.getenv("HARMONY_DOC_COUNTRY", "CN")
DEFAULT_DEVICE_ID = os.getenv("HARMONY_DOC_DEVICE_ID", "ESN")
DEFAULT_DEVICE_TYPE = os.getenv("HARMONY_DOC_DEVICE_TYPE", "1")
DEFAULT_VERIFY_SSL = os.getenv("HARMONY_DOC_VERIFY_SSL", "true").lower() in {
    "1",
    "true",
    "yes",
    "on",
}
DEFAULT_CATEGORY_LIST = [1, 3, 4, 8, 10, 11, 12, 13, 15, 16, 19]

mcp = FastMCP(name="harmonyos-api-server")


def get_formatted_timestamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d%H%M%S")


def _build_payload(query: str, offset: int, length: int) -> dict[str, Any]:
    return {
        "deviceId": DEFAULT_DEVICE_ID,
        "deviceType": DEFAULT_DEVICE_TYPE,
        "language": DEFAULT_LANGUAGE,
        "country": DEFAULT_COUNTRY,
        "keyWord": query,
        "requestOrgin": 5,
        "ts": get_formatted_timestamp(),
        "developerVertical": {
            "category": 1,
            "language": DEFAULT_LANGUAGE,
            "categoryList": DEFAULT_CATEGORY_LIST,
        },
        "cutPage": {"offset": offset, "length": length},
    }


def _normalize_link(link: str | None) -> str:
    if not link:
        return "无链接"
    if link.startswith("//"):
        return f"https:{link}"
    return link


def _extract_kit_info(ext: str | None) -> str:
    if not ext:
        return ""
    try:
        ext_data = json.loads(ext)
    except json.JSONDecodeError:
        return ""

    kit_name = ext_data.get("kitName", "Kit")
    catalog_name = ext_data.get("catalogName", "分类")
    return f"[{kit_name} - {catalog_name}] "


def _format_results(query: str, infos: list[dict[str, Any]]) -> str:
    formatted_results: list[str] = []
    for item in infos:
        title = item.get("name", "")
        description = item.get("description", "")
        link = _normalize_link(item.get("url"))
        kit_info = _extract_kit_info(item.get("ext"))
        formatted_results.append(
            f"标题: {kit_info}{title}\n"
            f"摘要: {description}\n"
            f"链接: {link}\n---"
        )

    result_block = "\n".join(formatted_results)
    return f'找到关于 "{query}" 的鸿蒙官方文档：\n\n{result_block}'


@mcp.tool
def search_harmonyos_api(query: str, offset: int = 0, length: int = 15) -> str:
    """查询鸿蒙系统 (HarmonyOS NEXT) 官方 API 文档、ArkTS 语法和 ArkUI 组件用法，返回文档标题、链接、摘要。"""
    logger.info("Searching HarmonyOS docs: query=%s offset=%s length=%s", query, offset, length)

    if not query.strip():
        return "查询关键词不能为空。"
    if offset < 0:
        return "offset 不能小于 0。"
    if length <= 0:
        return "length 必须大于 0。"

    payload = _build_payload(query=query, offset=offset, length=length)

    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "harmony-doc-search-mcp/0.1.0",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    try:
        with httpx.Client(
            timeout=DEFAULT_TIMEOUT_SECONDS,
            verify=DEFAULT_VERIFY_SSL,
            trust_env=True,
        ) as client:
            response = client.post(SEARCH_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as error:
        details = error.response.text
        logger.exception("HarmonyOS search HTTP error")
        return f"查询鸿蒙 API 失败：HTTP {error.response.status_code} - {details}"
    except Exception as error:  # pragma: no cover
        logger.exception("HarmonyOS search unexpected error")
        return f"查询鸿蒙 API 失败：{error}"

    search_result = data.get("searchResult") or []
    if not search_result:
        return f'未找到关于 "{query}" 的鸿蒙 API 文档结果。'

    developer_infos = search_result[0].get("developerInfos") or []
    if not developer_infos:
        return f'未找到关于 "{query}" 的鸿蒙 API 文档结果。'

    return _format_results(query=query, infos=developer_infos)


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    mcp.run()


if __name__ == "__main__":
    main()
