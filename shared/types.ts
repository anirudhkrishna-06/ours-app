// Core Emotional Types
export interface EmotionalMemory {
  id: string;
  userId: string;
  partnerId: string;
  relationshipId: string;
  imageUrl?: string; // Change from string? to string | null
  caption: string;
  mood: EmotionalMood;
  category: MemoryCategory;
  timestamp: Date;
  emotionalScore: number;
  encrypted: boolean;
  encryptedData?: string;
  isShared: boolean;
}

export type EmotionalMood = 
  | 'joy' | 'gratitude' | 'love' | 'peace' 
  | 'sadness' | 'tension' | 'confusion' | 'excitement';

export type MemoryCategory = 
  | 'gratitude' | 'first' | 'everyday' | 'challenge' | 'growth';

// SET Avatar Emotional State
export interface SETState {
  userAvatar: AvatarState;
  partnerAvatar: AvatarState;
  connectionStrength: number; // 0-1
  emotionalHarmony: number; // 0-1
  lastSync: Date;
  colorAura: string;
}

export interface AvatarState {
  mood: EmotionalMood;
  energy: number; // 0-1
  lastActive: Date;
  recentMemories: number;
}

// Emotional Reflection
export interface EmotionalReflection {
  id: string;
  userId: string;
  prompt: string;
  response: string;
  sentiment: number;
  isShared: boolean;
  timestamp: Date;
}

// User Profile
export interface UserProfile {
  uid: string;
  email: string;
  displayName?: string;
  emotionalPreference: 'gentle' | 'balanced' | 'expressive';
  partnerId?: string;
  relationshipId?: string;
  createdAt: Date;
  lastLogin: Date;
  encryptionKey?: string;
}

// Relationship Types
export interface Relationship {
  id: string;
  partner1Id: string;
  partner2Id: string;
  partner1Name: string;
  partner2Name: string;
  partner1Email: string;
  partner2Email: string;
  status: 'active' | 'inactive' | 'pending';
  createdAt: Date;
  lastActive: Date;
  connectionStrength: number;
  emotionalHarmony: number;
  sharedMemoriesCount: number;
  relationshipKey: string; // Shared encryption key
}

// Update UserProfile to include relationshipId
export interface UserProfile {
  uid: string;
  email: string;
  displayName?: string;
  emotionalPreference: 'gentle' | 'balanced' | 'expressive';
  partnerId?: string;
  relationshipId?: string; // Add this line
  createdAt: Date;
  lastLogin: Date;
  encryptionKey?: string;
}

export interface Invitation {
  id: string;
  fromUserId: string;
  fromUserName: string;
  fromUserEmail: string;
  toEmail?: string;
  connectionCode: string;
  personalMessage: string;
  method: 'email' | 'code' | 'qr';
  status: 'sent' | 'delivered' | 'accepted' | 'declined' | 'expired';
  createdAt: Date;
  expiresAt: Date;
  acceptedAt?: Date | null;
  relationshipId?: string | null;
}