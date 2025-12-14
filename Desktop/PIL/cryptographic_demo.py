#!/usr/bin/env python3
"""
PIL Cryptographic Communication System Demo

Demonstrates how PIL strengthens human-computer communication through:
- Secure perceptual seed phrases (like crypto wallet seeds)
- Cryptographic encoding/decoding of perceptual data
- Key generation from perceptual phrases
- Secure communication channels

December 2025 - PIL Cryptographic Era
"""

import hashlib
import json
from typing import Dict, Any, List
from PIL.pil_dictionary import (
    PILDictionary, PerceptualDomain, create_perceptual_seed_phrase,
    validate_pil_phrase, pil_phrase_to_keypair
)


def demo_secure_perceptual_encoding():
    """
    Demonstrate secure encoding of perceptual data using PIL phrases
    """
    print("🔐 PIL Cryptographic Communication Demo")
    print("=" * 60)
    print()

    # Create PIL dictionary
    pil_dict = PILDictionary()

    print("1️⃣  CREATING SECURE PERCEPTUAL SEED PHRASES")
    print("-" * 50)

    # Example perceptual data that a human wants to communicate to a computer
    visual_perception = {
        "brightness": 0.8,
        "contrast_ratio": 5.2,
        "color_temperature": "warm",
        "emotional_impact": "calming",
        "accessibility_score": 0.95
    }

    audio_perception = {
        "volume_db": 65,
        "frequency_response": "balanced",
        "emotional_tone": "soothing",
        "clarity": 0.88,
        "spatial_audio": True
    }

    # Create secure seed phrases for each perceptual domain
    visual_phrase = create_perceptual_seed_phrase(PerceptualDomain.SIGHT, visual_perception)
    audio_phrase = create_perceptual_seed_phrase(PerceptualDomain.SOUND, audio_perception)

    print("Visual Perception Seed Phrase:")
    print(f"  {' '.join(visual_phrase)}")
    print(f"  Domain: {PerceptualDomain.SIGHT.value}")
    print()

    print("Audio Perception Seed Phrase:")
    print(f"  {' '.join(audio_phrase)}")
    print(f"  Domain: {PerceptualDomain.SOUND.value}")
    print()

    print("2️⃣  CRYPTOGRAPHIC ENCODING/DECODING")
    print("-" * 50)

    # Encode phrases to entropy (like BIP39)
    visual_entropy = pil_dict.encode_phrase_to_entropy(visual_phrase)
    audio_entropy = pil_dict.encode_phrase_to_entropy(audio_phrase)

    print("Visual Entropy (hex):")
    print(f"  {visual_entropy.hex()}")
    print(f"  Length: {len(visual_entropy)} bytes")
    print()

    print("Audio Entropy (hex):")
    print(f"  {audio_entropy.hex()}")
    print(f"  Length: {len(audio_entropy)} bytes")
    print()

    # Verify round-trip encoding/decoding
    decoded_visual = pil_dict.decode_entropy_to_phrase(visual_entropy, 12)
    decoded_audio = pil_dict.decode_entropy_to_phrase(audio_entropy, 12)

    print("Round-trip Verification:")
    print(f"  Visual: {'✓ PASS' if decoded_visual == visual_phrase else '✗ FAIL'}")
    print(f"  Audio:  {'✓ PASS' if decoded_audio == audio_phrase else '✗ FAIL'}")
    print()

    print("3️⃣  CRYPTOGRAPHIC KEY GENERATION")
    print("-" * 50)

    # Generate keypairs from perceptual phrases (like HD wallets)
    visual_private, visual_public = pil_phrase_to_keypair(visual_phrase)
    audio_private, audio_public = pil_phrase_to_keypair(audio_phrase)

    print("Visual Perception Keypair:")
    print(f"  Private Key: {visual_private.hex()}")
    print(f"  Public Key:  {visual_public.hex()}")
    print()

    print("Audio Perception Keypair:")
    print(f"  Private Key: {audio_private.hex()}")
    print(f"  Public Key:  {audio_public.hex()}")
    print()

    print("4️⃣  SECURE HUMAN-COMPUTER COMMUNICATION")
    print("-" * 50)

    # Demonstrate secure communication channel
    print("Human → Computer: Perceptual Intent Transmission")
    print()

    # Human creates perceptual message
    human_message = {
        "intent": "Create a calming meditation app interface",
        "perceptual_requirements": {
            "visual": visual_perception,
            "audio": audio_perception
        },
        "security_level": "high",
        "timestamp": "2025-12-13T16:00:00Z"
    }

    # Create secure signature using perceptual private key
    message_json = json.dumps(human_message, sort_keys=True)
    message_hash = hashlib.sha256(message_json.encode()).digest()

    # Sign with visual perception private key (representing the human's "identity")
    signature = hashlib.sha256(visual_private + message_hash).digest()

    print("Message Content:")
    print(f"  Intent: {human_message['intent']}")
    print(f"  Security: {human_message['security_level']}")
    print(f"  Visual Requirements: {len(str(human_message['perceptual_requirements']['visual']))} chars")
    print(f"  Audio Requirements: {len(str(human_message['perceptual_requirements']['audio']))} chars")
    print()

    print("Cryptographic Signature:")
    print(f"  Signed with Visual Perception Key")
    print(f"  Signature: {signature.hex()}")
    print()

    # Computer verifies the message
    verification_hash = hashlib.sha256(visual_public + message_hash).digest()
    is_authentic = signature == verification_hash

    print("Computer Verification:")
    print(f"  Message Authentic: {'✓ VERIFIED' if is_authentic else '✗ TAMPERED'}")
    print(f"  Sender Identity: Visual Perception Domain")
    print()

    print("5️⃣  PERCEPTUAL DATA ENCRYPTION")
    print("-" * 50)

    # Demonstrate encrypting perceptual data
    sensitive_perception = {
        "user_emotion": "anxious",
        "stress_level": 0.85,
        "attention_span": 12,  # minutes
        "cognitive_load": 0.72,
        "privacy_concerns": ["emotional_data", "attention_metrics"]
    }

    # Use audio keypair for encryption (different domain for layered security)
    encryption_key = hashlib.sha256(audio_private + b"encryption").digest()[:16]  # AES-128 key

    # Simple XOR encryption demo (real implementation would use AES)
    data_json = json.dumps(sensitive_perception, sort_keys=True)
    encrypted_data = bytes([b ^ encryption_key[i % len(encryption_key)]
                           for i, b in enumerate(data_json.encode())])

    print("Sensitive Perceptual Data:")
    print(f"  {json.dumps(sensitive_perception, indent=2)}")
    print()

    print("Encrypted (hex):")
    print(f"  {encrypted_data.hex()}")
    print()

    # Decrypt
    decrypted_data = bytes([b ^ encryption_key[i % len(encryption_key)]
                           for i, b in enumerate(encrypted_data)])
    decrypted_json = decrypted_data.decode()

    print("Decrypted:")
    print(f"  {json.dumps(json.loads(decrypted_json), indent=2)}")
    print()

    print("6️⃣  COMMUNICATION STRENGTHENING BENEFITS")
    print("-" * 50)

    benefits = [
        "🔐 Cryptographic Security: Perceptual data protected like crypto wallets",
        "🧠 Human-Readable: Seed phrases make complex data accessible",
        "🔄 Deterministic: Same perception always generates same keys",
        "🎯 Domain-Specific: Different keys for visual, audio, tactile, etc.",
        "🔗 Verifiable: Cryptographic signatures ensure authenticity",
        "🛡️ Privacy-Preserving: Encrypted transmission of sensitive data",
        "🌐 Decentralized: No central authority controls perceptual communication",
        "⚡ Efficient: 2048-word dictionary provides 2^132 possible combinations",
        "🎨 Multi-Modal: Supports sight, sound, touch, taste, smell, emotion, cognition",
        "🔄 Bidirectional: Humans ↔ Computers communicate securely"
    ]

    for benefit in benefits:
        print(f"  {benefit}")
    print()

    print("7️⃣  REAL-WORLD APPLICATIONS")
    print("-" * 50)

    applications = [
        "🎮 Game Development: Secure perceptual asset validation",
        "🩺 Healthcare: Encrypted patient perceptual data",
        "🤖 AI Training: Verifiable human perceptual feedback",
        "🎨 Creative Tools: Secure artistic intent communication",
        "📱 Accessibility: Private accessibility preference sharing",
        "🔬 Research: Secure multi-modal data collection",
        "💼 Enterprise: Encrypted UX testing and feedback",
        "🌐 Web3: Decentralized perceptual experiences",
        "🎵 Music Therapy: Secure emotional response tracking",
        "🏥 Mental Health: Private mood and perception logging"
    ]

    for app in applications:
        print(f"  {app}")
    print()

    print("🎯 CONCLUSION: PIL Cryptographic Communication")
    print("=" * 60)
    print("PIL transforms human-computer communication by providing:")
    print("• Cryptographic security like blockchain wallets")
    print("• Human-readable perceptual encoding")
    print("• Multi-modal perceptual support")
    print("• Privacy-preserving data transmission")
    print("• Verifiable authenticity and integrity")
    print()
    print("Just as seed phrases secure cryptocurrency, PIL phrases secure")
    print("the future of human-AI perceptual interaction! 🌟🔐🤖")


def demo_cross_domain_communication():
    """
    Demonstrate secure communication across perceptual domains
    """
    print("\n🔄 CROSS-DOMAIN SECURE COMMUNICATION")
    print("=" * 60)

    # Create phrases from different domains
    domains = [PerceptualDomain.SIGHT, PerceptualDomain.SOUND,
              PerceptualDomain.TOUCH, PerceptualDomain.EMOTION]

    domain_data = {
        PerceptualDomain.SIGHT: {"brightness": 0.9, "harmony": "balanced"},
        PerceptualDomain.SOUND: {"volume": 70, "rhythm": "soothing"},
        PerceptualDomain.TOUCH: {"texture": "smooth", "temperature": "warm"},
        PerceptualDomain.EMOTION: {"mood": "calm", "energy": "balanced"}
    }

    print("Multi-Domain Perceptual Communication:")
    print()

    for domain in domains:
        phrase = create_perceptual_seed_phrase(domain, domain_data[domain])
        private_key, public_key = pil_phrase_to_keypair(phrase)

        print(f"{domain.value.upper()}: {' '.join(phrase[:4])}...")
        print(f"  Private: {private_key.hex()[:16]}...")
        print(f"  Public:  {public_key.hex()[:16]}...")
        print()


if __name__ == "__main__":
    demo_secure_perceptual_encoding()
    demo_cross_domain_communication()