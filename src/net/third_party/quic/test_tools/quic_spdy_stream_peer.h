// Copyright (c) 2019 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef NET_THIRD_PARTY_QUIC_TEST_TOOLS_QUIC_SPDY_STREAM_PEER_H_
#define NET_THIRD_PARTY_QUIC_TEST_TOOLS_QUIC_SPDY_STREAM_PEER_H_

#include "net/third_party/quic/core/quic_ack_listener_interface.h"
#include "net/third_party/quic/core/quic_interval_set.h"
#include "net/third_party/quic/platform/api/quic_containers.h"

namespace quic {

class QuicSpdyStream;

namespace test {

class QuicSpdyStreamPeer {
 public:
  static void set_ack_listener(
      QuicSpdyStream* stream,
      QuicReferenceCountedPointer<QuicAckListenerInterface> ack_listener);
  static const QuicIntervalSet<QuicStreamOffset>& unacked_frame_headers_offsets(
      QuicSpdyStream* stream);
};

}  // namespace test

}  // namespace quic

#endif  // NET_THIRD_PARTY_QUIC_TEST_TOOLS_QUIC_SPDY_STREAM_PEER_H_
