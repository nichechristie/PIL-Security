#!/usr/bin/env python3
"""
PIL Example Usage
Demonstrates Perceptual Intent Language validation and interpretation

December 2025 - PIL Development Example
"""

import asyncio
from PIL.pil_core import (
    PILValidator, PerceptualData, PerceptualDomain,
    PILInterpreter, create_pil_dict, validate_perceptual_assets
)

def demo_basic_validation():
    """Demonstrate basic perceptual data validation"""
    print("=== Basic Perceptual Validation Demo ===\n")

    # Create sample perceptual data
    perceptual_data = [
        PerceptualData(
            domain=PerceptualDomain.SIGHT,
            data={
                "contrast_ratio": 3.2,  # Below WCAG AA standard (4.5)
                "color_blind_safe": False,
                "complexity_score": 6
            },
            intent="ui_design"
        ),
        PerceptualData(
            domain=PerceptualDomain.SOUND,
            data={
                "volume_db": 90,  # Above safe hearing levels
                "has_descriptions": False,
                "toxicity_score": 0.5
            },
            intent="notification_audio"
        ),
        PerceptualData(
            domain=PerceptualDomain.TOUCH,
            data={
                "vibration_intensity": 8,
                "safety_rating": "high"
            },
            intent="haptic_feedback"
        )
    ]

    # Validate data
    validator = PILValidator()
    validated_data, result = validator.validate(perceptual_data)

    # Display results
    print(f"Overall Validation: {'PASS' if result.is_valid else 'FAIL'}")
    print(f"Confidence Score: {result.confidence_score:.2f}\n")

    if result.violations:
        print("Violations Found:")
        for violation in result.violations:
            print(f"  - {violation}")

    if result.suggestions:
        print("\nSuggestions:")
        for suggestion in result.suggestions:
            print(f"  - {suggestion}")

    print("\nValidated Data:")
    for data in validated_data:
        print(f"  {data.domain.value}: confidence={data.confidence:.2f}")

def demo_game_asset_validation():
    """Demonstrate game asset validation"""
    print("\n=== Game Asset Validation Demo ===\n")

    # Sample game assets
    game_assets = {
        "lighting": {
            "contrast_ratio": 5.1,
            "complexity_score": 8,  # Above cognitive load limit
            "color_blind_safe": True
        },
        "audio": {
            "volume_db": 75,
            "has_descriptions": True,
            "toxicity_score": 0.3
        },
        "haptics": {
            "vibration_intensity": 7,
            "safety_rating": "medium"
        }
    }

    # Validate assets
    validated_assets, report = validate_perceptual_assets(game_assets)

    print(f"Asset Validation: {'PASS' if report.is_valid else 'FAIL'}")
    print(f"Confidence Score: {report.confidence_score:.2f}\n")

    if report.violations:
        print("Asset Violations:")
        for violation in report.violations:
            print(f"  - {violation}")

    if report.suggestions:
        print("\nImprovement Suggestions:")
        for suggestion in report.suggestions:
            print(f"  - {suggestion}")

async def demo_ai_interpretation():
    """Demonstrate AI interpretation of perceptual data"""
    print("\n=== AI Interpretation Demo ===\n")

    # Create complex perceptual data
    complex_data = [
        PerceptualData(
            domain=PerceptualDomain.SIGHT,
            data={"contrast_ratio": 7.2, "emotional_impact": "calming", "complexity_score": 3},
            intent="meditation_app_ui"
        ),
        PerceptualData(
            domain=PerceptualDomain.SOUND,
            data={"frequency_hz": 432, "rhythm": "slow", "toxicity_score": 0.1},
            intent="binaural_beats"
        ),
        PerceptualData(
            domain=PerceptualDomain.TOUCH,
            data={"pressure": "gentle", "temperature": "warm", "pattern": "rhythmic"},
            intent="stress_relief"
        )
    ]

    # Create PIL dictionary
    pil_dict = create_pil_dict(complex_data)
    print("PIL Dictionary Structure:")
    print(f"Version: {pil_dict['version']}")
    print(f"Domains: {list(pil_dict['perceptual_domains'].keys())}\n")

    # Interpret with AI
    interpreter = PILInterpreter()  # No AI connector, uses fallback
    interpretation = await interpreter.interpret_perceptual_data(pil_dict)

    print("AI Interpretation:")
    print(interpretation)

def demo_custom_policies():
    """Demonstrate custom policy templates"""
    print("\n=== Custom Policy Demo ===\n")

    # Custom strict accessibility policies
    custom_policies = {
        "accessibility": {
            "contrast_ratio": {"min": 7.0},  # Stricter than WCAG AAA
            "color_blind_safe": True,
            "audio_descriptions": True
        },
        "content_moderation": {
            "toxicity_threshold": 0.5,  # Stricter moderation
            "inappropriate_content": False
        },
        "user_experience": {
            "cognitive_load": {"max": 5},  # Lower cognitive load
            "attention_span": {"max": 20}
        }
    }

    validator = PILValidator(policy_templates=custom_policies)

    # Test with custom policies
    test_data = PerceptualData(
        domain=PerceptualDomain.SIGHT,
        data={"contrast_ratio": 6.5, "complexity_score": 4},  # Would pass default, fail custom
        intent="strict_accessibility_test"
    )

    validated, result = validator.validate([test_data])

    print(f"Custom Policy Validation: {'PASS' if result.is_valid else 'FAIL'}")
    print(f"Violations: {result.violations}")
    print(f"Suggestions: {result.suggestions}")

def main():
    """Run all PIL demonstrations"""
    print("🎯 Perceptual Intent Language (PIL) Demonstration")
    print("December 2025 - Complete Perceptual AI System\n")

    # Run demos
    demo_basic_validation()
    demo_game_asset_validation()

    # Async demo
    asyncio.run(demo_ai_interpretation())

    demo_custom_policies()

    print("\n🎮 PIL successfully demonstrated!")
    print("Ready for integration with LUXBIN and QuantumGameDev AI")

if __name__ == "__main__":
    main()