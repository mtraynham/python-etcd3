# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: etcd3/etcdrpc/rpc.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from etcd3.etcdrpc import kv_pb2 as etcd3_dot_etcdrpc_dot_kv__pb2
from etcd3.etcdrpc import auth_pb2 as etcd3_dot_etcdrpc_dot_auth__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x65tcd3/etcdrpc/rpc.proto\x12\x0c\x65tcdserverpb\x1a\x16\x65tcd3/etcdrpc/kv.proto\x1a\x18\x65tcd3/etcdrpc/auth.proto\"\\\n\x0eResponseHeader\x12\x12\n\ncluster_id\x18\x01 \x01(\x04\x12\x11\n\tmember_id\x18\x02 \x01(\x04\x12\x10\n\x08revision\x18\x03 \x01(\x03\x12\x11\n\traft_term\x18\x04 \x01(\x04\"\xe4\x03\n\x0cRangeRequest\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\x11\n\trange_end\x18\x02 \x01(\x0c\x12\r\n\x05limit\x18\x03 \x01(\x03\x12\x10\n\x08revision\x18\x04 \x01(\x03\x12\x38\n\nsort_order\x18\x05 \x01(\x0e\x32$.etcdserverpb.RangeRequest.SortOrder\x12:\n\x0bsort_target\x18\x06 \x01(\x0e\x32%.etcdserverpb.RangeRequest.SortTarget\x12\x14\n\x0cserializable\x18\x07 \x01(\x08\x12\x11\n\tkeys_only\x18\x08 \x01(\x08\x12\x12\n\ncount_only\x18\t \x01(\x08\x12\x18\n\x10min_mod_revision\x18\n \x01(\x03\x12\x18\n\x10max_mod_revision\x18\x0b \x01(\x03\x12\x1b\n\x13min_create_revision\x18\x0c \x01(\x03\x12\x1b\n\x13max_create_revision\x18\r \x01(\x03\".\n\tSortOrder\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06\x41SCEND\x10\x01\x12\x0b\n\x07\x44\x45SCEND\x10\x02\"B\n\nSortTarget\x12\x07\n\x03KEY\x10\x00\x12\x0b\n\x07VERSION\x10\x01\x12\n\n\x06\x43REATE\x10\x02\x12\x07\n\x03MOD\x10\x03\x12\t\n\x05VALUE\x10\x04\"y\n\rRangeResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\x1d\n\x03kvs\x18\x02 \x03(\x0b\x32\x10.mvccpb.KeyValue\x12\x0c\n\x04more\x18\x03 \x01(\x08\x12\r\n\x05\x63ount\x18\x04 \x01(\x03\"t\n\nPutRequest\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\r\n\x05lease\x18\x03 \x01(\x03\x12\x0f\n\x07prev_kv\x18\x04 \x01(\x08\x12\x14\n\x0cignore_value\x18\x05 \x01(\x08\x12\x14\n\x0cignore_lease\x18\x06 \x01(\x08\"^\n\x0bPutResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12!\n\x07prev_kv\x18\x02 \x01(\x0b\x32\x10.mvccpb.KeyValue\"E\n\x12\x44\x65leteRangeRequest\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\x11\n\trange_end\x18\x02 \x01(\x0c\x12\x0f\n\x07prev_kv\x18\x03 \x01(\x08\"x\n\x13\x44\x65leteRangeResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\x0f\n\x07\x64\x65leted\x18\x02 \x01(\x03\x12\"\n\x08prev_kvs\x18\x03 \x03(\x0b\x32\x10.mvccpb.KeyValue\"\xef\x01\n\tRequestOp\x12\x33\n\rrequest_range\x18\x01 \x01(\x0b\x32\x1a.etcdserverpb.RangeRequestH\x00\x12/\n\x0brequest_put\x18\x02 \x01(\x0b\x32\x18.etcdserverpb.PutRequestH\x00\x12@\n\x14request_delete_range\x18\x03 \x01(\x0b\x32 .etcdserverpb.DeleteRangeRequestH\x00\x12/\n\x0brequest_txn\x18\x04 \x01(\x0b\x32\x18.etcdserverpb.TxnRequestH\x00\x42\t\n\x07request\"\xf9\x01\n\nResponseOp\x12\x35\n\x0eresponse_range\x18\x01 \x01(\x0b\x32\x1b.etcdserverpb.RangeResponseH\x00\x12\x31\n\x0cresponse_put\x18\x02 \x01(\x0b\x32\x19.etcdserverpb.PutResponseH\x00\x12\x42\n\x15response_delete_range\x18\x03 \x01(\x0b\x32!.etcdserverpb.DeleteRangeResponseH\x00\x12\x31\n\x0cresponse_txn\x18\x04 \x01(\x0b\x32\x19.etcdserverpb.TxnResponseH\x00\x42\n\n\x08response\"\xfa\x02\n\x07\x43ompare\x12\x33\n\x06result\x18\x01 \x01(\x0e\x32#.etcdserverpb.Compare.CompareResult\x12\x33\n\x06target\x18\x02 \x01(\x0e\x32#.etcdserverpb.Compare.CompareTarget\x12\x0b\n\x03key\x18\x03 \x01(\x0c\x12\x11\n\x07version\x18\x04 \x01(\x03H\x00\x12\x19\n\x0f\x63reate_revision\x18\x05 \x01(\x03H\x00\x12\x16\n\x0cmod_revision\x18\x06 \x01(\x03H\x00\x12\x0f\n\x05value\x18\x07 \x01(\x0cH\x00\x12\x11\n\trange_end\x18@ \x01(\x0c\"@\n\rCompareResult\x12\t\n\x05\x45QUAL\x10\x00\x12\x0b\n\x07GREATER\x10\x01\x12\x08\n\x04LESS\x10\x02\x12\r\n\tNOT_EQUAL\x10\x03\"<\n\rCompareTarget\x12\x0b\n\x07VERSION\x10\x00\x12\n\n\x06\x43REATE\x10\x01\x12\x07\n\x03MOD\x10\x02\x12\t\n\x05VALUE\x10\x03\x42\x0e\n\x0ctarget_union\"\x88\x01\n\nTxnRequest\x12&\n\x07\x63ompare\x18\x01 \x03(\x0b\x32\x15.etcdserverpb.Compare\x12(\n\x07success\x18\x02 \x03(\x0b\x32\x17.etcdserverpb.RequestOp\x12(\n\x07\x66\x61ilure\x18\x03 \x03(\x0b\x32\x17.etcdserverpb.RequestOp\"{\n\x0bTxnResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\x11\n\tsucceeded\x18\x02 \x01(\x08\x12+\n\tresponses\x18\x03 \x03(\x0b\x32\x18.etcdserverpb.ResponseOp\"7\n\x11\x43ompactionRequest\x12\x10\n\x08revision\x18\x01 \x01(\x03\x12\x10\n\x08physical\x18\x02 \x01(\x08\"B\n\x12\x43ompactionResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"\r\n\x0bHashRequest\"J\n\x0cHashResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\x0c\n\x04hash\x18\x02 \x01(\r\"!\n\rHashKVRequest\x12\x10\n\x08revision\x18\x01 \x01(\x03\"f\n\x0eHashKVResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\x0c\n\x04hash\x18\x02 \x01(\r\x12\x18\n\x10\x63ompact_revision\x18\x03 \x01(\x03\"\x11\n\x0fSnapshotRequest\"g\n\x10SnapshotResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\x17\n\x0fremaining_bytes\x18\x02 \x01(\x04\x12\x0c\n\x04\x62lob\x18\x03 \x01(\x0c\"\xd7\x01\n\x0cWatchRequest\x12:\n\x0e\x63reate_request\x18\x01 \x01(\x0b\x32 .etcdserverpb.WatchCreateRequestH\x00\x12:\n\x0e\x63\x61ncel_request\x18\x02 \x01(\x0b\x32 .etcdserverpb.WatchCancelRequestH\x00\x12>\n\x10progress_request\x18\x03 \x01(\x0b\x32\".etcdserverpb.WatchProgressRequestH\x00\x42\x0f\n\rrequest_union\"\xdb\x01\n\x12WatchCreateRequest\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\x11\n\trange_end\x18\x02 \x01(\x0c\x12\x16\n\x0estart_revision\x18\x03 \x01(\x03\x12\x17\n\x0fprogress_notify\x18\x04 \x01(\x08\x12<\n\x07\x66ilters\x18\x05 \x03(\x0e\x32+.etcdserverpb.WatchCreateRequest.FilterType\x12\x0f\n\x07prev_kv\x18\x06 \x01(\x08\"%\n\nFilterType\x12\t\n\x05NOPUT\x10\x00\x12\x0c\n\x08NODELETE\x10\x01\"&\n\x12WatchCancelRequest\x12\x10\n\x08watch_id\x18\x01 \x01(\x03\"\x16\n\x14WatchProgressRequest\"\xc2\x01\n\rWatchResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\x10\n\x08watch_id\x18\x02 \x01(\x03\x12\x0f\n\x07\x63reated\x18\x03 \x01(\x08\x12\x10\n\x08\x63\x61nceled\x18\x04 \x01(\x08\x12\x18\n\x10\x63ompact_revision\x18\x05 \x01(\x03\x12\x15\n\rcancel_reason\x18\x06 \x01(\t\x12\x1d\n\x06\x65vents\x18\x0b \x03(\x0b\x32\r.mvccpb.Event\",\n\x11LeaseGrantRequest\x12\x0b\n\x03TTL\x18\x01 \x01(\x03\x12\n\n\x02ID\x18\x02 \x01(\x03\"j\n\x12LeaseGrantResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\n\n\x02ID\x18\x02 \x01(\x03\x12\x0b\n\x03TTL\x18\x03 \x01(\x03\x12\r\n\x05\x65rror\x18\x04 \x01(\t\" \n\x12LeaseRevokeRequest\x12\n\n\x02ID\x18\x01 \x01(\x03\"C\n\x13LeaseRevokeResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"#\n\x15LeaseKeepAliveRequest\x12\n\n\x02ID\x18\x01 \x01(\x03\"_\n\x16LeaseKeepAliveResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\n\n\x02ID\x18\x02 \x01(\x03\x12\x0b\n\x03TTL\x18\x03 \x01(\x03\"2\n\x16LeaseTimeToLiveRequest\x12\n\n\x02ID\x18\x01 \x01(\x03\x12\x0c\n\x04keys\x18\x02 \x01(\x08\"\x82\x01\n\x17LeaseTimeToLiveResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\n\n\x02ID\x18\x02 \x01(\x03\x12\x0b\n\x03TTL\x18\x03 \x01(\x03\x12\x12\n\ngrantedTTL\x18\x04 \x01(\x03\x12\x0c\n\x04keys\x18\x05 \x03(\x0c\"[\n\x06Member\x12\n\n\x02ID\x18\x01 \x01(\x04\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08peerURLs\x18\x03 \x03(\t\x12\x12\n\nclientURLs\x18\x04 \x03(\t\x12\x11\n\tisLearner\x18\x05 \x01(\x08\"7\n\x10MemberAddRequest\x12\x10\n\x08peerURLs\x18\x01 \x03(\t\x12\x11\n\tisLearner\x18\x02 \x01(\x08\"\x8e\x01\n\x11MemberAddResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12$\n\x06member\x18\x02 \x01(\x0b\x32\x14.etcdserverpb.Member\x12%\n\x07members\x18\x03 \x03(\x0b\x32\x14.etcdserverpb.Member\"!\n\x13MemberRemoveRequest\x12\n\n\x02ID\x18\x01 \x01(\x04\"k\n\x14MemberRemoveResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12%\n\x07members\x18\x02 \x03(\x0b\x32\x14.etcdserverpb.Member\"3\n\x13MemberUpdateRequest\x12\n\n\x02ID\x18\x01 \x01(\x04\x12\x10\n\x08peerURLs\x18\x02 \x03(\t\"k\n\x14MemberUpdateResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12%\n\x07members\x18\x02 \x03(\x0b\x32\x14.etcdserverpb.Member\"\x13\n\x11MemberListRequest\"i\n\x12MemberListResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12%\n\x07members\x18\x02 \x03(\x0b\x32\x14.etcdserverpb.Member\"\x13\n\x11\x44\x65\x66ragmentRequest\"B\n\x12\x44\x65\x66ragmentResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"%\n\x11MoveLeaderRequest\x12\x10\n\x08targetID\x18\x01 \x01(\x04\"B\n\x12MoveLeaderResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"\xb6\x01\n\x0c\x41larmRequest\x12\x36\n\x06\x61\x63tion\x18\x01 \x01(\x0e\x32&.etcdserverpb.AlarmRequest.AlarmAction\x12\x10\n\x08memberID\x18\x02 \x01(\x04\x12&\n\x05\x61larm\x18\x03 \x01(\x0e\x32\x17.etcdserverpb.AlarmType\"4\n\x0b\x41larmAction\x12\x07\n\x03GET\x10\x00\x12\x0c\n\x08\x41\x43TIVATE\x10\x01\x12\x0e\n\nDEACTIVATE\x10\x02\"G\n\x0b\x41larmMember\x12\x10\n\x08memberID\x18\x01 \x01(\x04\x12&\n\x05\x61larm\x18\x02 \x01(\x0e\x32\x17.etcdserverpb.AlarmType\"h\n\rAlarmResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12)\n\x06\x61larms\x18\x02 \x03(\x0b\x32\x19.etcdserverpb.AlarmMember\"\x0f\n\rStatusRequest\"\x94\x01\n\x0eStatusResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x0e\n\x06\x64\x62Size\x18\x03 \x01(\x03\x12\x0e\n\x06leader\x18\x04 \x01(\x04\x12\x11\n\traftIndex\x18\x05 \x01(\x04\x12\x10\n\x08raftTerm\x18\x06 \x01(\x04\"\x13\n\x11\x41uthEnableRequest\"\x14\n\x12\x41uthDisableRequest\"5\n\x13\x41uthenticateRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"4\n\x12\x41uthUserAddRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\"\n\x12\x41uthUserGetRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"%\n\x15\x41uthUserDeleteRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"?\n\x1d\x41uthUserChangePasswordRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"6\n\x18\x41uthUserGrantRoleRequest\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x0c\n\x04role\x18\x02 \x01(\t\"7\n\x19\x41uthUserRevokeRoleRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04role\x18\x02 \x01(\t\"\"\n\x12\x41uthRoleAddRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\"\n\x12\x41uthRoleGetRequest\x12\x0c\n\x04role\x18\x01 \x01(\t\"\x15\n\x13\x41uthUserListRequest\"\x15\n\x13\x41uthRoleListRequest\"%\n\x15\x41uthRoleDeleteRequest\x12\x0c\n\x04role\x18\x01 \x01(\t\"P\n\x1e\x41uthRoleGrantPermissionRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12 \n\x04perm\x18\x02 \x01(\x0b\x32\x12.authpb.Permission\"O\n\x1f\x41uthRoleRevokePermissionRequest\x12\x0c\n\x04role\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\x0c\x12\x11\n\trange_end\x18\x03 \x01(\x0c\"B\n\x12\x41uthEnableResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"C\n\x13\x41uthDisableResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"S\n\x14\x41uthenticateResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\r\n\x05token\x18\x02 \x01(\t\"C\n\x13\x41uthUserAddResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"R\n\x13\x41uthUserGetResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\r\n\x05roles\x18\x02 \x03(\t\"F\n\x16\x41uthUserDeleteResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"N\n\x1e\x41uthUserChangePasswordResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"I\n\x19\x41uthUserGrantRoleResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"J\n\x1a\x41uthUserRevokeRoleResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"C\n\x13\x41uthRoleAddResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"e\n\x13\x41uthRoleGetResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12 \n\x04perm\x18\x02 \x03(\x0b\x32\x12.authpb.Permission\"S\n\x14\x41uthRoleListResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\r\n\x05roles\x18\x02 \x03(\t\"S\n\x14\x41uthUserListResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\x12\r\n\x05users\x18\x02 \x03(\t\"F\n\x16\x41uthRoleDeleteResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"O\n\x1f\x41uthRoleGrantPermissionResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader\"P\n AuthRoleRevokePermissionResponse\x12,\n\x06header\x18\x01 \x01(\x0b\x32\x1c.etcdserverpb.ResponseHeader*\"\n\tAlarmType\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07NOSPACE\x10\x01\x32\xea\x02\n\x02KV\x12\x42\n\x05Range\x12\x1a.etcdserverpb.RangeRequest\x1a\x1b.etcdserverpb.RangeResponse\"\x00\x12<\n\x03Put\x12\x18.etcdserverpb.PutRequest\x1a\x19.etcdserverpb.PutResponse\"\x00\x12T\n\x0b\x44\x65leteRange\x12 .etcdserverpb.DeleteRangeRequest\x1a!.etcdserverpb.DeleteRangeResponse\"\x00\x12<\n\x03Txn\x12\x18.etcdserverpb.TxnRequest\x1a\x19.etcdserverpb.TxnResponse\"\x00\x12N\n\x07\x43ompact\x12\x1f.etcdserverpb.CompactionRequest\x1a .etcdserverpb.CompactionResponse\"\x00\x32\x9e\x01\n\x05Watch\x12M\n\x08Progress\x12\".etcdserverpb.WatchProgressRequest\x1a\x1b.etcdserverpb.WatchResponse\"\x00\x12\x46\n\x05Watch\x12\x1a.etcdserverpb.WatchRequest\x1a\x1b.etcdserverpb.WatchResponse\"\x00(\x01\x30\x01\x32\xf5\x02\n\x05Lease\x12Q\n\nLeaseGrant\x12\x1f.etcdserverpb.LeaseGrantRequest\x1a .etcdserverpb.LeaseGrantResponse\"\x00\x12T\n\x0bLeaseRevoke\x12 .etcdserverpb.LeaseRevokeRequest\x1a!.etcdserverpb.LeaseRevokeResponse\"\x00\x12\x61\n\x0eLeaseKeepAlive\x12#.etcdserverpb.LeaseKeepAliveRequest\x1a$.etcdserverpb.LeaseKeepAliveResponse\"\x00(\x01\x30\x01\x12`\n\x0fLeaseTimeToLive\x12$.etcdserverpb.LeaseTimeToLiveRequest\x1a%.etcdserverpb.LeaseTimeToLiveResponse\"\x00\x32\xde\x02\n\x07\x43luster\x12N\n\tMemberAdd\x12\x1e.etcdserverpb.MemberAddRequest\x1a\x1f.etcdserverpb.MemberAddResponse\"\x00\x12W\n\x0cMemberRemove\x12!.etcdserverpb.MemberRemoveRequest\x1a\".etcdserverpb.MemberRemoveResponse\"\x00\x12W\n\x0cMemberUpdate\x12!.etcdserverpb.MemberUpdateRequest\x1a\".etcdserverpb.MemberUpdateResponse\"\x00\x12Q\n\nMemberList\x12\x1f.etcdserverpb.MemberListRequest\x1a .etcdserverpb.MemberListResponse\"\x00\x32\x95\x04\n\x0bMaintenance\x12\x42\n\x05\x41larm\x12\x1a.etcdserverpb.AlarmRequest\x1a\x1b.etcdserverpb.AlarmResponse\"\x00\x12\x45\n\x06Status\x12\x1b.etcdserverpb.StatusRequest\x1a\x1c.etcdserverpb.StatusResponse\"\x00\x12Q\n\nDefragment\x12\x1f.etcdserverpb.DefragmentRequest\x1a .etcdserverpb.DefragmentResponse\"\x00\x12?\n\x04Hash\x12\x19.etcdserverpb.HashRequest\x1a\x1a.etcdserverpb.HashResponse\"\x00\x12\x45\n\x06HashKV\x12\x1b.etcdserverpb.HashKVRequest\x1a\x1c.etcdserverpb.HashKVResponse\"\x00\x12M\n\x08Snapshot\x12\x1d.etcdserverpb.SnapshotRequest\x1a\x1e.etcdserverpb.SnapshotResponse\"\x00\x30\x01\x12Q\n\nMoveLeader\x12\x1f.etcdserverpb.MoveLeaderRequest\x1a .etcdserverpb.MoveLeaderResponse\"\x00\x32\xdd\x0b\n\x04\x41uth\x12Q\n\nAuthEnable\x12\x1f.etcdserverpb.AuthEnableRequest\x1a .etcdserverpb.AuthEnableResponse\"\x00\x12T\n\x0b\x41uthDisable\x12 .etcdserverpb.AuthDisableRequest\x1a!.etcdserverpb.AuthDisableResponse\"\x00\x12W\n\x0c\x41uthenticate\x12!.etcdserverpb.AuthenticateRequest\x1a\".etcdserverpb.AuthenticateResponse\"\x00\x12P\n\x07UserAdd\x12 .etcdserverpb.AuthUserAddRequest\x1a!.etcdserverpb.AuthUserAddResponse\"\x00\x12P\n\x07UserGet\x12 .etcdserverpb.AuthUserGetRequest\x1a!.etcdserverpb.AuthUserGetResponse\"\x00\x12S\n\x08UserList\x12!.etcdserverpb.AuthUserListRequest\x1a\".etcdserverpb.AuthUserListResponse\"\x00\x12Y\n\nUserDelete\x12#.etcdserverpb.AuthUserDeleteRequest\x1a$.etcdserverpb.AuthUserDeleteResponse\"\x00\x12q\n\x12UserChangePassword\x12+.etcdserverpb.AuthUserChangePasswordRequest\x1a,.etcdserverpb.AuthUserChangePasswordResponse\"\x00\x12\x62\n\rUserGrantRole\x12&.etcdserverpb.AuthUserGrantRoleRequest\x1a\'.etcdserverpb.AuthUserGrantRoleResponse\"\x00\x12\x65\n\x0eUserRevokeRole\x12\'.etcdserverpb.AuthUserRevokeRoleRequest\x1a(.etcdserverpb.AuthUserRevokeRoleResponse\"\x00\x12P\n\x07RoleAdd\x12 .etcdserverpb.AuthRoleAddRequest\x1a!.etcdserverpb.AuthRoleAddResponse\"\x00\x12P\n\x07RoleGet\x12 .etcdserverpb.AuthRoleGetRequest\x1a!.etcdserverpb.AuthRoleGetResponse\"\x00\x12S\n\x08RoleList\x12!.etcdserverpb.AuthRoleListRequest\x1a\".etcdserverpb.AuthRoleListResponse\"\x00\x12Y\n\nRoleDelete\x12#.etcdserverpb.AuthRoleDeleteRequest\x1a$.etcdserverpb.AuthRoleDeleteResponse\"\x00\x12t\n\x13RoleGrantPermission\x12,.etcdserverpb.AuthRoleGrantPermissionRequest\x1a-.etcdserverpb.AuthRoleGrantPermissionResponse\"\x00\x12w\n\x14RoleRevokePermission\x12-.etcdserverpb.AuthRoleRevokePermissionRequest\x1a..etcdserverpb.AuthRoleRevokePermissionResponse\"\x00\x42)\n\x11io.etcd.jetcd.apiB\nJetcdProtoP\x01\xa2\x02\x05Jetcdb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'etcd3.etcdrpc.rpc_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\021io.etcd.jetcd.apiB\nJetcdProtoP\001\242\002\005Jetcd'
  _ALARMTYPE._serialized_start=7534
  _ALARMTYPE._serialized_end=7568
  _RESPONSEHEADER._serialized_start=91
  _RESPONSEHEADER._serialized_end=183
  _RANGEREQUEST._serialized_start=186
  _RANGEREQUEST._serialized_end=670
  _RANGEREQUEST_SORTORDER._serialized_start=556
  _RANGEREQUEST_SORTORDER._serialized_end=602
  _RANGEREQUEST_SORTTARGET._serialized_start=604
  _RANGEREQUEST_SORTTARGET._serialized_end=670
  _RANGERESPONSE._serialized_start=672
  _RANGERESPONSE._serialized_end=793
  _PUTREQUEST._serialized_start=795
  _PUTREQUEST._serialized_end=911
  _PUTRESPONSE._serialized_start=913
  _PUTRESPONSE._serialized_end=1007
  _DELETERANGEREQUEST._serialized_start=1009
  _DELETERANGEREQUEST._serialized_end=1078
  _DELETERANGERESPONSE._serialized_start=1080
  _DELETERANGERESPONSE._serialized_end=1200
  _REQUESTOP._serialized_start=1203
  _REQUESTOP._serialized_end=1442
  _RESPONSEOP._serialized_start=1445
  _RESPONSEOP._serialized_end=1694
  _COMPARE._serialized_start=1697
  _COMPARE._serialized_end=2075
  _COMPARE_COMPARERESULT._serialized_start=1933
  _COMPARE_COMPARERESULT._serialized_end=1997
  _COMPARE_COMPARETARGET._serialized_start=1999
  _COMPARE_COMPARETARGET._serialized_end=2059
  _TXNREQUEST._serialized_start=2078
  _TXNREQUEST._serialized_end=2214
  _TXNRESPONSE._serialized_start=2216
  _TXNRESPONSE._serialized_end=2339
  _COMPACTIONREQUEST._serialized_start=2341
  _COMPACTIONREQUEST._serialized_end=2396
  _COMPACTIONRESPONSE._serialized_start=2398
  _COMPACTIONRESPONSE._serialized_end=2464
  _HASHREQUEST._serialized_start=2466
  _HASHREQUEST._serialized_end=2479
  _HASHRESPONSE._serialized_start=2481
  _HASHRESPONSE._serialized_end=2555
  _HASHKVREQUEST._serialized_start=2557
  _HASHKVREQUEST._serialized_end=2590
  _HASHKVRESPONSE._serialized_start=2592
  _HASHKVRESPONSE._serialized_end=2694
  _SNAPSHOTREQUEST._serialized_start=2696
  _SNAPSHOTREQUEST._serialized_end=2713
  _SNAPSHOTRESPONSE._serialized_start=2715
  _SNAPSHOTRESPONSE._serialized_end=2818
  _WATCHREQUEST._serialized_start=2821
  _WATCHREQUEST._serialized_end=3036
  _WATCHCREATEREQUEST._serialized_start=3039
  _WATCHCREATEREQUEST._serialized_end=3258
  _WATCHCREATEREQUEST_FILTERTYPE._serialized_start=3221
  _WATCHCREATEREQUEST_FILTERTYPE._serialized_end=3258
  _WATCHCANCELREQUEST._serialized_start=3260
  _WATCHCANCELREQUEST._serialized_end=3298
  _WATCHPROGRESSREQUEST._serialized_start=3300
  _WATCHPROGRESSREQUEST._serialized_end=3322
  _WATCHRESPONSE._serialized_start=3325
  _WATCHRESPONSE._serialized_end=3519
  _LEASEGRANTREQUEST._serialized_start=3521
  _LEASEGRANTREQUEST._serialized_end=3565
  _LEASEGRANTRESPONSE._serialized_start=3567
  _LEASEGRANTRESPONSE._serialized_end=3673
  _LEASEREVOKEREQUEST._serialized_start=3675
  _LEASEREVOKEREQUEST._serialized_end=3707
  _LEASEREVOKERESPONSE._serialized_start=3709
  _LEASEREVOKERESPONSE._serialized_end=3776
  _LEASEKEEPALIVEREQUEST._serialized_start=3778
  _LEASEKEEPALIVEREQUEST._serialized_end=3813
  _LEASEKEEPALIVERESPONSE._serialized_start=3815
  _LEASEKEEPALIVERESPONSE._serialized_end=3910
  _LEASETIMETOLIVEREQUEST._serialized_start=3912
  _LEASETIMETOLIVEREQUEST._serialized_end=3962
  _LEASETIMETOLIVERESPONSE._serialized_start=3965
  _LEASETIMETOLIVERESPONSE._serialized_end=4095
  _MEMBER._serialized_start=4097
  _MEMBER._serialized_end=4188
  _MEMBERADDREQUEST._serialized_start=4190
  _MEMBERADDREQUEST._serialized_end=4245
  _MEMBERADDRESPONSE._serialized_start=4248
  _MEMBERADDRESPONSE._serialized_end=4390
  _MEMBERREMOVEREQUEST._serialized_start=4392
  _MEMBERREMOVEREQUEST._serialized_end=4425
  _MEMBERREMOVERESPONSE._serialized_start=4427
  _MEMBERREMOVERESPONSE._serialized_end=4534
  _MEMBERUPDATEREQUEST._serialized_start=4536
  _MEMBERUPDATEREQUEST._serialized_end=4587
  _MEMBERUPDATERESPONSE._serialized_start=4589
  _MEMBERUPDATERESPONSE._serialized_end=4696
  _MEMBERLISTREQUEST._serialized_start=4698
  _MEMBERLISTREQUEST._serialized_end=4717
  _MEMBERLISTRESPONSE._serialized_start=4719
  _MEMBERLISTRESPONSE._serialized_end=4824
  _DEFRAGMENTREQUEST._serialized_start=4826
  _DEFRAGMENTREQUEST._serialized_end=4845
  _DEFRAGMENTRESPONSE._serialized_start=4847
  _DEFRAGMENTRESPONSE._serialized_end=4913
  _MOVELEADERREQUEST._serialized_start=4915
  _MOVELEADERREQUEST._serialized_end=4952
  _MOVELEADERRESPONSE._serialized_start=4954
  _MOVELEADERRESPONSE._serialized_end=5020
  _ALARMREQUEST._serialized_start=5023
  _ALARMREQUEST._serialized_end=5205
  _ALARMREQUEST_ALARMACTION._serialized_start=5153
  _ALARMREQUEST_ALARMACTION._serialized_end=5205
  _ALARMMEMBER._serialized_start=5207
  _ALARMMEMBER._serialized_end=5278
  _ALARMRESPONSE._serialized_start=5280
  _ALARMRESPONSE._serialized_end=5384
  _STATUSREQUEST._serialized_start=5386
  _STATUSREQUEST._serialized_end=5401
  _STATUSRESPONSE._serialized_start=5404
  _STATUSRESPONSE._serialized_end=5552
  _AUTHENABLEREQUEST._serialized_start=5554
  _AUTHENABLEREQUEST._serialized_end=5573
  _AUTHDISABLEREQUEST._serialized_start=5575
  _AUTHDISABLEREQUEST._serialized_end=5595
  _AUTHENTICATEREQUEST._serialized_start=5597
  _AUTHENTICATEREQUEST._serialized_end=5650
  _AUTHUSERADDREQUEST._serialized_start=5652
  _AUTHUSERADDREQUEST._serialized_end=5704
  _AUTHUSERGETREQUEST._serialized_start=5706
  _AUTHUSERGETREQUEST._serialized_end=5740
  _AUTHUSERDELETEREQUEST._serialized_start=5742
  _AUTHUSERDELETEREQUEST._serialized_end=5779
  _AUTHUSERCHANGEPASSWORDREQUEST._serialized_start=5781
  _AUTHUSERCHANGEPASSWORDREQUEST._serialized_end=5844
  _AUTHUSERGRANTROLEREQUEST._serialized_start=5846
  _AUTHUSERGRANTROLEREQUEST._serialized_end=5900
  _AUTHUSERREVOKEROLEREQUEST._serialized_start=5902
  _AUTHUSERREVOKEROLEREQUEST._serialized_end=5957
  _AUTHROLEADDREQUEST._serialized_start=5959
  _AUTHROLEADDREQUEST._serialized_end=5993
  _AUTHROLEGETREQUEST._serialized_start=5995
  _AUTHROLEGETREQUEST._serialized_end=6029
  _AUTHUSERLISTREQUEST._serialized_start=6031
  _AUTHUSERLISTREQUEST._serialized_end=6052
  _AUTHROLELISTREQUEST._serialized_start=6054
  _AUTHROLELISTREQUEST._serialized_end=6075
  _AUTHROLEDELETEREQUEST._serialized_start=6077
  _AUTHROLEDELETEREQUEST._serialized_end=6114
  _AUTHROLEGRANTPERMISSIONREQUEST._serialized_start=6116
  _AUTHROLEGRANTPERMISSIONREQUEST._serialized_end=6196
  _AUTHROLEREVOKEPERMISSIONREQUEST._serialized_start=6198
  _AUTHROLEREVOKEPERMISSIONREQUEST._serialized_end=6277
  _AUTHENABLERESPONSE._serialized_start=6279
  _AUTHENABLERESPONSE._serialized_end=6345
  _AUTHDISABLERESPONSE._serialized_start=6347
  _AUTHDISABLERESPONSE._serialized_end=6414
  _AUTHENTICATERESPONSE._serialized_start=6416
  _AUTHENTICATERESPONSE._serialized_end=6499
  _AUTHUSERADDRESPONSE._serialized_start=6501
  _AUTHUSERADDRESPONSE._serialized_end=6568
  _AUTHUSERGETRESPONSE._serialized_start=6570
  _AUTHUSERGETRESPONSE._serialized_end=6652
  _AUTHUSERDELETERESPONSE._serialized_start=6654
  _AUTHUSERDELETERESPONSE._serialized_end=6724
  _AUTHUSERCHANGEPASSWORDRESPONSE._serialized_start=6726
  _AUTHUSERCHANGEPASSWORDRESPONSE._serialized_end=6804
  _AUTHUSERGRANTROLERESPONSE._serialized_start=6806
  _AUTHUSERGRANTROLERESPONSE._serialized_end=6879
  _AUTHUSERREVOKEROLERESPONSE._serialized_start=6881
  _AUTHUSERREVOKEROLERESPONSE._serialized_end=6955
  _AUTHROLEADDRESPONSE._serialized_start=6957
  _AUTHROLEADDRESPONSE._serialized_end=7024
  _AUTHROLEGETRESPONSE._serialized_start=7026
  _AUTHROLEGETRESPONSE._serialized_end=7127
  _AUTHROLELISTRESPONSE._serialized_start=7129
  _AUTHROLELISTRESPONSE._serialized_end=7212
  _AUTHUSERLISTRESPONSE._serialized_start=7214
  _AUTHUSERLISTRESPONSE._serialized_end=7297
  _AUTHROLEDELETERESPONSE._serialized_start=7299
  _AUTHROLEDELETERESPONSE._serialized_end=7369
  _AUTHROLEGRANTPERMISSIONRESPONSE._serialized_start=7371
  _AUTHROLEGRANTPERMISSIONRESPONSE._serialized_end=7450
  _AUTHROLEREVOKEPERMISSIONRESPONSE._serialized_start=7452
  _AUTHROLEREVOKEPERMISSIONRESPONSE._serialized_end=7532
  _KV._serialized_start=7571
  _KV._serialized_end=7933
  _WATCH._serialized_start=7936
  _WATCH._serialized_end=8094
  _LEASE._serialized_start=8097
  _LEASE._serialized_end=8470
  _CLUSTER._serialized_start=8473
  _CLUSTER._serialized_end=8823
  _MAINTENANCE._serialized_start=8826
  _MAINTENANCE._serialized_end=9359
  _AUTH._serialized_start=9362
  _AUTH._serialized_end=10863
# @@protoc_insertion_point(module_scope)
