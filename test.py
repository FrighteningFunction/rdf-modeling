import re
from collections import Counter

def find_common_patterns_v2(text, threshold=2):
    """
    Find non-alphanumeric patterns in the text for regex generation.
    """
    # Identify non-alphanumeric patterns and symbols
    tokens = re.findall(r'[^\w\s]', text)  # Extract only non-alphanumeric characters
    counter = Counter(tokens)
    
    # Find frequent symbols
    common_patterns = [token for token, freq in counter.items() if freq >= threshold]
    return common_patterns

def clean_text_with_improved_regex(text, common_patterns):
    """
    Clean the text using refined regex patterns.
    """
    # Generate regex for non-alphanumeric patterns
    for pattern in common_patterns:
        escaped_pattern = re.escape(pattern)  # Escape special characters
        text = re.sub(escaped_pattern, '', text)  # Remove the pattern
    
    # Remove extra spaces and normalize
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Input text
input_text = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exploring Space: The Next Frontier</title>
</head>
<body>
    <h1>Exploring Space: The Next Frontier 🚀</h1>
    <p>The universe is vast and largely unexplored. Despite advancements in space exploration, we have only begun to scratch the surface of what’s out there. 🌌</p>

    <h2>Why Explore Space?</h2>
    <p>Space exploration provides numerous benefits, including:
        <ul>
            <li><strong>Scientific discovery:</strong> New information about planets, stars, and galaxies.</li>
            <li><strong>Technological advancements:</strong> Innovations that often lead to everyday applications.</li>
            <li><strong>Inspiration for future generations:</strong> Space exploration has sparked the imaginations of young scientists and engineers around the world.</li>
        </ul>
    </p>

    <h3>The Mars Mission 🪐</h3>
    <p>NASA's Mars mission has captured the public's attention for years. The <a href="https://mars.nasa.gov" target="_blank">Perseverance rover</a>, launched in 2020, is currently on Mars, studying the planet's surface and searching for signs of ancient life. With human missions to Mars planned for the 2030s, the excitement continues to grow! 🌍🚀</p>

    <h4>Key Discoveries:</h4>
    <ul>
        <li>Evidence of ancient rivers and lakes 🏞️</li>
        <li>Signs of past volcanic activity 🔥</li>
        <li>Discovery of Martian dust storms 🌬️</li>
    </ul>

    <h3>Space Tourism: The Future of Travel? ✈️</h3>
    <p>With companies like <strong>SpaceX</strong> and <strong>Blue Origin</strong> pushing the boundaries of space travel, space tourism is becoming a reality. While it’s still in its infancy, this industry promises to make space travel more accessible to the wealthy in the near future.</p>

    <h5>Challenges to Overcome:</h5>
    <ul>
        <li>High cost of space travel 💸</li>
        <li>Space debris and safety risks 🚀</li>
        <li>Environmental impact 🌍</li>
    </ul>

    <p><em>In conclusion, space exploration continues to be one of the most exciting and forward-thinking endeavors of humanity. The possibilities for discovery are endless, and the journey has only just begun.</em></p>

    <footer>
        <p>For more information, visit <a href="https://www.nasa.gov" target="_blank">NASA's official website</a>.</p>
    </footer>

    <p>#spaceexploration #marsmission #spacetourism #future #technology</p>
</body>
</html>

"""

# Step 1: Find common patterns (non-alphanumeric symbols)
common_patterns = find_common_patterns_v2(input_text)
print("Common Patterns:", common_patterns)

# Step 2: Clean text with improved regex
cleaned_text = clean_text_with_improved_regex(input_text, common_patterns)

print("Cleaned Text:\n", cleaned_text)
