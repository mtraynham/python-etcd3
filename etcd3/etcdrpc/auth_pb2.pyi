"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file

Copyright 2016-2021 The jetcd authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class User(google.protobuf.message.Message):
    """User is a single entry in the bucket authUsers"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    ROLES_FIELD_NUMBER: builtins.int
    name: builtins.bytes
    password: builtins.bytes
    @property
    def roles(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        name: builtins.bytes = ...,
        password: builtins.bytes = ...,
        roles: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "password", b"password", "roles", b"roles"]) -> None: ...

global___User = User

@typing_extensions.final
class Permission(google.protobuf.message.Message):
    """Permission is a single entity"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Type:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _TypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Permission._Type.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        READ: Permission._Type.ValueType  # 0
        WRITE: Permission._Type.ValueType  # 1
        READWRITE: Permission._Type.ValueType  # 2

    class Type(_Type, metaclass=_TypeEnumTypeWrapper): ...
    READ: Permission.Type.ValueType  # 0
    WRITE: Permission.Type.ValueType  # 1
    READWRITE: Permission.Type.ValueType  # 2

    PERMTYPE_FIELD_NUMBER: builtins.int
    KEY_FIELD_NUMBER: builtins.int
    RANGE_END_FIELD_NUMBER: builtins.int
    permType: global___Permission.Type.ValueType
    key: builtins.bytes
    range_end: builtins.bytes
    def __init__(
        self,
        *,
        permType: global___Permission.Type.ValueType = ...,
        key: builtins.bytes = ...,
        range_end: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "permType", b"permType", "range_end", b"range_end"]) -> None: ...

global___Permission = Permission

@typing_extensions.final
class Role(google.protobuf.message.Message):
    """Role is a single entry in the bucket authRoles"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    KEYPERMISSION_FIELD_NUMBER: builtins.int
    name: builtins.bytes
    @property
    def keyPermission(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Permission]: ...
    def __init__(
        self,
        *,
        name: builtins.bytes = ...,
        keyPermission: collections.abc.Iterable[global___Permission] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["keyPermission", b"keyPermission", "name", b"name"]) -> None: ...

global___Role = Role