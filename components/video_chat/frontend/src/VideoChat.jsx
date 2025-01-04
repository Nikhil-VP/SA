import React, { useEffect, useRef, useState } from 'react';
import {
  Streamlit,
  ComponentProps,
  withStreamlitConnection,
} from "streamlit-component-lib";

const ICE_SERVERS = {
  iceServers: [
    {
      urls: ['stun:stun1.l.google.com:19302', 'stun:stun2.l.google.com:19302'],
    },
  ],
};

const VideoChat = (props: ComponentProps) => {
  const localVideoRef = useRef<HTMLVideoElement>(null);
  const remoteVideoRef = useRef<HTMLVideoElement>(null);
  const peerConnectionRef = useRef<RTCPeerConnection | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const roomId = props.args.room_id;

  useEffect(() => {
    const initializeMedia = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true,
        });
        
        if (localVideoRef.current) {
          localVideoRef.current.srcObject = stream;
        }

        // Initialize WebSocket connection
        const ws = new WebSocket('wss://your-signaling-server.com');
        
        // Initialize peer connection
        peerConnectionRef.current = new RTCPeerConnection(ICE_SERVERS);
        
        // Add local tracks to peer connection
        stream.getTracks().forEach(track => {
          if (peerConnectionRef.current) {
            peerConnectionRef.current.addTrack(track, stream);
          }
        });

        // Handle incoming tracks
        peerConnectionRef.current.ontrack = (event) => {
          if (remoteVideoRef.current) {
            remoteVideoRef.current.srcObject = event.streams[0];
          }
        };

        // Handle ICE candidates
        peerConnectionRef.current.onicecandidate = (event) => {
          if (event.candidate) {
            ws.send(JSON.stringify({
              type: 'candidate',
              candidate: event.candidate,
              room: roomId,
            }));
          }
        };

        // WebSocket message handling
        ws.onmessage = async (event) => {
          const data = JSON.parse(event.data);
          
          if (data.type === 'offer' && peerConnectionRef.current) {
            await peerConnectionRef.current.setRemoteDescription(new RTCSessionDescription(data.offer));
            const answer = await peerConnectionRef.current.createAnswer();
            await peerConnectionRef.current.setLocalDescription(answer);
            
            ws.send(JSON.stringify({
              type: 'answer',
              answer: answer,
              room: roomId,
            }));
          }
          
          if (data.type === 'answer' && peerConnectionRef.current) {
            await peerConnectionRef.current.setRemoteDescription(new RTCSessionDescription(data.answer));
          }
          
          if (data.type === 'candidate' && peerConnectionRef.current) {
            await peerConnectionRef.current.addIceCandidate(new RTCIceCandidate(data.candidate));
          }
        };

      } catch (error) {
        console.error('Error accessing media devices:', error);
      }
    };

    initializeMedia();
    
    return () => {
      // Cleanup
      if (peerConnectionRef.current) {
        peerConnectionRef.current.close();
      }
    };
  }, [roomId]);

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div>
        <h3>Local Video</h3>
        <video
          ref={localVideoRef}
          autoPlay
          playsInline
          muted
          style={{ width: '400px', border: '1px solid #ccc' }}
        />
      </div>
      <div>
        <h3>Remote Video</h3>
        <video
          ref={remoteVideoRef}
          autoPlay
          playsInline
          style={{ width: '400px', border: '1px solid #ccc' }}
        />
      </div>
    </div>
  );
};

export default withStreamlitConnection(VideoChat); 