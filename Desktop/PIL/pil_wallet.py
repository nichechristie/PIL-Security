"""
PIL Wallet - Secure Perceptual Storage with Biometric Authentication

A cryptographic wallet system that uses PIL phrases combined with biometric
authentication (voice, retina scans) for secure access.

December 2025 - Multi-Modal Perceptual Security
"""

import hashlib
import hmac
import json
import secrets
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from PIL.pil_dictionary import PILDictionary, PerceptualDomain, pil_phrase_to_keypair


@dataclass
class BiometricProfile:
    """Biometric authentication profile"""
    voice_signature: Optional[bytes] = None
    retina_pattern: Optional[bytes] = None
    fingerprint_hash: Optional[bytes] = None
    facial_features: Optional[bytes] = None

    def get_auth_strength(self) -> int:
        """Get authentication strength based on available biometrics"""
        strength = 0
        if self.voice_signature:
            strength += 1
        if self.retina_pattern:
            strength += 2  # Retina is very secure
        if self.fingerprint_hash:
            strength += 1
        if self.facial_features:
            strength += 1
        return strength


@dataclass
class PILWallet:
    """
    PIL Wallet - Secure storage with perceptual authentication

    Uses PIL phrases + biometrics for multi-modal security
    """
    wallet_id: str
    pil_phrase: List[str]
    biometric_profile: BiometricProfile
    encrypted_data: Dict[str, bytes]
    access_log: List[Dict[str, Any]]

    def __init__(self, wallet_id: str, pil_phrase: List[str]):
        self.wallet_id = wallet_id
        self.pil_phrase = pil_phrase
        self.biometric_profile = BiometricProfile()
        self.encrypted_data = {}
        self.access_log = []

        # Generate wallet keys from PIL phrase
        self.private_key, self.public_key = pil_phrase_to_keypair(pil_phrase)

    def authenticate_voice(self, voice_sample: bytes) -> bool:
        """
        Authenticate using voice biometric

        Args:
            voice_sample: Raw voice audio data

        Returns:
            True if voice matches stored profile
        """
        if not self.biometric_profile.voice_signature:
            return False

        # Create voice signature from sample
        voice_hash = hashlib.sha256(voice_sample).digest()

        # Compare with stored signature (simplified - real implementation would use voice recognition)
        return hmac.compare_digest(voice_hash, self.biometric_profile.voice_signature)

    def authenticate_retina(self, retina_scan: bytes) -> bool:
        """
        Authenticate using retina biometric

        Args:
            retina_scan: Retina scan data

        Returns:
            True if retina matches stored pattern
        """
        if not self.biometric_profile.retina_pattern:
            return False

        # Hash retina scan for comparison
        retina_hash = hashlib.sha256(retina_scan).digest()

        # Compare patterns (simplified - real implementation would use iris recognition)
        return hmac.compare_digest(retina_hash, self.biometric_profile.retina_pattern)

    def authenticate_multi_modal(self, **auth_factors) -> Tuple[bool, str]:
        """
        Multi-modal authentication combining PIL + biometrics

        Args:
            auth_factors: Authentication factors (voice, retina, etc.)

        Returns:
            (success, reason)
        """
        # Always require PIL phrase
        pil_valid = self._verify_pil_phrase(auth_factors.get('pil_phrase'))
        if not pil_valid:
            return False, "Invalid PIL phrase"

        # Check biometric factors
        auth_strength = 0
        reasons = []

        if 'voice' in auth_factors:
            if self.authenticate_voice(auth_factors['voice']):
                auth_strength += 1
                reasons.append("voice verified")
            else:
                reasons.append("voice failed")

        if 'retina' in auth_factors:
            if self.authenticate_retina(auth_factors['retina']):
                auth_strength += 2  # Retina is high-security
                reasons.append("retina verified")
            else:
                reasons.append("retina failed")

        # Require minimum authentication strength
        min_strength = 1  # PIL phrase alone
        if self.biometric_profile.get_auth_strength() > 0:
            min_strength = 2  # Require at least one biometric

        if auth_strength >= min_strength:
            self._log_access("successful", reasons)
            return True, f"Authenticated ({', '.join(reasons)})"
        else:
            self._log_access("failed", reasons)
            return False, f"Insufficient authentication strength: {auth_strength}/{min_strength}"

    def _verify_pil_phrase(self, provided_phrase: Optional[List[str]]) -> bool:
        """Verify PIL phrase matches wallet"""
        if not provided_phrase:
            return False
        return provided_phrase == self.pil_phrase

    def _log_access(self, result: str, details: List[str]):
        """Log access attempt"""
        self.access_log.append({
            "timestamp": "2025-12-13T16:00:00Z",  # Would use real timestamp
            "result": result,
            "details": details,
            "wallet_id": self.wallet_id
        })

    def store_data(self, key: str, data: bytes, authenticated: bool = False) -> bool:
        """
        Store encrypted data in wallet

        Args:
            key: Data identifier
            data: Data to store
            authenticated: Whether user is authenticated

        Returns:
            True if stored successfully
        """
        if not authenticated:
            return False

        # Encrypt data with wallet key
        encrypted = self._encrypt_data(data)
        self.encrypted_data[key] = encrypted
        return True

    def retrieve_data(self, key: str, authenticated: bool = False) -> Optional[bytes]:
        """
        Retrieve decrypted data from wallet

        Args:
            key: Data identifier
            authenticated: Whether user is authenticated

        Returns:
            Decrypted data or None
        """
        if not authenticated or key not in self.encrypted_data:
            return None

        # Decrypt data
        return self._decrypt_data(self.encrypted_data[key])

    def _encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data with wallet key (simplified)"""
        # Use wallet private key for encryption (simplified - real implementation would use AES)
        key = self.private_key[:16]  # First 16 bytes for AES-128
        encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
        return encrypted

    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt data with wallet key"""
        return self._encrypt_data(encrypted_data)  # XOR is symmetric

    def enroll_biometric(self, biometric_type: str, biometric_data: bytes) -> bool:
        """
        Enroll biometric data for authentication

        Args:
            biometric_type: Type of biometric (voice, retina, etc.)
            biometric_data: Biometric sample data

        Returns:
            True if enrolled successfully
        """
        bio_hash = hashlib.sha256(biometric_data).digest()

        if biometric_type == "voice":
            self.biometric_profile.voice_signature = bio_hash
        elif biometric_type == "retina":
            self.biometric_profile.retina_pattern = bio_hash
        elif biometric_type == "fingerprint":
            self.biometric_profile.fingerprint_hash = bio_hash
        elif biometric_type == "face":
            self.biometric_profile.facial_features = bio_hash
        else:
            return False

        return True

    def get_security_status(self) -> Dict[str, Any]:
        """Get wallet security status"""
        return {
            "wallet_id": self.wallet_id,
            "pil_phrase_length": len(self.pil_phrase),
            "biometric_factors": self.biometric_profile.get_auth_strength(),
            "stored_items": len(self.encrypted_data),
            "last_access": self.access_log[-1] if self.access_log else None,
            "public_key": self.public_key.hex()[:16] + "..."
        }


class PILWalletManager:
    """
    Manager for PIL wallets with biometric authentication
    """

    def __init__(self):
        self.wallets: Dict[str, PILWallet] = {}
        self.pil_dict = PILDictionary()

    def create_wallet(self, perceptual_profile: Dict[str, Any]) -> PILWallet:
        """
        Create a new PIL wallet based on user's perceptual profile

        Args:
            perceptual_profile: User's perceptual characteristics

        Returns:
            New PIL wallet
        """
        # Generate personalized PIL phrase based on profile
        domain = PerceptualDomain.COGNITION  # Default to cognition for security
        pil_phrase = self.pil_dict.create_secure_perceptual_phrase(domain, perceptual_profile)

        # Create unique wallet ID
        wallet_id = hashlib.sha256(''.join(pil_phrase).encode()).hexdigest()[:16]

        wallet = PILWallet(wallet_id, pil_phrase)
        self.wallets[wallet_id] = wallet

        return wallet

    def authenticate_wallet_access(self, wallet_id: str, **auth_factors) -> Tuple[bool, str, Optional[PILWallet]]:
        """
        Authenticate access to a wallet using multi-modal factors

        Args:
            wallet_id: Wallet to access
            auth_factors: Authentication factors (pil_phrase, voice, retina, etc.)

        Returns:
            (success, message, wallet)
        """
        if wallet_id not in self.wallets:
            return False, "Wallet not found", None

        wallet = self.wallets[wallet_id]
        success, message = wallet.authenticate_multi_modal(**auth_factors)

        return success, message, wallet if success else None

    def biometric_wallet_access(self, wallet_id: str, voice_sample: Optional[bytes] = None,
                              retina_scan: Optional[bytes] = None) -> Tuple[bool, str]:
        """
        Access wallet using voice and/or retina biometrics

        Args:
            wallet_id: Wallet to access
            voice_sample: Voice audio data
            retina_scan: Retina scan data

        Returns:
            (success, message)
        """
        auth_factors = {}

        # Add voice authentication
        if voice_sample:
            auth_factors['voice'] = voice_sample

        # Add retina authentication
        if retina_scan:
            auth_factors['retina'] = retina_scan

        success, message, _ = self.authenticate_wallet_access(wallet_id, **auth_factors)
        return success, message

    def voice_retina_wallet_access(self, wallet_id: str, pil_phrase: List[str],
                                 voice_sample: bytes, retina_scan: bytes) -> Tuple[bool, str, Optional[PILWallet]]:
        """
        Full multi-modal authentication: PIL phrase + voice + retina

        Args:
            wallet_id: Wallet to access
            pil_phrase: PIL seed phrase
            voice_sample: Voice biometric
            retina_scan: Retina biometric

        Returns:
            (success, message, wallet)
        """
        auth_factors = {
            'pil_phrase': pil_phrase,
            'voice': voice_sample,
            'retina': retina_scan
        }

        return self.authenticate_wallet_access(wallet_id, **auth_factors)


# Global wallet manager
wallet_manager = PILWalletManager()


def create_perceptual_wallet(perceptual_profile: Dict[str, Any]) -> PILWallet:
    """
    Create a personalized PIL wallet based on perceptual profile

    Args:
        perceptual_profile: User's perceptual characteristics

    Returns:
        New PIL wallet
    """
    return wallet_manager.create_wallet(perceptual_profile)


def voice_access_wallet(wallet_id: str, voice_sample: bytes) -> Tuple[bool, str]:
    """
    Access wallet using voice authentication

    Args:
        wallet_id: Wallet ID
        voice_sample: Voice audio data

    Returns:
        (success, message)
    """
    return wallet_manager.biometric_wallet_access(wallet_id, voice_sample=voice_sample)


def retina_access_wallet(wallet_id: str, retina_scan: bytes) -> Tuple[bool, str]:
    """
    Access wallet using retina authentication

    Args:
        wallet_id: Wallet ID
        retina_scan: Retina scan data

    Returns:
        (success, message)
    """
    return wallet_manager.biometric_wallet_access(wallet_id, retina_scan=retina_scan)


def multi_modal_wallet_access(wallet_id: str, pil_phrase: List[str],
                            voice_sample: bytes, retina_scan: bytes) -> Tuple[bool, str, Optional[PILWallet]]:
    """
    Access wallet using full multi-modal authentication

    Args:
        wallet_id: Wallet ID
        pil_phrase: PIL seed phrase
        voice_sample: Voice biometric
        retina_scan: Retina biometric

    Returns:
        (success, message, wallet)
    """
    return wallet_manager.voice_retina_wallet_access(wallet_id, pil_phrase, voice_sample, retina_scan)