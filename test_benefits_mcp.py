import asyncio
import logging
from model.card_benefits_request import CardBenefitsRequest
from server.benefits_mcp_server import get_card_benefits

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_get_card_benefits():
    """Test getting benefits for different cards."""
    # Test single card
    request = CardBenefitsRequest(card_ids=["freedom"])
    response = await get_card_benefits(request)
    logger.info(f"Benefits for Freedom card: {response}")
    
    # Test multiple cards
    request = CardBenefitsRequest(card_ids=["sapphire_preferred", "sapphire_reserve"])
    response = await get_card_benefits(request)
    logger.info(f"Benefits for Sapphire cards: {response}")
    
    # Test invalid card
    request = CardBenefitsRequest(card_ids=["invalid_card"])
    response = await get_card_benefits(request)
    logger.info(f"Benefits for invalid card: {response}")

async def main():
    """Run all tests."""
    logger.info("Starting Benefits MCP tests")
    
    try:
        await test_get_card_benefits()
        logger.info("All tests completed successfully")
    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main()) 