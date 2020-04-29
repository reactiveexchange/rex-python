# automatically generated by the FlatBuffers compiler, do not modify

# namespace: feed

import flatbuffers

class FeedRequest(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsFeedRequest(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FeedRequest()
        x.Init(buf, n + offset)
        return x

    # FeedRequest
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FeedRequest
    def ReqId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # FeedRequest
    def SubReqType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int16Flags, o + self._tab.Pos)
        return 1

    # FeedRequest
    def FeedType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int16Flags, o + self._tab.Pos)
        return 0

    # FeedRequest
    def Depth(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # FeedRequest
    def Grouping(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint16Flags, o + self._tab.Pos)
        return 0

    # FeedRequest
    def Frequency(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # FeedRequest
    def Markets(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.String(a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return ""

    # FeedRequest
    def MarketsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def FeedRequestStart(builder): builder.StartObject(7)
def FeedRequestAddReqId(builder, reqId): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(reqId), 0)
def FeedRequestAddSubReqType(builder, subReqType): builder.PrependInt16Slot(1, subReqType, 1)
def FeedRequestAddFeedType(builder, feedType): builder.PrependInt16Slot(2, feedType, 0)
def FeedRequestAddDepth(builder, depth): builder.PrependUint8Slot(3, depth, 0)
def FeedRequestAddGrouping(builder, grouping): builder.PrependUint16Slot(4, grouping, 0)
def FeedRequestAddFrequency(builder, frequency): builder.PrependInt32Slot(5, frequency, 0)
def FeedRequestAddMarkets(builder, markets): builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(markets), 0)
def FeedRequestStartMarketsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def FeedRequestEnd(builder): return builder.EndObject()
