from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, Integer, Float, Boolean, Text, Date, Time
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from models import Base
from models.usage_history import UsageHistory



class Agent(Base):
    __tablename__ = 'agents'

    # Core Agent Fields
    agent_id = Column(String, primary_key=True) # Corresponds to the agent ID key in the JSON
    user_id = Column(String, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False, index=True) # Link to the User table

    # Agent Properties (mapped directly from JSON fields)
    ambientSoundVolume = Column(Integer, nullable=True)
    ambientSounds = Column(Integer, nullable=True)
    application_id = Column(String, nullable=True) # Redundant with id, but kept from JSON
    audioRecording = Column(Boolean, nullable=True)
    avatarUrl = Column(String, nullable=True)
    backchannelFrequency = Column(Float, nullable=True)
    backgroundDenoising = Column(Boolean, nullable=True)
    calls = Column(String, nullable=True) # Consider Integer if data is consistently numeric

    created_at = Column(DateTime, nullable=True)
    deleted = Column(Boolean, nullable=True)
    description = Column(Text, nullable=True)
    detectEmotion = Column(Boolean, nullable=True)
    hipaaCompliance = Column(Boolean, nullable=True)
    idleTimeout = Column(Float, nullable=True)
    initialMessage = Column(Text, nullable=True)
    interruptionThreshold = Column(Float, nullable=True)
    knowledgeBase = Column(String, nullable=True)
    language = Column(String, nullable=True)
    latency = Column(Integer, nullable=True)
    llmModel = Column(Integer, nullable=True)
    llmModelName = Column(String, nullable=True)
    llmProvider = Column(Integer, nullable=True)
    llmProviderName = Column(String, nullable=True)
    llmTemperature = Column(Float, nullable=True)
    logoUrl = Column(String, nullable=True)
    maxIdleMessages = Column(Integer, nullable=True)
    maxTokens = Column(Integer, nullable=True)
    maximumDuration = Column(Integer, nullable=True)
    minChars = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    responseDelay = Column(Integer, nullable=True)
    silenceTimeout = Column(Integer, nullable=True)
    speechNormalization = Column(Boolean, nullable=True)
    status = Column(String, nullable=True)
    sttModel = Column(Integer, nullable=True)
    sttProvider = Column(Integer, nullable=True)
    sttProviderName = Column(String, nullable=True)
    systemPrompt = Column(Text, nullable=True)
    totalCalls = Column(Integer, nullable=True)
    transcriptionModel = Column(String, nullable=True)
    ttsModel = Column(Integer, nullable=True)
    ttsProvider = Column(Integer, nullable=True)
    ttsProviderName = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    videoRecording = Column(Boolean, nullable=True)
    agentVoiceProvider = Column(String, nullable=True) # Renamed from voiceProvider to avoid conflict
    whoSpeaksFirst = Column(Integer, nullable=True)

    # Relationships
    user = relationship("User", back_populates="agents")
    call_logs = relationship("CallLog", back_populates="agent_profile", cascade="all, delete-orphan")
    system_prompt_history = relationship("SystemPromptHistory", back_populates="agent", cascade="all, delete-orphan")
    usage_histories = relationship('UsageHistory', back_populates='agent', foreign_keys=[UsageHistory.agent_id], cascade="all, delete-orphan")
    # One-to-one relationship with Voice
    voice = relationship("Voice", back_populates="agent", uselist=False, cascade="all, delete-orphan")
    # One-to-one relationship with VoiceCustomSettings
    voice_custom_settings = relationship("VoiceCustomSettings", back_populates="agent", uselist=False, cascade="all, delete-orphan")
    call_record = relationship('CallRecord', back_populates='agent', uselist=False)
    conversations = relationship('Conversation', back_populates='agent')



    def __repr__(self):
        return f"<Agent(id='{self.agent_id}', name='{self.name}')>"

# Voice Model (One-to-One with Agent)
class Voice(Base):
    __tablename__ = 'voices'

    # This 'id' corresponds to 'voice.id' or 'voice.voice_id' from the JSON
    voice_id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.agent_id', ondelete="CASCADE"), unique=True, nullable=False, index=True)

    accent = Column(String, nullable=True)
    age = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True) # voice.created_at
    gender = Column(String, nullable=True)
    name = Column(String, nullable=True) # voice.name
    provider = Column(String, nullable=True) # voice.provider

    # Relationship
    agent = relationship("Agent", back_populates="voice")

    def __repr__(self):
        return f"<Voice(id='{self.voice_id}', name='{self.name}', agent_id='{self.agent_id}')>"

# VoiceCustomSettings Model (One-to-One with Agent)
class VoiceCustomSettings(Base):
    __tablename__ = 'voice_custom_settings'

    # agent_id is both PK and FK to enforce 1-to-1 and ensure it's tied to an agent
    agent_id = Column(String, ForeignKey('agents.agent_id', ondelete="CASCADE"), primary_key=True)

    enabled = Column(Boolean, nullable=True)
    clarityAndSimilarity = Column(Float, nullable=True)
    pitch = Column(Float, nullable=True)
    similarity_boost = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    stability = Column(Float, nullable=True)
    style = Column(Float, nullable=True)
    styleExaggeration = Column(Float, nullable=True)
    useSpeakerBoost = Column(Boolean, nullable=True)

    # Relationship
    agent = relationship("Agent", back_populates="voice_custom_settings")

    def __repr__(self):
        return f"<VoiceCustomSettings(agent_id='{self.agent_id}', enabled='{self.enabled}')>"

# SystemPromptHistory Model (One-to-Many with Agent)
class SystemPromptHistory(Base):
    __tablename__ = 'system_prompt_history'

    prompt_id = Column(String, primary_key=True) # Corresponds to the UUID key in the history object
    agent_id = Column(String, ForeignKey('agents.agent_id', ondelete="CASCADE"), nullable=False, index=True)

    date = Column(Date, nullable=True)
    prompt = Column(Text, nullable=True)
    reason = Column(String, nullable=True)
    time = Column(Time, nullable=True)
    timestamp = Column(DateTime, nullable=True)

    # Relationship
    agent = relationship("Agent", back_populates="system_prompt_history")

    def __repr__(self):
        return f"<SystemPromptHistory(prompt_id='{self.prompt_id}', agent_id='{self.agent_id}', date='{self.date}')>"