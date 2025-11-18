# EnGenius Tools - Home Page

## Overview
The home page (`home.html`) provides a beautiful landing page with 4 tool buttons that redirect to different applications.

## How to Configure URLs

### Method 1: Edit tool-config.js (Recommended)
Open `tool-config.js` and update the URLs:

```javascript
const TOOL_URLS = {
    // Switch Comparison Tool
    'switch-comparison': 'https://your-url.com/switch-comparison',

    // Camera AI Token Calculator
    'camera-calculator': 'https://your-url.com/camera-calculator',

    // Switch EnGenius Filter (already configured)
    'switch-filter': 'index.html',

    // Access Point Comparison Tool
    'ap-comparison': 'https://your-url.com/ap-comparison'
};
```

### Tool IDs and Names

| Tool ID | Button Text | Current URL | Description |
|---------|-------------|-------------|-------------|
| `switch-comparison` | Switch Comparison Tool | Not configured | Compare multiple switches side by side |
| `camera-calculator` | Camera AI Token Calculator | Not configured | Calculate AI token requirements |
| `switch-filter` | Switch EnGenius Filter | `index.html` | Find the perfect switch (working) |
| `ap-comparison` | Access Point Comparison Tool | Not configured | Compare wireless access points |

## Usage

### To Access the Home Page:
```
http://localhost:8080/home.html
```

### To Set as Default Page:
Rename or create a symbolic link:
```bash
# Option 1: Rename (backup index first)
mv index.html switch-filter.html
mv home.html index.html

# Update tool-config.js to point to switch-filter.html instead
```

## Features

- **Beautiful gradient design** with different colors for each tool
- **Responsive layout** - works on desktop, tablet, and mobile
- **Hover animations** - cards lift up on hover
- **Icon indicators** - each tool has a unique emoji icon
- **Click protection** - shows alert for unconfigured tools
- **Easy configuration** - all URLs in one file

## Customization

### Change Tool Icons
Edit the emoji in `home.html`:
```html
<div class="tool-icon">🔄</div>  <!-- Change this emoji -->
```

### Change Tool Colors
The gradients are defined in CSS:
```css
.tool-card:nth-child(1) {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}
```

### Change Tool Descriptions
Edit the description text:
```html
<div class="tool-description">Your description here</div>
```

## Examples

### Example 1: Internal Tools
```javascript
'switch-comparison': 'comparison.html',
'camera-calculator': 'calculator.html',
```

### Example 2: External Tools
```javascript
'switch-comparison': 'https://tools.engenius.com/switch-compare',
'camera-calculator': 'https://tools.engenius.com/ai-calculator',
```

### Example 3: Relative Paths
```javascript
'switch-comparison': '../tools/comparison/index.html',
'camera-calculator': './camera-calc.html',
```

## Testing

1. Open `http://localhost:8080/home.html`
2. Click on "Switch EnGenius Filter" - should work (goes to index.html)
3. Click on other tools - should show "not configured" alert
4. Edit `tool-config.js` with your URLs
5. Refresh page and test again

## Notes

- URLs can be absolute or relative
- Use `#` to disable a tool temporarily
- The Switch Filter tool is already configured and working
- All tools open in the same window (not new tab)
