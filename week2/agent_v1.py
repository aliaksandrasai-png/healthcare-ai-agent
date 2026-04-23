"""
Healthcare Appointment Scheduling Agent v1.0
Day 10 — Full CRUD + Audit Logging + Conversation Memory
"""

# ============================================================
# 1. IMPORTS & SETUP
# ============================================================
from groq import Groq
from dotenv import load_dotenv
import sqlite3
import json
import os
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
conn = sqlite3.connect("scheduler.db")
cursor = conn.cursor()

# ============================================================
# 2. SYSTEM PROMPT
# ============================================================
SYSTEM_PROMPT = """You are an appointment scheduling assistant 
for a healthcare facility.

You are NOT a medical professional. You do not assess symptoms, 
diagnose, triage, or provide medical guidance of any kind.
Your help in medical situations = routing, not responding.

YOUR JOB:
- Help patients book, reschedule, or cancel appointments
- Use check_availability to find open slots
- Use book_slot to confirm appointments
- Use cancel_appointment to cancel bookings
- Collect: patient name, phone, insurance, preferred time
- If patient doesn't specify a department, ask their preference
- If patient doesn't know, suggest starting with Family Medicine

CRITICAL RULE:
- ALWAYS trust function results over your own reasoning
- If a function returns "Appointment cancelled" — it WAS cancelled
- If a function returns "Appointment confirmed" — it WAS confirmed
- Never contradict a function result based on conversation context
- Report function results accurately to the patient

MEDICAL BOUNDARIES:
- Do NOT assess, evaluate, or comment on symptoms
- Do NOT suggest specific medical specialties based on symptoms
- Do NOT echo or repeat patient's symptoms back to them
- Do NOT ask diagnostic or triage questions
- Do NOT explain medications, treatments, or procedures
- Do NOT make urgency judgments
- Do NOT assume patient's motives or intent

EMERGENCY PROTOCOL:
- If crisis language detected (harm, suicide, emergency):
  acknowledge briefly, direct to local emergency services,
  escalate to human staff, ask NO questions

TONE:
- Professional, warm, neutral
- No judgment of patient intent
- Treat every request with equal neutrality

CANNOT say:
- Unverified phone numbers, URLs, or addresses
- Unverified doctor names from patient 
  (use "your doctor" instead)
- Any assessment of symptoms or medical urgency

Today's date is 2026-04-27."""

# ============================================================
# 3. TOOLS DEFINITION
# ============================================================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check available appointment slots for a given date. Can filter by doctor name or department.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "doctor_name": {"type": "string", "description": "Doctor's name, e.g. Dr. Smith"},
                    "department": {"type": "string", "description": "Department name, e.g. Cardiology"}
                },
                "required": ["date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_slot",
            "description": "Book an appointment slot for a patient",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "time": {"type": "string", "description": "Time in HH:MM format"},
                    "doctor_name": {"type": "string", "description": "Doctor's name"},
                    "patient_name": {"type": "string", "description": "Patient's full name"},
                    "patient_phone": {"type": "string", "description": "Patient's phone number"},
                    "insurance": {"type": "string", "description": "Insurance provider name"}
                },
                "required": ["date", "time", "doctor_name", "patient_name", "patient_phone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_appointment",
            "description": "Cancel an existing appointment for a patient",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "time": {"type": "string", "description": "Time in HH:MM format"},
                    "doctor_name": {"type": "string", "description": "Doctor's name"},
                    "patient_name": {"type": "string", "description": "Patient's full name"}
                },
                "required": ["date", "time", "doctor_name", "patient_name"]
            }
        }
    }
]

# ============================================================
# 4. FUNCTIONS
# ============================================================
def check_availability(date, doctor_name=None, department=None):
    """Check available slots in the database"""
    if doctor_name in [None, "null", "unknown", ""]:
        doctor_name = None
    if department in [None, "null", "unknown", ""]:
        department = None

    if doctor_name:
        cursor.execute("""
            SELECT doctors.name, doctors.department, slots.time
            FROM slots JOIN doctors ON slots.doctor_id = doctors.id
            WHERE slots.date = ? AND doctors.name = ? AND slots.status = 'available'
            ORDER BY slots.time
        """, (date, doctor_name))
    elif department:
        cursor.execute("""
            SELECT doctors.name, doctors.department, slots.time
            FROM slots JOIN doctors ON slots.doctor_id = doctors.id
            WHERE slots.date = ? AND doctors.department = ? AND slots.status = 'available'
            ORDER BY doctors.name, slots.time
        """, (date, department))
    else:
        cursor.execute("""
            SELECT doctors.name, doctors.department, slots.time
            FROM slots JOIN doctors ON slots.doctor_id = doctors.id
            WHERE slots.date = ? AND slots.status = 'available'
            ORDER BY doctors.department, doctors.name, slots.time
        """, (date,))

    results = cursor.fetchall()
    if not results:
        return f"No available slots on {date}"

    output = f"Available slots on {date}:\n"
    for doctor, dept, time in results:
        output += f"  {time} — {doctor} ({dept})\n"
    return output


def book_slot(date, time, doctor_name, patient_name, patient_phone, insurance=None):
    """Book an appointment for a patient"""
    cursor.execute("""
        SELECT slots.id, slots.status
        FROM slots JOIN doctors ON slots.doctor_id = doctors.id
        WHERE slots.date = ? AND slots.time = ? AND doctors.name = ?
    """, (date, time, doctor_name))

    result = cursor.fetchone()
    if not result:
        return f"No slot found for {doctor_name} on {date} at {time}"
    if result[1] == 'booked':
        return f"Sorry, {doctor_name} at {time} on {date} is already booked"

    cursor.execute("""
        UPDATE slots
        SET patient_name = ?, patient_phone = ?,
            insurance = ?, status = 'booked'
        WHERE id = ?
    """, (patient_name, patient_phone, insurance, result[0]))

    conn.commit()
    return f"Appointment confirmed: {doctor_name} on {date} at {time} for {patient_name}"


def cancel_appointment(date, time, doctor_name, patient_name):
    """Cancel a patient's appointment"""
    cursor.execute("""
        SELECT slots.id, slots.status, slots.patient_name
        FROM slots JOIN doctors ON slots.doctor_id = doctors.id
        WHERE slots.date = ? AND slots.time = ?
        AND doctors.name = ? AND slots.status = 'booked'
    """, (date, time, doctor_name))

    result = cursor.fetchone()
    if not result:
        return f"No booking found for {doctor_name} on {date} at {time}"
    if result[2] != patient_name:
        return f"Patient name does not match the booking"

    cursor.execute("""
        UPDATE slots
        SET patient_name = NULL, patient_phone = NULL,
            insurance = NULL, appointment_type = 'primary',
            status = 'available'
        WHERE id = ?
    """, (result[0],))

    conn.commit()
    return f"Appointment cancelled: {doctor_name} on {date} at {time} for {patient_name}"


# Function dispatcher
FUNCTION_MAP = {
    "check_availability": check_availability,
    "book_slot": book_slot,
    "cancel_appointment": cancel_appointment,
}

# ============================================================
# 5a. AUDIT LOGGING
# ============================================================
def log_interaction(user_message, function_called, arguments, result, agent_response):
    """Log every interaction to audit file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"""
{'='*60}
TIMESTAMP: {timestamp}
USER: {user_message}
FUNCTION: {function_called}
ARGUMENTS: {arguments}
RESULT: {result}
AGENT RESPONSE: {agent_response}
{'='*60}
"""
    with open("audit.log", "a", encoding="utf-8") as f:
        f.write(log_entry)

# ============================================================
# 5b. OUTPUT VALIDATION
# ============================================================
def validate_response(function_result, agent_response):
    """Check if agent response contradicts function result"""
    
    contradictions = []
    
    if agent_response is None:
        return ["Agent response is None"]
    
    # Function says confirmed, but agent says not booked
    if "confirmed" in function_result.lower():
        if any(word in agent_response.lower() for word in 
               ["not available", "no slot", "unable to book", "couldn't book"]):
            contradictions.append(
                f"CONTRADICTION: Function confirmed booking, "
                f"but agent says otherwise"
            )
    
    # Function says cancelled, but agent says nothing to cancel
    if "cancelled" in function_result.lower():
        if any(word in agent_response.lower() for word in 
               ["no appointment to cancel", "nothing to cancel", 
                "no booking found", "was not successfully"]):
            contradictions.append(
                f"CONTRADICTION: Function cancelled appointment, "
                f"but agent denies it"
            )
    
    # Function says no slots, but agent promises availability
    if "no available slots" in function_result.lower():
        if any(word in agent_response.lower() for word in 
               ["available at", "opening at", "i've booked"]):
            contradictions.append(
                f"CONTRADICTION: No slots available, "
                f"but agent promises availability"
            )
    
    return contradictions

# ============================================================
# 6. MAIN AGENT FUNCTION
# ============================================================
def run_agent(user_message, conversation_history):
    """Process a patient message and return agent response"""

    conversation_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
        tools=TOOLS
    )

    message = response.choices[0].message

    # If model wants to call a function
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # Call the function
        func = FUNCTION_MAP.get(function_name)
        if func:
            try:
                result = func(**arguments)
            except Exception as e:
                result = f"Error calling {function_name}: {str(e)}"
        else:
            result = f"Unknown function: {function_name}"

        # Add function call and result to history
        conversation_history.append(message)
        conversation_history.append({
            "role": "tool",
            "content": result,
            "tool_call_id": tool_call.id
        })

        # Get final response
        try:
            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
                tools=TOOLS,
                tool_choice="none"
            )
            agent_response = final_response.choices[0].message.content
        except Exception:
            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
            )
            agent_response = final_response.choices[0].message.content

        # >>> VALIDATION: check for contradictions <<<
        contradictions = validate_response(result, agent_response or "")
        if contradictions:
            for c in contradictions:
                print(f"⚠️  {c}")
            log_interaction(
                user_message,
                f"CONTRADICTION_DETECTED in {function_name}",
                arguments, result,
                f"{agent_response} ||| CONTRADICTIONS: {contradictions}"
            )
        else:
            log_interaction(user_message, function_name, arguments, result, agent_response)

        conversation_history.append({"role": "assistant", "content": agent_response})

        return agent_response

    # If model responds without function call
    else:
        agent_response = message.content
        conversation_history.append({"role": "assistant", "content": agent_response})

        log_interaction(user_message, "none", {}, "N/A", agent_response)

        return agent_response


# ============================================================
# 7. RUN
# ============================================================
if __name__ == "__main__":
    print("Healthcare Scheduling Agent v1.0")
    print("Type 'quit' to exit\n")

    conversation_history = []

    while True:
        user_input = input("Patient: ")
        if user_input.lower() == 'quit':
            break

        response = run_agent(user_input, conversation_history)
        print(f"\nAgent: {response}\n")

    conn.close()
    print("Session ended.")