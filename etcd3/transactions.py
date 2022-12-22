import typing

import etcd3.etcdrpc as etcdrpc
import etcd3.leases as leases
import etcd3.utils as utils

_OPERATORS = {
    etcdrpc.Compare.EQUAL: "==",
    etcdrpc.Compare.NOT_EQUAL: "!=",
    etcdrpc.Compare.LESS: "<",
    etcdrpc.Compare.GREATER: ">"
}

KVKey = typing.Union[bytes, str]
KVValue = typing.Union[bytes, str, int]


class BaseCompare:
    def __init__(self, key: KVKey, range_end: typing.Optional[KVKey] = None):
        self.key = key
        self.range_end = range_end
        self.value: typing.Optional[KVValue] = None
        self.op: typing.Optional[
            etcdrpc.Compare.CompareResult.ValueType
        ] = None

    # TODO check other is of correct type for compare
    # Version, Mod and Create can only be ints
    def __eq__(self, other: KVValue) -> 'BaseCompare':  # type: ignore
        self.value = other
        self.op = etcdrpc.Compare.EQUAL
        return self

    def __ne__(self, other: KVValue) -> 'BaseCompare':  # type: ignore
        self.value = other
        self.op = etcdrpc.Compare.NOT_EQUAL
        return self

    def __lt__(self, other: KVValue) -> 'BaseCompare':
        self.value = other
        self.op = etcdrpc.Compare.LESS
        return self

    def __gt__(self, other: KVValue) -> 'BaseCompare':
        self.value = other
        self.op = etcdrpc.Compare.GREATER
        return self

    def __repr__(self) -> str:
        if self.range_end is None:
            keys = self.key
        else:
            keys = "[{}, {})".format(str(self.key), str(self.range_end))
        return "{}: {} {} '{}'".format(
            self.__class__,
            str(keys),
            _OPERATORS.get(self.op) if self.op else '?',
            str(self.value)
        )

    def build_message(self) -> etcdrpc.Compare:
        compare = etcdrpc.Compare()
        compare.key = utils.to_bytes(self.key)
        if self.range_end is not None:
            compare.range_end = utils.to_bytes(self.range_end)

        if self.op is None:
            raise ValueError('op must be one of =, !=, < or >')

        compare.result = self.op

        self.build_compare(compare)
        return compare

    def build_compare(self, compare: etcdrpc.Compare) -> None:
        raise NotImplementedError


class Value(BaseCompare):
    def build_compare(self, compare: etcdrpc.Compare) -> None:
        compare.target = etcdrpc.Compare.VALUE
        if self.value is not None:
            compare.value = utils.to_bytes(self.value)


class Version(BaseCompare):
    def build_compare(self, compare: etcdrpc.Compare) -> None:
        compare.target = etcdrpc.Compare.VERSION
        if self.value is not None:
            compare.version = int(self.value)


class Create(BaseCompare):
    def build_compare(self, compare: etcdrpc.Compare) -> None:
        compare.target = etcdrpc.Compare.CREATE
        if self.value is not None:
            compare.create_revision = int(self.value)


class Mod(BaseCompare):
    def build_compare(self, compare: etcdrpc.Compare) -> None:
        compare.target = etcdrpc.Compare.MOD
        if self.value is not None:
            compare.mod_revision = int(self.value)


class Put:
    def __init__(
        self,
        key: KVKey,
        value: KVValue,
        lease: typing.Optional[typing.Union[leases.Lease, int, str]] = None,
        prev_kv: bool = False
    ):
        self.key = key
        self.value = value
        self.lease = lease
        self.prev_kv = prev_kv


class Get:
    def __init__(
        self,
        key: KVKey,
        range_end: typing.Optional[KVKey] = None
    ):
        self.key = key
        self.range_end = range_end


class Delete:
    def __init__(
        self,
        key: KVKey,
        range_end: typing.Optional[KVKey] = None,
        prev_kv: bool = False
    ):
        self.key = key
        self.range_end = range_end
        self.prev_kv = prev_kv


class Txn:
    def __init__(
        self,
        compare: typing.List[BaseCompare],
        success: typing.Optional[
            typing.List[typing.Union[Put, Get, Delete]]
        ] = None,
        failure: typing.Optional[
            typing.List[typing.Union[Put, Get, Delete]]
        ] = None
    ):
        self.compare = compare
        self.success = success
        self.failure = failure
