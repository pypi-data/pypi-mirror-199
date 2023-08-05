"""
Metadeco allows you to set metadata to decorated objects.

Copyright 2023-present Julien Mauroy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import sys
import typing

__author__ = "Predeactor"
__authors__ = ["Predeactor <pro.julien.mauroy@gmail.com>"]
__version__ = "0.2.1"

if sys.version_info.minor > 9:
    _F = typing.ParamSpec("_F")
else:
    from typing_extensions import ParamSpec
    _F = ParamSpec("_F")  # type: ignore
_R = typing.TypeVar("_R")


def __ensure_target(target: typing.Any, property: typing.Optional[str]) -> typing.Any:
    # Ensure target is not None
    if not target:
        raise ValueError("Subject is None, can't lookup empty object")

    # Define what we must lookup (Target or property of target)
    final_target = getattr(target, property) if property else target
    if not final_target:
        raise ValueError("Could not obtain property in '{subject}'")

    return final_target


def metadata(
    key: str, value: typing.Any
) -> typing.Callable[[typing.Callable[_F, _R]], typing.Callable[_F, _R]]:
    def decorator(target: typing.Callable[_F, _R]) -> typing.Callable[_F, _R]:
        define_metadata(target, key, value, None)
        return target

    return decorator


def has_metadata(target: typing.Any, property: typing.Optional[str] = None) -> bool:
    final_target = __ensure_target(target, property)

    return (
        len(final_target.metadata) > 0 if hasattr(final_target, "metadata") else False
    )


def define_metadata(
    target: typing.Any,
    key: str,
    value: typing.Any,
    property: typing.Optional[str] = None,
):
    final_target = __ensure_target(target, property)

    if not hasattr(final_target, "metadata"):
        final_target.metadata = {}
    final_target.metadata[key] = value


def get_metadata(
    target: typing.Any, key: str, property: typing.Optional[str] = None
) -> typing.Optional[typing.Any]:
    final_target = __ensure_target(target, property)

    if not hasattr(final_target, "metadata"):
        raise ValueError(f"No metadata has been registered to '{target}'")

    # Get all metadata and see if the one we want is registered
    metadata = final_target.metadata

    if key not in metadata:
        raise ValueError(f"Metadata '{key}' is not set on object '{target}'")

    # And voilà!
    return metadata[key]


def list_metadata(
    target: typing.Any, property: typing.Optional[str] = None
) -> typing.Dict[str, typing.Any]:
    final_target = __ensure_target(target, property)

    return final_target.metadata


def delete_metadata(
    target: typing.Any, key: str, property: typing.Optional[str] = None
) -> None:
    final_target = __ensure_target(target, property)

    if not hasattr(final_target, "metadata"):
        return
    metadata = final_target.metadata

    if key in metadata:
        del metadata[key]
