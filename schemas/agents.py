from pydantic import BaseModel, Field
from typing import Optional, Dict
import uuid

class VoiceSchema(BaseModel):
    name: str
    provider: str
    voice_id: str
    gender: str
    age: str
    accent: str
    created_at: str

class VoiceCustomSettingsSchema(BaseModel):
    clarityAndSimilarity: float
    enabled: bool
    pitch: float
    similarity_boost: float
    speed: float
    stability: float
    style: float
    styleExaggeration: float
    useSpeakerBoost: bool

class SystemPromptHistorySchema(BaseModel):
    date: str
    prompt: str
    reason: str
    time: str
    timestamp: str

class AgentSchema(BaseModel):
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    application_id: str
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str
    status: Optional[str]
    language: Optional[str]
    knowledgeBase: Optional[str]
    initialMessage: Optional[str]
    systemPrompt: Optional[str]
    avatarUrl: Optional[str]
    logoUrl: Optional[str]
    agentVoiceProvider: Optional[str]
    transcriptionModel: Optional[str]
    llmProvider: Optional[int]
    llmProviderName: Optional[str]
    llmModel: Optional[int]
    llmModelName: Optional[str]
    llmTemperature: Optional[float]
    sttProvider: Optional[int]
    sttProviderName: Optional[str]
    sttModel: Optional[int]
    ttsProvider: Optional[int]
    ttsProviderName: Optional[str]
    ttsModel: Optional[int]
    ambientSounds: Optional[int]
    ambientSoundVolume: Optional[float]
    backchannelFrequency: Optional[float]
    backgroundDenoising: Optional[bool]
    detectEmotion: Optional[bool]
    hipaaCompliance: Optional[bool]
    idleTimeout: Optional[float]
    interruptionThreshold: Optional[float]
    latency: Optional[int]
    maxIdleMessages: Optional[int]
    maxTokens: Optional[int]
    maximumDuration: Optional[int]
    minChars: Optional[int]
    responseDelay: Optional[int]
    silenceTimeout: Optional[int]
    speechNormalization: Optional[bool]
    whoSpeaksFirst: Optional[int]
    audioRecording: Optional[bool]
    videoRecording: Optional[bool]
    calls: Optional[str]
    totalCalls: Optional[int]
    
    voice: Optional[VoiceSchema]
    voiceCustomSettings: Optional[VoiceCustomSettingsSchema]
    systemPromptHistory: Optional[Dict[str, SystemPromptHistorySchema]]
