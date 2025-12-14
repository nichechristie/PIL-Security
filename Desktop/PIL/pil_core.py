"""
Perceptual Intent Language (PIL) - Core Module
Validates and interprets perceptual data across multiple modalities

December 2025 - Complete perceptual AI system development
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class PerceptualDomain(Enum):
    """Supported perceptual domains"""
    SIGHT = "sight"
    SOUND = "sound"
    TOUCH = "touch"
    TASTE = "taste"
    SMELL = "smell"
    PROPRIOCEPTION = "proprioception"
    THERMOCEPTION = "thermoception"

@dataclass
class PerceptualData:
    """Container for perceptual information"""
    domain: PerceptualDomain
    data: Dict[str, Any]
    intent: Optional[str] = None
    confidence: float = 0.0
    timestamp: Optional[float] = None

@dataclass
class ValidationResult:
    """Result of perceptual validation"""
    is_valid: bool
    violations: List[str]
    suggestions: List[str]
    confidence_score: float

class PILValidator:
    """
    Core validator for perceptual intent language data
    """

    def __init__(self, policy_templates: Optional[Dict] = None):
        self.policy_templates = policy_templates or self._load_default_policies()
        self.validation_rules = self._initialize_validation_rules()

    def _load_default_policies(self) -> Dict:
        """Load default policy templates"""
        return {
            "accessibility": {
                "contrast_ratio": {"min": 4.5},
                "color_blind_safe": True,
                "audio_descriptions": True
            },
            "content_moderation": {
                "toxicity_threshold": 0.8,
                "inappropriate_content": False
            },
            "user_experience": {
                "cognitive_load": {"max": 7},
                "attention_span": {"max": 30}
            }
        }

    def _initialize_validation_rules(self) -> Dict[PerceptualDomain, List]:
        """Initialize validation rules for each domain"""
        return {
            PerceptualDomain.SIGHT: [
                self._validate_visual_contrast,
                self._validate_color_accessibility,
                self._validate_visual_complexity
            ],
            PerceptualDomain.SOUND: [
                self._validate_audio_levels,
                self._validate_audio_accessibility,
                self._validate_audio_content
            ],
            PerceptualDomain.TOUCH: [
                self._validate_haptic_feedback,
                self._validate_tactile_safety
            ],
            PerceptualDomain.TASTE: [],  # Placeholder
            PerceptualDomain.SMELL: [],  # Placeholder
        }

    def validate(self, perceptual_data: List[PerceptualData]) -> Tuple[List[PerceptualData], ValidationResult]:
        """
        Validate perceptual data against policies and rules

        Args:
            perceptual_data: List of perceptual data points

        Returns:
            Tuple of (validated_data, validation_report)
        """
        validated_data = []
        all_violations = []
        all_suggestions = []
        total_confidence = 0.0

        for data in perceptual_data:
            # Apply domain-specific validation rules
            violations, suggestions, confidence = self._apply_validation_rules(data)
            all_violations.extend(violations)
            all_suggestions.extend(suggestions)
            total_confidence += confidence

            # Update data confidence
            data.confidence = confidence
            validated_data.append(data)

        # Calculate overall confidence
        avg_confidence = total_confidence / len(perceptual_data) if perceptual_data else 0.0

        result = ValidationResult(
            is_valid=len(all_violations) == 0,
            violations=all_violations,
            suggestions=all_suggestions,
            confidence_score=avg_confidence
        )

        return validated_data, result

    def _apply_validation_rules(self, data: PerceptualData) -> Tuple[List[str], List[str], float]:
        """Apply validation rules for specific perceptual data"""
        violations = []
        suggestions = []
        confidence = 1.0

        if data.domain in self.validation_rules:
            for rule_func in self.validation_rules[data.domain]:
                rule_violations, rule_suggestions, rule_confidence = rule_func(data)
                violations.extend(rule_violations)
                suggestions.extend(rule_suggestions)
                confidence = min(confidence, rule_confidence)

        return violations, suggestions, confidence

    # Validation rule implementations
    def _validate_visual_contrast(self, data: PerceptualData) -> Tuple[List[str], List[str], float]:
        """Validate visual contrast ratios"""
        violations = []
        suggestions = []
        confidence = 1.0

        if "contrast_ratio" in data.data:
            ratio = data.data["contrast_ratio"]
            min_ratio = self.policy_templates["accessibility"]["contrast_ratio"]["min"]
            if ratio < min_ratio:
                violations.append(f"Contrast ratio {ratio} below minimum {min_ratio}")
                suggestions.append("Increase contrast between foreground and background colors")
                confidence = 0.7

        return violations, suggestions, confidence

    def _validate_color_accessibility(self, data: PerceptualData) -> Tuple[List[str], List[str], float]:
        """Validate color accessibility"""
        violations = []
        suggestions = []
        confidence = 1.0

        if self.policy_templates["accessibility"]["color_blind_safe"]:
            if "color_blind_safe" in data.data and not data.data["color_blind_safe"]:
                violations.append("Color scheme not accessible for color-blind users")
                suggestions.append("Use additional visual cues beyond color (shapes, patterns, labels)")
                confidence = 0.8

        return violations, suggestions, confidence

    def _validate_visual_complexity(self, data: PerceptualData) -> Tuple[List[str], List[str], float]:
        """Validate visual complexity against cognitive load limits"""
        violations = []
        suggestions = []
        confidence = 1.0

        if "complexity_score" in data.data:
            score = data.data["complexity_score"]
            max_load = self.policy_templates["user_experience"]["cognitive_load"]["max"]
            if score > max_load:
                violations.append(f"Visual complexity {score} exceeds cognitive load limit {max_load}")
                suggestions.append("Simplify visual elements or break into smaller chunks")
                confidence = 0.6

        return violations, suggestions, confidence

    def _validate_audio_levels(self, data: PerceptualData) -> Tuple[List[str], List[str], float]:
        """Validate audio levels"""
        violations = []
        suggestions = []
        confidence = 1.0

        if "volume_db" in data.data:
            volume = data.data["volume_db"]
            if volume > 85:  # Hearing damage threshold
                violations.append(f"Audio volume {volume}dB exceeds safe hearing levels")
                suggestions.append("Reduce audio volume or provide user controls")
                confidence = 0.5

        return violations, suggestions, confidence

    def _validate_audio_accessibility(self, data: PerceptualData) -> Tuple[List[str], List[str], float]:
        """Validate audio accessibility"""
        violations = []
        suggestions = []
        confidence = 1.0

        if self.policy_templates["accessibility"]["audio_descriptions"]:
            if "has_descriptions" in data.data and not data.data["has_descriptions"]:
                violations.append("Audio content missing descriptions for accessibility")
                suggestions.append("Add audio descriptions for visually impaired users")
                confidence = 0.9

        return violations, suggestions, confidence

    def _validate_audio_content(self, data: PerceptualData) -> Tuple[List[str], List[str], float]:
        """Validate audio content for appropriateness"""
        violations = []
        suggestions = []
        confidence = 1.0

        if "toxicity_score" in data.data:
            score = data.data["toxicity_score"]
            threshold = self.policy_templates["content_moderation"]["toxicity_threshold"]
            if score > threshold:
                violations.append(f"Audio content toxicity score {score} exceeds threshold {threshold}")
                suggestions.append("Review and moderate audio content")
                confidence = 0.4

        return violations, suggestions, confidence

    def _validate_haptic_feedback(self, data: PerceptualData) -> Tuple[List[str], List[str], float]:
        """Validate haptic feedback"""
        violations = []
        suggestions = []
        confidence = 1.0

        # Placeholder - implement haptic validation
        return violations, suggestions, confidence

    def _validate_tactile_safety(self, data: PerceptualData) -> Tuple[List[str], List[str], float]:
        """Validate tactile safety"""
        violations = []
        suggestions = []
        confidence = 1.0

        # Placeholder - implement tactile safety validation
        return violations, suggestions, confidence

class PILInterpreter:
    """
    AI-based interpretation layer for complex perceptual data
    """

    def __init__(self, ai_connector=None):
        self.ai_connector = ai_connector  # Would connect to Christie AI

    async def interpret_perceptual_data(self, pil_dict: Dict[str, Any]) -> str:
        """
        Interpret complex perceptual intent using AI

        Args:
            pil_dict: Dictionary containing perceptual data

        Returns:
            AI interpretation of perceptual intent
        """
        if self.ai_connector:
            # Real AI integration would go here
            interpretation = await self.ai_connector.analyze_perceptual_data(pil_dict)
            return interpretation
        else:
            # Fallback interpretation
            return f"Perceptual intent analysis: {json.dumps(pil_dict, indent=2)}"

def create_pil_dict(perceptual_data: List[PerceptualData]) -> Dict[str, Any]:
    """
    Convert perceptual data to PIL dictionary format

    Args:
        perceptual_data: List of PerceptualData objects

    Returns:
        PIL-formatted dictionary
    """
    pil_dict = {
        "version": "1.0",
        "timestamp": asyncio.get_event_loop().time(),
        "perceptual_domains": {}
    }

    for data in perceptual_data:
        domain_key = data.domain.value
        if domain_key not in pil_dict["perceptual_domains"]:
            pil_dict["perceptual_domains"][domain_key] = []

        pil_dict["perceptual_domains"][domain_key].append({
            "data": data.data,
            "intent": data.intent,
            "confidence": data.confidence,
            "timestamp": data.timestamp
        })

    return pil_dict

# Convenience functions for integration
def validate_perceptual_assets(assets: Dict[str, Any]) -> Tuple[Dict[str, Any], ValidationResult]:
    """
    Validate game assets using PIL

    Args:
        assets: Dictionary of game assets (lighting, audio, etc.)

    Returns:
        Tuple of (validated_assets, validation_report)
    """
    # Convert assets to perceptual data
    perceptual_data = []

    # Process visual assets
    if "lighting" in assets:
        perceptual_data.append(PerceptualData(
            domain=PerceptualDomain.SIGHT,
            data=assets["lighting"],
            intent="game_lighting"
        ))

    # Process audio assets
    if "audio" in assets:
        perceptual_data.append(PerceptualData(
            domain=PerceptualDomain.SOUND,
            data=assets["audio"],
            intent="game_audio"
        ))

    # Validate
    validator = PILValidator()
    validated_data, result = validator.validate(perceptual_data)

    # Convert back to asset format
    validated_assets = assets.copy()
    return validated_assets, result