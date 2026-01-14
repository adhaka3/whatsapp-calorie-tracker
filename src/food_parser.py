"""Food parser for extracting meals and calculating nutrition"""
import json
import os
from typing import Dict, List, Tuple
import re
from difflib import SequenceMatcher


class FoodParser:
    def __init__(self, food_database_path: str = "data/indian_foods.json", llm_provider: str = None, use_llm: bool = False):
        """
        Initialize the food parser
        
        Args:
            food_database_path: Path to the Indian foods JSON database
            llm_provider: 'openai', 'anthropic', or None for regex-only (default: None)
            use_llm: If True, will use LLM when available. If False, uses regex only (default: False)
        """
        self.llm_provider = llm_provider
        self.use_llm = use_llm
        self.client = None
        
        # Load food database
        with open(food_database_path, 'r') as f:
            self.food_db = json.load(f)
        
        # Create a searchable index
        self.food_index = self._create_food_index()
        
        # Initialize LLM client only if requested
        if self.use_llm and self.llm_provider:
            try:
                self._init_llm_client()
            except Exception as e:
                print(f"Warning: Could not initialize LLM client: {e}")
                print("Falling back to regex-based parsing (free, no API needed!)")
                self.use_llm = False
    
    def _init_llm_client(self):
        """Initialize the appropriate LLM client"""
        if self.llm_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            
            try:
                from openai import OpenAI
                import httpx
                
                # Create a clean httpx client without proxy settings
                http_client = httpx.Client(
                    timeout=30.0,
                    limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
                )
                
                # Initialize OpenAI client with explicit http_client
                self.client = OpenAI(
                    api_key=api_key,
                    max_retries=2,
                    timeout=30.0,
                    http_client=http_client
                )
            except Exception as e:
                raise ValueError(f"Failed to initialize OpenAI client: {e}")
        elif self.llm_provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
    
    def _create_food_index(self) -> Dict:
        """Create a searchable index of foods"""
        index = {}
        for food in self.food_db:
            # Add main name
            index[food['name'].lower()] = food
            # Add aliases
            for alias in food.get('aliases', []):
                index[alias.lower()] = food
        return index
    
    def parse_meal_with_llm(self, user_message: str) -> List[Dict]:
        """Use LLM to extract food items and quantities from user message"""
        
        if not self.use_llm or not self.client:
            # LLM not available, use regex parser
            return self._simple_parse(user_message)
        
        # Create a prompt for the LLM
        prompt = f"""You are a helpful nutrition assistant. Extract all food items and their quantities from the user's message.

Available foods in database: {', '.join([food['name'] for food in self.food_db])}

User message: "{user_message}"

Extract food items in JSON format. For each item, identify:
1. The food name (match to closest item in the database)
2. The quantity/multiplier (e.g., "2 rotis" = quantity 2, "1 bowl dal" = quantity 1)

Return ONLY a JSON array like this:
[
  {{"food": "roti", "quantity": 2}},
  {{"food": "dal", "quantity": 1}}
]

If no food items are found, return an empty array: []
"""

        try:
            if self.llm_provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a nutrition tracking assistant. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                llm_response = response.choices[0].message.content.strip()
            
            elif self.llm_provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=500,
                    temperature=0.3,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                llm_response = response.content[0].text.strip()
            
            # Extract JSON from response
            llm_response = llm_response.strip()
            # Remove markdown code blocks if present
            llm_response = re.sub(r'^```json\s*', '', llm_response)
            llm_response = re.sub(r'\s*```$', '', llm_response)
            
            parsed_items = json.loads(llm_response)
            return parsed_items
        
        except Exception as e:
            print(f"Error parsing with LLM: {e}")
            # Fallback to simple parsing
            return self._simple_parse(user_message)
    
    def _fuzzy_match_score(self, str1: str, str2: str) -> float:
        """Calculate fuzzy matching score between two strings"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def _find_best_food_match(self, food_text: str, threshold: float = 0.6) -> tuple:
        """Find the best matching food from database using fuzzy matching"""
        best_match = None
        best_score = threshold
        
        food_text_lower = food_text.lower().strip()
        
        # First try exact match
        if food_text_lower in self.food_index:
            return self.food_index[food_text_lower]['name'], 1.0
        
        # Then try fuzzy matching
        for food_name, food_data in self.food_index.items():
            score = self._fuzzy_match_score(food_text_lower, food_name)
            if score > best_score:
                best_score = score
                best_match = food_data['name']
        
        return best_match, best_score
    
    def _simple_parse(self, user_message: str) -> List[Dict]:
        """Advanced regex-based parsing without LLM (FREE!)"""
        items = []
        message_lower = user_message.lower()
        
        # Remove common prefixes
        message_lower = re.sub(r'^(i had|i ate|ate|had|eating|consumed)\s+', '', message_lower)
        
        # Split by common delimiters
        parts = re.split(r'\s+and\s+|\s+with\s+|,\s*|\s+&\s+', message_lower)
        
        found_foods = set()  # Track found foods to avoid duplicates
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Extract quantity and food name
            # Pattern: "2 rotis", "3 idlis", "1 bowl dal", etc.
            quantity_patterns = [
                r'^(\d+)\s+(?:pieces?\s+of\s+)?(?:bowls?\s+(?:of\s+)?)?(?:plates?\s+(?:of\s+)?)?(\w+(?:\s+\w+)*)',
                r'^(\d+)\s+(\w+)',
                r'^(\w+(?:\s+\w+)*)',  # No number, just food name
            ]
            
            quantity = 1
            food_text = part
            
            for pattern in quantity_patterns:
                match = re.search(pattern, part)
                if match:
                    if len(match.groups()) == 2:
                        quantity = int(match.group(1))
                        food_text = match.group(2)
                    else:
                        food_text = match.group(1)
                    break
            
            # Clean up food text
            food_text = re.sub(r'\s+', ' ', food_text).strip()
            
            # Try to find matching food in database
            best_match, score = self._find_best_food_match(food_text)
            
            if best_match and best_match not in found_foods:
                items.append({
                    'food': best_match,
                    'quantity': quantity
                })
                found_foods.add(best_match)
        
        # If no items found with splitting, try direct matching
        if not items:
            for food_name, food_data in self.food_index.items():
                if food_name in message_lower:
                    if food_data['name'] not in found_foods:
                        # Try to extract quantity
                        quantity = 1
                        pattern = r'(\d+)\s*' + re.escape(food_name)
                        match = re.search(pattern, message_lower)
                        if match:
                            quantity = int(match.group(1))
                        
                        items.append({
                            'food': food_data['name'],
                            'quantity': quantity
                        })
                        found_foods.add(food_data['name'])
        
        return items
    
    def calculate_nutrition(self, parsed_items: List[Dict]) -> Tuple[float, float, List[Dict]]:
        """Calculate total calories and protein from parsed items"""
        total_calories = 0
        total_protein = 0
        detailed_items = []
        
        for item in parsed_items:
            food_name = item['food'].lower()
            quantity = item.get('quantity', 1)
            
            if food_name in self.food_index:
                food_data = self.food_index[food_name]
                
                item_calories = food_data['calories'] * quantity
                item_protein = food_data['protein'] * quantity
                
                total_calories += item_calories
                total_protein += item_protein
                
                detailed_items.append({
                    'name': food_data['name'],
                    'quantity': quantity,
                    'serving_size': food_data['serving_size'],
                    'calories': round(item_calories, 1),
                    'protein': round(item_protein, 1)
                })
        
        return round(total_calories, 1), round(total_protein, 1), detailed_items
    
    def process_message(self, user_message: str) -> Dict:
        """Complete pipeline: parse message and calculate nutrition"""
        
        # Check for summary requests
        message_lower = user_message.lower()
        if any(word in message_lower for word in ['summary', 'total', 'today', 'stats', 'how much']):
            return {'type': 'summary_request'}
        
        # Check for export requests
        if any(word in message_lower for word in ['export', 'download', 'excel']):
            return {'type': 'export_request'}
        
        # Parse the meal
        parsed_items = self.parse_meal_with_llm(user_message)
        
        if not parsed_items:
            # Get available foods for better error message
            common_foods = [food['name'] for food in self.food_db[:15]]  # Show first 15
            return {
                'type': 'no_food_found',
                'message': f"❌ Sorry, I couldn't find any food items from our database in your message.\n\n"
                          f"📋 Common foods I can track:\n{', '.join(common_foods)}\n\n"
                          f"💡 Try: '2 rotis and dal' or 'had chicken biryani'\n\n"
                          f"Type 'list' to see all available foods."
            }
        
        # Calculate nutrition
        total_calories, total_protein, detailed_items = self.calculate_nutrition(parsed_items)
        
        # Check if any items were actually found in database
        if not detailed_items:
            unmatched_foods = [item['food'] for item in parsed_items]
            return {
                'type': 'not_in_database',
                'unmatched_items': unmatched_foods,
                'message': f"❌ These items are not in our database: {', '.join(unmatched_foods)}\n\n"
                          f"💡 Please try similar food items or add them to the database.\n\n"
                          f"Type 'list' to see available foods."
            }
        
        # Check for partial matches
        if len(detailed_items) < len(parsed_items):
            matched = [item['name'] for item in detailed_items]
            unmatched = [item['food'] for item in parsed_items if item['food'] not in [m.lower() for m in matched]]
            
            return {
                'type': 'partial_match',
                'total_calories': total_calories,
                'total_protein': total_protein,
                'items': detailed_items,
                'parsed_items': parsed_items,
                'unmatched_items': unmatched,
                'warning': f"⚠️ Note: These items were not found in database: {', '.join(unmatched)}"
            }
        
        return {
            'type': 'meal_logged',
            'total_calories': total_calories,
            'total_protein': total_protein,
            'items': detailed_items,
            'parsed_items': parsed_items
        }
    
    def get_food_list(self, category: str = "all") -> str:
        """Get formatted list of available foods"""
        if category == "all":
            foods_by_type = {}
            for food in self.food_db:
                # Simple categorization based on food name
                if food['name'] in ['roti', 'naan', 'paratha', 'puri', 'dosa', 'idli', 'uttapam']:
                    category = "🍞 Breads"
                elif food['name'] in ['rice', 'biryani', 'khichdi', 'poha', 'upma']:
                    category = "🍚 Rice & Grains"
                elif food['name'] in ['dal', 'rajma', 'chana masala', 'sambar']:
                    category = "🫘 Lentils & Beans"
                elif food['name'] in ['butter chicken', 'chicken curry', 'egg curry', 'palak paneer']:
                    category = "🍛 Curries"
                elif food['name'] in ['paneer', 'curd', 'milk', 'lassi', 'raita']:
                    category = "🥛 Dairy"
                elif food['name'] in ['boiled egg', 'omelette']:
                    category = "🥚 Eggs"
                elif food['name'] in ['samosa', 'vada', 'gulab jamun', 'jalebi']:
                    category = "🍘 Snacks & Sweets"
                elif food['name'] in ['tea', 'coffee']:
                    category = "☕ Beverages"
                elif food['name'] in ['banana', 'apple']:
                    category = "🍎 Fruits"
                else:
                    category = "🍽️ Other"
                
                if category not in foods_by_type:
                    foods_by_type[category] = []
                foods_by_type[category].append(food['name'])
            
            result = "📋 *Available Foods:*\n\n"
            for cat, foods in sorted(foods_by_type.items()):
                result += f"{cat}\n{', '.join(sorted(foods))}\n\n"
            
            result += "💡 *Usage:* Send '2 rotis and dal' or 'had biryani'"
            return result
        else:
            foods = [food['name'] for food in self.food_db]
            return f"Available foods: {', '.join(sorted(foods))}"