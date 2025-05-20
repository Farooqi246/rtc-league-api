from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.agents import Agent, Voice, VoiceCustomSettings, SystemPromptHistory  # SQLAlchemy models
from schemas.agents import AgentSchema  # Pydantic models you'll define below
from schemas.agents import VoiceSchema, VoiceCustomSettingsSchema, SystemPromptHistorySchema
import uuid

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_agent(agent_data: AgentSchema, db: Session = Depends(get_db)):
    try:
        # 1️⃣ Insert Agent
        agent = Agent(**agent_data.dict(exclude={"voice", "voiceCustomSettings", "systemPromptHistory"}))
        db.add(agent)

        # 2️⃣ Insert Voice
        if agent_data.voice:
            voice = Voice(**agent_data.voice.dict(), agent_id=agent.agent_id)
            db.add(voice)

        # 3️⃣ Insert VoiceCustomSettings
        if agent_data.voiceCustomSettings:
            vcs = VoiceCustomSettings(**agent_data.voiceCustomSettings.dict(), agent_id=agent.agent_id)
            db.add(vcs)

        # 4️⃣ Insert SystemPromptHistory (many entries)
        if agent_data.systemPromptHistory:
            for sph_data in agent_data.systemPromptHistory.values():
                sph = SystemPromptHistory(
                    prompt_id=str(uuid.uuid4()),   # ✅ Generate UUID for PK
                    agent_id=agent.agent_id,
                    **sph_data.dict()
                )
                db.add(sph)

        db.commit()
        db.refresh(agent)
        return {"message": "Agent created successfully", "agent_id": agent.agent_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/{agent_id}")
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    voice = db.query(Voice).filter(Voice.agent_id == agent_id).first()
    vcs = db.query(VoiceCustomSettings).filter(VoiceCustomSettings.agent_id == agent_id).first()
    sph_list = db.query(SystemPromptHistory).filter(SystemPromptHistory.agent_id == agent_id).all()

    return {
        "agent": agent,
        "voice": voice,
        "voiceCustomSettings": vcs,
        "systemPromptHistory": {sph.prompt_id: sph for sph in sph_list}
    }

@router.put("/{agent_id}")
def update_agent(agent_id: str, agent_data: AgentSchema, db: Session = Depends(get_db)):
    try:
        # Find the agent
        agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Do not update agent_id, update other fields
        update_data = agent_data.dict(exclude_unset=True, exclude={"agent_id", "voice", "voiceCustomSettings", "systemPromptHistory"})
        for key, value in update_data.items():
            setattr(agent, key, value)

        db.commit()
        db.refresh(agent)
        return {"message": "Agent updated successfully", "agent_id": agent.agent_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the agent: {str(e)}")



@router.delete("/{agent_id}")
def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        # Delete related entries first
        db.query(SystemPromptHistory).filter(SystemPromptHistory.agent_id == agent_id).delete()
        db.query(VoiceCustomSettings).filter(VoiceCustomSettings.agent_id == agent_id).delete()
        db.query(Voice).filter(Voice.agent_id == agent_id).delete()

        # Delete Agent
        db.delete(agent)

        db.commit()
        return {"message": "Agent deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

#============================= 🔽 Voice CRUD ==============================

@router.put("/{agent_id}/voice")
def update_voice(agent_id: str, voice_data: VoiceSchema, db: Session = Depends(get_db)):
    voice = db.query(Voice).filter(Voice.agent_id == agent_id).first()
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")

    for key, value in voice_data.dict().items():
        setattr(voice, key, value)

    db.commit()
    db.refresh(voice)
    return {"message": "Voice updated successfully", "voice": voice}

# 🔽 Get Voice
@router.get("/{agent_id}/voice")
def get_voice(agent_id: str, db: Session = Depends(get_db)):
    voice = db.query(Voice).filter(Voice.agent_id == agent_id).first()
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    return voice

# 🔽 Delete Voice
@router.delete("/{agent_id}/voice")
def delete_voice(agent_id: str, db: Session = Depends(get_db)):
    voice = db.query(Voice).filter(Voice.agent_id == agent_id).first()
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")

    db.delete(voice)
    db.commit()
    return {"message": "Voice deleted successfully"}


#============================= 🔽 VoiceCustomSettings CRUD ==============================


# 🔽 Update VoiceCustomSettings
@router.put("/{agent_id}/voice-custom-settings")
def update_voice_custom_settings(agent_id: str, vcs_data: VoiceCustomSettingsSchema, db: Session = Depends(get_db)):
    vcs = db.query(VoiceCustomSettings).filter(VoiceCustomSettings.agent_id == agent_id).first()
    if not vcs:
        raise HTTPException(status_code=404, detail="VoiceCustomSettings not found")

    for key, value in vcs_data.dict().items():
        setattr(vcs, key, value)

    db.commit()
    db.refresh(vcs)
    return {"message": "VoiceCustomSettings updated successfully", "voiceCustomSettings": vcs}

# 🔽 Get VoiceCustomSettings
@router.get("/{agent_id}/voice-custom-settings")
def get_voice_custom_settings(agent_id: str, db: Session = Depends(get_db)):
    vcs = db.query(VoiceCustomSettings).filter(VoiceCustomSettings.agent_id == agent_id).first()
    if not vcs:
        raise HTTPException(status_code=404, detail="VoiceCustomSettings not found")
    return vcs

# 🔽 Delete VoiceCustomSettings
@router.delete("/{agent_id}/voice-custom-settings")
def delete_voice_custom_settings(agent_id: str, db: Session = Depends(get_db)):
    vcs = db.query(VoiceCustomSettings).filter(VoiceCustomSettings.agent_id == agent_id).first()
    if not vcs:
        raise HTTPException(status_code=404, detail="VoiceCustomSettings not found")

    db.delete(vcs)
    db.commit()
    return {"message": "VoiceCustomSettings deleted successfully"}



#============================= 🔽 SystemPromptHistory CRUD ===============================

# 🔽 Update SystemPromptHistory by prompt_id
@router.put("/{agent_id}/prompt-history/{prompt_id}")
def update_system_prompt_history(agent_id: str, prompt_id: str, sph_data: SystemPromptHistorySchema, db: Session = Depends(get_db)):
    sph = db.query(SystemPromptHistory).filter(SystemPromptHistory.agent_id == agent_id, SystemPromptHistory.prompt_id == prompt_id).first()
    if not sph:
        raise HTTPException(status_code=404, detail="SystemPromptHistory not found")

    for key, value in sph_data.dict().items():
        setattr(sph, key, value)

    db.commit()
    db.refresh(sph)
    return {"message": "SystemPromptHistory updated successfully", "systemPromptHistory": sph}

# 🔽 Get All SystemPromptHistory for agent
@router.get("/{agent_id}/prompt-history")
def get_system_prompt_history(agent_id: str, db: Session = Depends(get_db)):
    sph_list = db.query(SystemPromptHistory).filter(SystemPromptHistory.agent_id == agent_id).all()
    if not sph_list:
        raise HTTPException(status_code=404, detail="No SystemPromptHistory found")
    return sph_list

# 🔽 Delete SystemPromptHistory by prompt_id
@router.delete("/{agent_id}/prompt-history/{prompt_id}")
def delete_system_prompt_history(agent_id: str, prompt_id: str, db: Session = Depends(get_db)):
    sph = db.query(SystemPromptHistory).filter(SystemPromptHistory.agent_id == agent_id, SystemPromptHistory.prompt_id == prompt_id).first()
    if not sph:
        raise HTTPException(status_code=404, detail="SystemPromptHistory not found")

    db.delete(sph)
    db.commit()
    return {"message": "SystemPromptHistory entry deleted successfully"}
