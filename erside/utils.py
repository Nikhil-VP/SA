from patient_data import calls_collection
from datetime import datetime

def check_for_call():
    """
    Check if there are any pending calls in the system
    Returns the call document if there's an incoming call, None otherwise
    """
    # Query the calls collection for any pending calls
    pending_call = calls_collection.find_one({
        "status": "pending",
        "scheduled_time": {
            "$lte": datetime.now()  # Only show calls that are scheduled for now or in the past
        }
    })
    
    return pending_call

def update_call_status(call_id, new_status):
    """
    Update the status of a call
    """
    calls_collection.update_one(
        {"_id": call_id},
        {"$set": {"status": new_status}}
    )

def schedule_call(patient_uhid, scheduled_time):
    """
    Schedule a new call
    """
    call_data = {
        "patient_uhid": patient_uhid,
        "scheduled_time": scheduled_time,
        "status": "pending",  # can be 'pending', 'active', 'completed', 'cancelled'
        "created_at": datetime.now()
    }
    calls_collection.insert_one(call_data)
