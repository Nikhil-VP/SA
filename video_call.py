import streamlit as st
import streamlit.components.v1 as components

def video_chat_component(room_id):
    # HTML/JavaScript for video chat
    component_html = """
    <div style="display: flex; gap: 20px;">
        <div>
            <h3>Local Video</h3>
            <video id="localVideo" autoplay playsinline muted style="width: 400px; border: 1px solid #ccc;"></video>
        </div>
        <div>
            <h3>Remote Video</h3>
            <video id="remoteVideo" autoplay playsinline style="width: 400px; border: 1px solid #ccc;"></video>
        </div>
    </div>

    <script>
    const localVideo = document.getElementById('localVideo');
    const remoteVideo = document.getElementById('remoteVideo');
    let localStream;
    let peerConnection;

    const configuration = {
        iceServers: [
            { urls: 'stun:stun.l.google.com:19302' }
        ]
    };

    async function startVideo() {
        try {
            localStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            localVideo.srcObject = localStream;

            // Create peer connection
            peerConnection = new RTCPeerConnection(configuration);

            // Add local stream to peer connection
            localStream.getTracks().forEach(track => {
                peerConnection.addTrack(track, localStream);
            });

            // Handle incoming tracks
            peerConnection.ontrack = event => {
                remoteVideo.srcObject = event.streams[0];
            };

            // Connect to signaling server
            const ws = new WebSocket('wss://your-signaling-server.com');
            
            // Handle ICE candidates
            peerConnection.onicecandidate = event => {
                if (event.candidate) {
                    ws.send(JSON.stringify({
                        type: 'candidate',
                        candidate: event.candidate,
                        room: '""" + room_id + """'
                    }));
                }
            };

            // WebSocket message handling
            ws.onmessage = async event => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'offer') {
                    await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
                    const answer = await peerConnection.createAnswer();
                    await peerConnection.setLocalDescription(answer);
                    
                    ws.send(JSON.stringify({
                        type: 'answer',
                        answer: answer,
                        room: '""" + room_id + """'
                    }));
                }
                
                if (data.type === 'answer') {
                    await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
                }
                
                if (data.type === 'candidate') {
                    await peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate));
                }
            };

        } catch (error) {
            console.error('Error accessing media devices:', error);
        }
    }

    // Start video when the component loads
    startVideo();
    </script>
    """
    
    # Render the component
    components.html(component_html, height=600)

def create_room():
    """Create a new room ID."""
    import uuid
    return str(uuid.uuid4()) 