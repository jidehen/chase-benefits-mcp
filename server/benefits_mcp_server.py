import logging
from typing import List, Dict, Any
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP
from model.card_benefits_request import CardBenefitsRequest
from model.card_benefits_response import CardBenefitsResponse, CardBenefits, Multiplier, Perk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

# Mock card benefits data
MOCK_CARD_BENEFITS = {
    "freedom": {
        "card_id": "freedom",
        "card_name": "Chase Freedom",
        "annual_fee": 0.0,
        "multipliers": [
            {
                "category": "rotating_categories",
                "multiplier": 5.0,
                "description": "5% cash back on up to $1,500 in combined purchases in rotating categories each quarter"
            },
            {
                "category": "all_other_purchases",
                "multiplier": 1.0,
                "description": "1% cash back on all other purchases"
            }
        ],
        "perks": [
            {
                "name": "No Annual Fee",
                "description": "No annual fee",
                "value": 0.0
            }
        ],
        "point_value": 1.0
    },
    "freedom_unlimited": {
        "card_id": "freedom_unlimited",
        "card_name": "Chase Freedom Unlimited",
        "annual_fee": 0.0,
        "multipliers": [
            {
                "category": "all_purchases",
                "multiplier": 1.5,
                "description": "1.5% cash back on all purchases"
            }
        ],
        "perks": [
            {
                "name": "No Annual Fee",
                "description": "No annual fee",
                "value": 0.0
            }
        ],
        "point_value": 1.0
    },
    "sapphire_preferred": {
        "card_id": "sapphire_preferred",
        "card_name": "Chase Sapphire Preferred",
        "annual_fee": 95.0,
        "multipliers": [
            {
                "category": "travel_dining",
                "multiplier": 2.0,
                "description": "2X points on travel and dining at restaurants"
            },
            {
                "category": "all_other_purchases",
                "multiplier": 1.0,
                "description": "1X points on all other purchases"
            }
        ],
        "perks": [
            {
                "name": "Annual Fee",
                "description": "$95 annual fee",
                "value": 95.0
            },
            {
                "name": "Transfer Partners",
                "description": "Transfer points to airline and hotel partners",
                "value": None
            }
        ],
        "point_value": 1.25
    },
    "sapphire_reserve": {
        "card_id": "sapphire_reserve",
        "card_name": "Chase Sapphire Reserve",
        "annual_fee": 550.0,
        "multipliers": [
            {
                "category": "travel_dining",
                "multiplier": 3.0,
                "description": "3X points on travel and dining at restaurants"
            },
            {
                "category": "all_other_purchases",
                "multiplier": 1.0,
                "description": "1X points on all other purchases"
            }
        ],
        "perks": [
            {
                "name": "Annual Fee",
                "description": "$550 annual fee",
                "value": 550.0
            },
            {
                "name": "Travel Credit",
                "description": "$300 annual travel credit",
                "value": 300.0
            },
            {
                "name": "Transfer Partners",
                "description": "Transfer points to airline and hotel partners",
                "value": None
            },
            {
                "name": "Priority Pass",
                "description": "Priority Pass Select membership",
                "value": None
            }
        ],
        "point_value": 1.5
    }
}

# Initialize FastMCP server
mcp = FastMCP("Benefits")

def get_card_benefits_internal(card_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Get benefits for specified cards.
    
    Args:
        card_ids: List of card IDs to get benefits for
        
    Returns:
        List[Dict[str, Any]]: List of card benefits
        
    Raises:
        ValueError: If any card_id is not found
    """
    benefits = []
    for card_id in card_ids:
        if card_id not in MOCK_CARD_BENEFITS:
            raise ValueError(f"Card {card_id} not found")
        benefits.append(MOCK_CARD_BENEFITS[card_id])
    return benefits

async def get_card_benefits(request: CardBenefitsRequest) -> CardBenefitsResponse:
    """
    Get benefits for specified cards.
    
    Args:
        request: The card benefits request containing card IDs
        
    Returns:
        CardBenefitsResponse: The card benefits response
    """
    logger.info(f"Getting benefits for cards: {request.card_ids}")
    
    try:
        benefits = get_card_benefits_internal(request.card_ids)
        
        response_cards = [
            CardBenefits(
                card_id=benefit["card_id"],
                card_name=benefit["card_name"],
                annual_fee=benefit["annual_fee"],
                multipliers=[
                    Multiplier(**multiplier)
                    for multiplier in benefit["multipliers"]
                ],
                perks=[
                    Perk(**perk)
                    for perk in benefit["perks"]
                ],
                point_value=benefit["point_value"]
            )
            for benefit in benefits
        ]
        
        response = CardBenefitsResponse(cards=response_cards)
        logger.info(f"Found benefits for {len(response_cards)} cards")
        return response
        
    except ValueError as e:
        logger.error(f"Error getting card benefits: {str(e)}")
        return CardBenefitsResponse(cards=[])
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return CardBenefitsResponse(cards=[])

# Register MCP tool
@mcp.tool()
async def get_card_benefits_tool(request: CardBenefitsRequest) -> CardBenefitsResponse:
    """MCP tool for getting card benefits."""
    return await get_card_benefits(request)

if __name__ == "__main__":
    logger.info("Starting Benefits MCP server")
    mcp.run() 