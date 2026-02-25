from fastapi import FastAPI
from app.services.agora_service import AgoraService
from app.models import BaseApiResponse
import time

app = FastAPI(title="AfroDoctor Call Service")

# In-memory store: { call_id: { "start_time": timestamp, "status": "active" } }
active_calls = {}

@app.get("/")
def health_check():
    return {"status": "online", "service": "AfroDoctor Call API"}

@app.post("/calls/{call_id}/join", response_model=BaseApiResponse)
async def join_call(call_id: int):
    # For a real app, we'd check if the call_id exists in a DB.
    # Here, we just generate the token for any call_id provided.
    channel_name = f"channel_{call_id}"
    
    try:
        # Generate Agora details using our service
        agora_data = AgoraService.generate_rtc_token(channel_name)
        
        # Store call start time
        active_calls[call_id] = {"start_time": time.time(), "status": "joined"}
        
        return BaseApiResponse(
            success=True,
            message="Join details generated successfully",
            data={
                "token": agora_data["token"],
                "uid": agora_data["uid"],
                "appId": agora_data["appId"],
                "channelName": channel_name,
                "callType": "video"
            }
        )
    except Exception as e:
        return BaseApiResponse(success=False, message=str(e))

@app.post("/calls/{call_id}/end", response_model=BaseApiResponse)
async def end_call(call_id: int):
    if call_id in active_calls:
        start_time = active_calls[call_id]["start_time"]
        duration = time.time() - start_time
        del active_calls[call_id]
        
        print(f"Call {call_id} ended. Total duration: {duration:.2f} seconds.")
        return BaseApiResponse(success=True, message=f"Call ended. Duration: {int(duration)}s")
    
    return BaseApiResponse(success=False, message="Call session not found")

@app.post("/calls/{call_id}/reject", response_model=BaseApiResponse)
async def reject_call(call_id: int):
    if call_id in active_calls:
        del active_calls[call_id]
    
    return BaseApiResponse(success=True, message="Call rejected successfully")